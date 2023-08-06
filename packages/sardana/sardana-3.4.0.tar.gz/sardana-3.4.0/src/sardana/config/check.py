# -*- coding: utf-8 -*-

##############################################################################
##
## This file is part of Sardana
## 
## http://www.tango-controls.org/static/sardana/latest/doc/html/index.html
##
## Copyright 2019 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Sardana is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Sardana is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""
This script loads and validates a YAML sardana config (see example file).

Here we assume that the config has already passed a validation check so
that we know that the format itself is correct.

Note that in order to do checks on controller configuration, the script
needs to be run in the same python environment that sardana will use (or
at least one that contains all the same controller code). This is because
it needs to inspect the controllers' code. It does not require sardana to
be running, though.
"""

import importlib
import logging
import os
import sys

import sardana
from yaml import load, Loader


logger = logging.getLogger(__name__)


def get_py_class(module_path, class_name):
    """Import a class from the module at the given filesystem path"""
    spec = importlib.util.spec_from_file_location("ctrl_conf", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


def check_ctrl_props(pos, ctrl_class, ctrl_conf):
    class_props = {
        name.lower(): value
        for name, value in getattr(ctrl_class, "ctrl_properties", {}).items()
    }
    for name, value in ctrl_conf.get("properties", {}).items():
        if name.lower() not in class_props:
            yield [*pos, "ctrl_properties", name], f"Unknown controller property {name}"
            continue
        prop_info = class_props[name.lower()]
        if prop_info[sardana.pool.controller.Type]:
            # We could check type here...
            # Guess sardana (or tango) has some way to do it?
            pass


def check_ctrl_attrs(pos, ctrl_class, ctrl_conf):
    class_attrs = {
        name.lower(): value
        for name, value in getattr(ctrl_class, "ctrl_attributes", {}).items()
    }
    for name, value in ctrl_conf.get("attributes", {}).items():
        path = [*pos, "ctrl_attributes", name]
        if name.lower() not in class_attrs:
            yield path, f"Unknown controller attribute {name}"
            continue
        prop_info = class_attrs[name.lower()]
        prop_type = prop_info[sardana.pool.controller.Type]
        if prop_type:
            if callable(prop_type):
                try:
                    prop_type(value)
                except TypeError as e:
                    yield path, f"Value has bad type: {e}"
            # We could check type here...
            # Guess sardana (or tango) has some way to do it?
            pass


def check_axis_attrs(pos, ctrl_class, element_conf):
    class_attrs = {
        name.lower(): value
        for name, value in getattr(ctrl_class, "axis_attributes", {}).items()
    }
    for name, value in element_conf.get("attributes", {}).items():
        pos = [*pos, "elements", element_conf["name"], "attributes", name]
        if name.lower() not in class_attrs:
            yield pos, f"Unknown axis attribute {name}"
            continue
        prop_info = class_attrs[name.lower()]
        prop_type = prop_info[sardana.pool.controller.Type]
        if prop_type:
            if callable(prop_type):
                try:
                    prop_type(value)
                except TypeError as e:
                    yield pos, f"Value has bad type: {e}"
            # We could check type here...
            # Guess sardana (or tango) has some way to do it?
            pass


def check_tango_attr_conf(pos, ctrl_class, element_conf):
    tango_attr_conf = element_conf.get("tango_attribute_config", [])
    axis_attrs = {
        attr.lower()
        for attr in (
                *getattr(ctrl_class, "standard_axis_attributes", []),
                *getattr(ctrl_class, "axis_attributes", [])
        )
    }
    for attr, props in tango_attr_conf.items():
        if attr.lower() not in axis_attrs:
            yield ([*pos, "tango_attribute_properties", "attr"],
                   f"No axis attribute called {attr}")
            continue
        # TODO sanity check props; this should be standard config stuff like label, unit...


def get_pos(d, key, pos_prefix=()):
    """
    Generate items found by the given key. Also yields positions for each item, with prefix
    """
    yield from (([*pos_prefix, key, name], item)
                for name, item in d[key].items())


def check_physical_roles(pos, ctrl_conf, ctrl_class, roles_key, all_ctrl_elements):
    """
    Check that the expected physical roles are defined.
    """
    # TODO are role names case sensitive?

    conf_roles = dict(ctrl_conf.get("physical_roles", {}))
    if ctrl_class:
        class_roles = getattr(ctrl_class, roles_key, [])
        for class_role_name in class_roles:
            try:
                conf_role_element = conf_roles.pop(class_role_name)
            except KeyError:
                yield [*pos, "physical_roles"], f"Motor role '{class_role_name}' not configured"
                continue
            if conf_role_element.lower() not in all_ctrl_elements:
                # Should be a reference to an existing element
                # TODO check that it's the right kind of element (motor/counter?)
                yield ([*pos, "physical_roles", class_role_name],
                       f"Physical role '{class_role_name}' refers to unknown element '{conf_role_element}'")
        if conf_roles:
            # Should be emptied by the loop above, otherwise
            # we have extra definitions not recognized by the class.
            for role in conf_roles:
                yield ([*pos, "physical_roles", role],
                       f"Physical role '{role}' does not exist in controller class '{ctrl_class.__name__}'")
    else:
        for role, element in conf_roles.items():
            if element.lower() not in all_ctrl_elements:
                yield ([*pos, "physical_roles", role],
                       f"Physical role {role} refers to unknown element {element}")


def check_pseudo_roles(pos, ctrl_conf, ctrl_class, role_key):
    """
    Check that the expected pseudo roles are defined.
    """
    # TODO are role names case sensitive?
    elements = ctrl_conf.get("elements", {})
    if ctrl_class:
        pseudo_roles = getattr(ctrl_class, role_key, [])
        found_roles = set()
        if not pseudo_roles:
            # The class may omit the roles; in that case there will be a default role
            # named after the class.
            pseudo_roles = [ctrl_class.__name__]
        for el_name, element in elements.items():
            axis = element["axis"]
            try:
                role = pseudo_roles[axis - 1]
            except IndexError:
                axis_roles = list(zip(range(1, len(pseudo_roles) + 1), pseudo_roles))
                yield [*pos, "elements", el_name], (
                    f"Axis {axis} does not exist in controller class {ctrl_class.__name__}."
                    f" Existing axes: {axis_roles}"
                )
            else:
                # Note that we can't really verify here that the axis corresponds to the
                # correct role, we must assume the user knows what they are doing.
                logger.info(f"Found role {role} for axis {axis} on {ctrl_conf['type']}"
                            + f" controller {pos[-1]} (class {ctrl_class.__name__})")
                found_roles.add(role)
        missing_roles = set(pseudo_roles) - found_roles
        if missing_roles:
            yield [*pos, "elements"], f"No elements configured for roles: {', '.join(missing_roles)}"
    else:
        # No class info, we can just do a simple check of axis numbers
        axes = []
        for el_name, element in elements.items():
            axis = element["axis"]
            axes.append(axis)
        if sorted(axes) != list(range(1, len(elements) + 1)):
            yield [*pos, "elements"], "Expected axes to be consecutively numbered from 1."


def check_instruments(ctrl_pos, ctrl_conf, instruments):
    elements = ctrl_conf.get("elements", [])
    for name, element in elements.items():
        instr = element.get("instrument")
        if instr and instr not in instruments:
            yield [*ctrl_pos, "elements", name, "instrument"], f"Instrument {instr} is not defined"


def get_ctrl_elements(config):
    """
    Return two dicts containing, respectively, all controllers and all controller elements
    """
    ctrls = {}
    elements = {}
    for _, pool in config.get("pools", {}).items():
        for ctrl_name, ctrl in pool.get("controllers", {}).items():
            ctrls[ctrl_name.lower()] = ctrl
            for el_name, element in ctrl.get("elements", {}).items():
                elements[el_name.lower()] = element
    return ctrls, elements


def load_python_class(pymodule, classname, paths):

    # Note that this is potentially dangerous, as the
    # controller module could do whatever it likes on
    # import. Guess it's probably better that this happens
    # sooner than later... don't think there's really a safe
    # way to do this.
    #
    # Since we don't actually need to *run* the controller, we
    # should, in principle, be able to get away with parsing
    # and inspecting the AST. Though I bet it would be tricky
    # to check subclass and stuff that way.

    pypath, pyname = os.path.split(pymodule)
    if pypath:
        # We got the complete path to the module
        try:
            return get_py_class(pymodule, classname)
        except ImportError as ie:
            raise RuntimeError(f"Could not load python code: {ie}")
        except FileNotFoundError as fe:
            raise RuntimeError(f"Could not find python code: {fe}")
        except AttributeError as ae:
            raise RuntimeError(f"Could not find python class: {ae}")

    else:
        # Just controller name given, need to look it up
        for _path in paths:
            pymodule = f"{_path}/{pyname}"
            try:
                return get_py_class(pymodule, classname)
            except ImportError as ie:
                raise RuntimeError(f"Could not load python code: {ie}")
            except FileNotFoundError:
                pass
            except AttributeError as ae:
                raise RuntimeError(f"Could not find python class: {ae}")
        else:
            raise RuntimeError(f"Could not find or load code for {pyname}")


def check_measurement_groups(pos, meas_grps, ctrls, ctrl_elements):
    for meas_grp, meas_grp_conf in meas_grps.items():
        for ctrl_name, ctrl_conf in meas_grp_conf.get("controllers", {}).items():
            if ctrl_name.lower() not in ctrls:
                yield [*pos, meas_grp, "controllers", ctrl_name], f"Unknown controller {ctrl_name}"
                continue
        for channel_i, channel in enumerate(meas_grp_conf.get("channels", [])):
            if isinstance(channel, str):
                # The normal case
                channel_name = channel
            else:
                # A bit weird but this is how you add config to a channel;
                # it is a dict of one key - the name - containing a config dict.
                channel_name = list(channel.keys())[0]
            if channel_name.lower() not in ctrl_elements:
                yield ([*pos, meas_grp, "channels", channel_i],
                       f"Channel refers to unknown element {channel_name}")


def check_config(config, load_code=True):
    """
    Takes a config dict, and checks that it is valid.
    This is a generator that yields tuples of config position and error message.
    If nothing is yielded, it means the config was considered to be valid.
    """

    all_ctrls, all_ctrl_elements = get_ctrl_elements(config)

    for pos, pool in get_pos(config, "pools"):
        pool_paths = pool.get("pool_path", [])
        sardana_path = sardana.__path__[0]
        default_pool_path = f"{sardana_path}/pool/poolcontrollers/"

        instruments = pool.get("instruments")

        for ctrl_pos, ctrl_conf in get_pos(pool, "controllers", pos):
            ctrl_name = ctrl_pos[-1]
            ctrl_type = ctrl_conf["type"]
            pymodule = ctrl_conf.get("python_module")
            pyclass = ctrl_conf.get("python_class")
            if load_code:
                # Find and import the controller class.
                try:
                    ctrl_class = load_python_class(pymodule, pyclass,
                                                   [*pool_paths, default_pool_path])  # TODO correct order?
                except RuntimeError as e:
                    yield ctrl_pos, str(e)
                    logger.warning(f"No further sanity checks possible on controller {ctrl_name}."
                                   + " Could not import code.")
                    continue

                yield from check_ctrl_props(ctrl_pos, ctrl_class, ctrl_conf)
                yield from check_ctrl_attrs(ctrl_pos, ctrl_class, ctrl_conf)

            else:
                logger.info("Controller loading disabled; no code consistency checks")
                ctrl_class = None

            yield from check_instruments(ctrl_pos, ctrl_conf, instruments)

            # More specific checks for some controller types
            if ctrl_type == "PseudoMotor":
                yield from check_physical_roles(ctrl_pos, ctrl_conf, ctrl_class,
                                                "motor_roles", all_ctrl_elements)
                yield from check_pseudo_roles(ctrl_pos, ctrl_conf, ctrl_class, "pseudo_motor_roles")
            if ctrl_type == "PseudoCounter":
                yield from check_physical_roles(ctrl_pos, ctrl_conf, ctrl_class,
                                                "counter_roles", all_ctrl_elements)
                # TODO this fails on IoverI0, which has no pseudo_counter_roles
                yield from check_pseudo_roles(ctrl_pos, ctrl_conf, ctrl_class, "pseudo_counter_roles")

            # TODO any more controller types that need special checks?

        meas_grps = pool.get("measurement_groups")
        if meas_grps:
            yield from check_measurement_groups([*pos, "measurement_groups"],
                                                meas_grps,
                                                all_ctrls, all_ctrl_elements)


if __name__ == "__main__":
    from pydantic import ValidationError

    from .model import Configuration

    # If there are YAML syntax error, we just raise them right away
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            config = load(f, Loader=Loader)
    else:
        config = load(sys.stdin, Loader=Loader)

    try:
        Configuration(**config)
    except ValidationError as e:
        sys.exit(f"Failed to validate the configuration format: {e}")

    errors = list(check_config(config))
    if errors:
        for path, error in errors:
            logger.error(f"{' -> '.join(path)}: {error}")
        sys.exit("!!! Configuration is not valid - or could not be validated !!!")
    else:
        print("*** Configuration looks good! ***")
