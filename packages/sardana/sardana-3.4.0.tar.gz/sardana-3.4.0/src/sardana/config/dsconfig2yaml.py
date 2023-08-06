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
This script takes a dsconfig representation (could be a straight dump)
of a sardana configuration and produces a YAML sardana config file.
The goal is that this should be a 1 to 1 transformation.

Making a suitable dump (make sure to include all important servers):
$ python -m dsconfig.dump server:Pool/1 server:MacroServer/1 > my_dsconfig.json

Running this script (giving the relevant macroserver name):
$ python dsconfig2yaml.py my_dsconfig.json my/macroserver/1
"""

import copy
import json
import logging
import tango

from sardana.pool import AcqSynchType
from sardana.taurus.core.tango.sardana import PlotType
from sardana.pool.pool import ElementType, TYPE_MAP_OBJ
from tango.utils import CaselessDict, CaselessList

from .common import clean_dict, get_full_name


logger = logging.getLogger(__name__)


def get_tango_host():
    return tango.ApiUtil.get_env_var("TANGO_HOST")


def find_device(config, cls, name):
    for servername, instances in config["servers"].items():
        for instname, classes in instances.items():
            for classname, clss in classes.items():
                if classname.lower() == cls.lower():
                    for devicename, device in clss.items():
                        if devicename.lower() == name.lower():
                            return servername, instname, classes, device
    raise KeyError(f"Device {name} not found!")


def find_pools(config):
    for servername, instances in config["servers"].items():
        for instname, classes in instances.items():
            for classname, clss in classes.items():
                if classname.lower() == "pool":
                    for devicename, device in clss.items():
                        # Return both device and alias, for lookup
                        yield devicename.lower(), (servername, instname, classes, devicename, device)
                        alias = device["alias"]
                        yield alias, (servername, instname, classes, devicename, device)


def build_instruments(instrument_list):
    if not instrument_list:
        return None  # If there are no instruments dont crash
    for clss, name in zip(instrument_list[::2],
                          instrument_list[1::2]):
        yield name, {"class": clss}


def get_property(device, name, multiple=False):
    properties = CaselessDict(device.get("properties", {}))
    if name in properties:
        values = properties[name]
        if multiple:
            return values
        if len(values) == 1:
            return values[0]
        else:
            raise ValueError(f"Expected exactly one value of property {name}"
                             + f" for device {device}; found{values}")


def destringify(value):
    try:
        # So, let's guess the type!
        # TODO add tests for various types
        # TODO still we have the problem of ambiguity between the string "true" and
        # the boolean "true"...
        return json.loads(value)
    except ValueError:
        return value


def get_memorized_value(values):
    if len(values) == 1:
        value = values[0]
        # Data type is not available to us. I guess the only real way is
        # to inspect the controller class.
        return destringify(value)


def get_property_value(lst: list):
    if len(lst) == 1:
        return destringify(lst[0])
    else:
        return [destringify(v) for v in lst]
    

def get_attribute_properties(device, name, polled_attr={}, skip_values=set()):
    results = {}
    if polled_attr:
        for attr, period in polled_attr.items():
            if attr.lower() == name.lower():
                results["polling_period"] = period
    properties = CaselessDict(device.get("attribute_properties", {}))
    if results or name in properties:
        for prop, values in properties[name].items():
            if prop.lower() == "__value_ts":
                continue
            if prop.lower() == "__value":
                if name in skip_values:
                    continue
                results["value"] = get_memorized_value(values)
            elif prop.lower() in {"abs_change",
                                  "rel_change",
                                  "archive_abs_change",
                                  "archive_rel_change"}:
                # Loading as JSON will convert to int or float depending
                # on the string format. This is better for diffing.
                if len(values) == 2:
                    vneg = json.loads(values[0])
                    vpos = json.loads(values[1])
                    if vneg == -vpos:
                        results[prop] = vpos
                    else:
                        results[prop] = [vneg, vpos]
                else:
                    # Not sure under what circumstances this can happen,
                    # but it appears to be valid.
                    results[prop] = json.loads(values[0])
            elif prop.lower() in {"min_value",
                                  "max_value",
                                  "min_alarm",
                                  "max_alarm"}:
                value, = values
                results[prop] = json.loads(value)
            elif prop.lower() in {"label",
                                  "format",
                                  "unit"}:
                results[prop] = values[0]
        if len(results) == 1 and "value" in results:
            return results["value"]
        return results


def get_polled_attrs(device):
    polled_attr = get_property(device, "polled_attr", multiple=True)
    if polled_attr:
        return {
            attr: int(period)
            for attr, period in zip(polled_attr[::2], polled_attr[1::2])
        }
    return {}


SPECIAL_ELEMENT_PROPERTIES = CaselessList(
    ["axis", "ctrl_id", "instrument_id", "DriftCorrection"]
)  # TODO more?


def build_element(devicename, element, ctrl_name, ctrl_type):
    alias = element.get("alias")
    axis = int(get_property(element, "axis"))
    info = {
        "axis": axis
    }
    polled_attr = get_polled_attrs(element)

    # Attributes with configuration parameters
    if ctrl_type == "Motor":
        # DialPosition is not part of configuration, however it is stored
        # in the Tango DB and is used by the drift correction feature
        # of pseudo motors.
        skip_values = tango.utils.CaselessList(["DialPosition"])
    else:
        skip_values = set()
    attributes = {
        attr: get_attribute_properties(element, attr, polled_attr,
                                       skip_values=skip_values)
        for attr in element.get("attribute_properties", [])
        if attr != "DialPosition"
    }
    if ctrl_type == "PseudoMotor":
        drift_correction = get_property(element, "DriftCorrection")
        if drift_correction is not None and drift_correction.lower() == "true":
            info["drift_correction"] = True
    # TODO 'Force_HW_Read'?

    # Fill in any other attributes that happen to be polled
    for attr, period in polled_attr.items():
        caseless_attrs = CaselessDict({attrname: attrname for attrname in attributes})
        if attr not in caseless_attrs:
            attributes[attr] = {"polling_period": period}
    if attributes:
        info["attributes"] = attributes

    instrument_id = get_property(element, "Instrument_id")
    if instrument_id:
        info["instrument"] = instrument_id
    type_data = TYPE_MAP_OBJ[ElementType[ctrl_type]]
    default_name = type_data.auto_full_name.format(ctrl_name=ctrl_name, axis=axis)
    if devicename.lower() != default_name.lower():
        # Non-default device name
        info["tango_device"] = devicename

    return alias, info


def find_ctrl_elements(server, ctrl_name, ctrl_type):
    logger.debug(f"find_ctrl_elements {ctrl_name}, {ctrl_type}")
    for class_name, devices in server.items():
        if class_name.lower() == ctrl_type.lower():
            for devicename, element in devices.items():
                ctrl_id = get_property(element, "ctrl_id")
                if ctrl_id.lower() == ctrl_name.lower():
                    yield build_element(devicename, element, ctrl_name, ctrl_type)


def sort_elements(elements):
    return sorted(elements, key=lambda e: e[1].get("axis"))


def get_controller_device_name(devname, klass, name):
    "Check if device name deviates from the default, in that case, store it"
    if devname.lower() == f"controller/{klass}/{name}".lower():
        return None
    return devname


SPECIAL_CTRL_PROPERTIES = CaselessList(
    ["type", "klass", "library", "physical_roles"]
)


CONTROLLER_TYPE_ORDER = [
    "Motor",
    "PseudoMotor",
    "CTExpChannel",
    "ZeroDExpChannel",
    "OneDExpChannel",
    "TwoDExpChannel",
    "PseudoCounter",
    "TriggerGate",
    "IORegister",
]


def sort_controllers(ctrls):
    "Get the controllers sorted in the standard way"
    return sorted(ctrls, key=lambda c: CONTROLLER_TYPE_ORDER.index(c[1]["type"]))


def find_controllers(server):
    for devname, ctrl in server["Controller"].items():
        # Note that we want a consistent order of the keys here, don't
        # change it unless you know what you're doing.
        alias = ctrl["alias"]
        ctrl_type = get_property(ctrl, "type")
        logger.debug(f"Found controller {alias} of type {ctrl_type}")
        ctrl_class = get_property(ctrl, "klass")
        ctrl_info = {
            "type": ctrl_type,
            "tango_device": get_controller_device_name(devname, ctrl_class, alias),
            "python_class": ctrl_class,
            "python_module": get_property(ctrl, "library"),
        }

        # Allow extra properties (settings etc)
        extra_properties = {
            prop: get_property_value(value)
            for prop, value in ctrl.get("properties", {}).items()
            if prop not in SPECIAL_CTRL_PROPERTIES
        }
        if extra_properties:
            ctrl_info["properties"] = extra_properties
        attributes = {
            attr: get_attribute_properties(ctrl, attr)
            for attr in ctrl.get("attribute_properties", [])
        }
        if attributes:
            ctrl_info["attributes"] = attributes

        if ctrl_type in {"PseudoMotor", "PseudoCounter"}:
            pr_prop = ctrl["properties"].get("physical_roles")
            if pr_prop:
                physical_roles = {
                    role: axis
                    for role, axis in zip(pr_prop[::2], pr_prop[1::2])
                }
                ctrl_info["physical_roles"] = physical_roles

        ctrl_info["elements"] = dict(sort_elements(find_ctrl_elements(server, alias, ctrl_type)))
        yield alias, clean_dict(ctrl_info)


def find_measurement_groups(server):
    tg_fullname_to_name = {
        get_full_name(name, get_tango_host()): tg["alias"]
        for name, tg in server.get("TriggerGate", {}).items()
    }
    for name, mntgrp in server.get("MeasurementGroup", {}).items():
        config = {}
        alias = mntgrp["alias"]
        configuration = get_attribute_properties(device=mntgrp, name="configuration")
        if configuration:
            assert isinstance(configuration, dict),\
                f"Expected measurement group configuration to be a JSON object; got {configuration}"
            channels_raw = []
            for ctrl in configuration["controllers"].values():
                synchronizer = ctrl.get("synchronizer")
                synchronization = ctrl.get("synchronization")
                timer = ctrl.get("timer")
                monitor = ctrl.get("monitor")
                ctrl_channels = copy.deepcopy(list(ctrl["channels"].values()))
                ch_fullname_to_name = {ch["full_name"]:ch["name"] for ch in ctrl_channels}
                ctrl_channels_sorted = sorted(ctrl_channels, key=lambda ch: ch["index"])
                for ch in ctrl["channels"].values():
                    if synchronizer is not None and synchronizer != "software":
                        ch["synchronizer"] = tg_fullname_to_name[synchronizer]
                    if synchronization is not None and synchronization != AcqSynchType.Trigger:
                        ch["synchronization"] = AcqSynchType.get(synchronization)
                    if timer is not None:
                        timer_name = ch_fullname_to_name[timer]
                        if timer_name != ctrl_channels_sorted[0]["name"]:
                            ch["timer"] = timer_name
                    if monitor is not None:
                        monitor_name = ch_fullname_to_name[monitor]
                        if monitor_name != ctrl_channels_sorted[0]["name"]:
                            ch["monitor"] = monitor_name
                    enabled = ch.get("enabled")
                    if enabled:
                        ch.pop("enabled")
                    output = ch.get("output")
                    if output:
                        ch.pop("output")
                    plot_type = ch.get("plot_type")
                    if plot_type == PlotType.No: 
                        ch.pop("plot_type")
                    plot_axes = ch.get("plot_axes")
                    if len(plot_axes) == 0:
                        ch.pop("plot_axes")
                    data_type = ch.get("data_type")
                    if data_type == "float64":
                        ch.pop("data_type")
                    data_units = ch.get("data_units")
                    if data_units == "":
                        ch.pop("data_units", None)
                    nexus_path = ch.get("nexus_path")
                    if nexus_path == "":
                        ch.pop("nexus_path")
                    ch.pop("name")
                    ch.pop("full_name")
                    ch.pop("source", None)
                    ch.pop("_controller_name")
                    # These are not used by sardana
                    ch.pop("normalization")
                    ch.pop("conditioning")
                    ch.pop("ndim", None)
                    channels_raw.append(ch)
            channels_raw = sorted(channels_raw, key=lambda ch: ch["index"])
            channels = []
            for ch in channels_raw:
                label = ch.pop("label")
                ch.pop("index")
                if ch:
                    channels.append({label:ch})
                else:
                    channels.append(label)
            label = configuration.get("label")
            if label != alias:
                config["label"] = label
            description = configuration.get("description")
            if (description is not None
                    and description != "General purpose measurement configuration"):
                config["description"] = description
        else:
            channels = mntgrp["properties"].get("elements", [])
        config["channels"] = channels
        
        yield alias, config


def get_device_name(current, server, inst):
    if current.lower() == f"{server}/{inst}/1".lower():
        # Using default name, no need to export it
        return None
    return current


def get_server_name(name, server_name, instance_name):
    if name != instance_name:
        return f"{server_name}/{instance_name}"
    if server_name != "Sardana":
        return server_name


def get_door(door):
    if get_property(door, "id"):
        raise RuntimeError(
            "Your installation contains numeric element IDs. The config"
            + " tool only works with setting USE_NUMERIC_ELEMENT_IDS=False."
            + " Furthermore your installation requires conversion."
        )
    return None


def build_sardana_config(config, ms_device_name):
    """
    Convert a dsconfig into a sardanoa config.
    Need to get a MacroServer device name.
    """
    ms_srv, ms_inst, ms_server, ms_device = find_device(config, "MacroServer", ms_device_name)
    pool_names = get_property(ms_device, "PoolNames", multiple=True)
    all_pools = CaselessDict(find_pools(config))
    pools = {}
    for name in pool_names:
        # Some complexity because techically the PoolNames property may contain
        # either device names or aliases, while we always want to refer to the
        # pools by alias.
        try:
            info = _, inst, *_ = all_pools[name.lower()]
        except KeyError as e:
            raise ValueError(f"Could not find pool {e} listed in MacroServer property PoolNames!")
        pools[inst] = info
    logger.debug(f"Found pools: {pools.keys()}")
    macro_servers = {
        ms_inst: (ms_srv, ms_inst, ms_server, ms_device_name, ms_device,)
    }

    return {
        "macro_servers": {
            ms_name: clean_dict({
                "tango_alias": (device["alias"]
                                if device["alias"].lower() != f"ms_{ms_inst}_1".lower()
                                else None),
                "tango_device": get_device_name(devname, "MacroServer", ms_name),
                "tango_server": get_server_name(ms_name, srvrname, instname),
                "python_path": get_property(device, "ClassPath", multiple=True),
                "macro_path": get_property(device, "MacroPath", multiple=True),
                "recorder_path": get_property(device, "RecorderPath", multiple=True),
                "doors": {
                    # TODO here we could check that the door does not have a numeric id property,
                    # if it does, exit and say the installation needs to be migrated.
                    door["alias"]: get_door(door)
                    for door in server["Door"].values()
                },
                "environment": {} or None,  # TODO
            })
            for ms_name, (srvrname, instname, server, devname, device)
            in macro_servers.items()
        },
        "pools": {
            # Use instance name as pool name; I think this is better since
            # it is more "readable" than the alias... and the alias is usually
            # generated anyway so it carries little meaning
            instname: clean_dict({
                "tango_alias": (device["alias"]
                                if device["alias"].lower() != f"pool_{instname}_1".lower()
                                else None),
                "tango_device": get_device_name(devname, "Pool", instname),
                "tango_server": get_server_name(poolname, srvrname, instname),
                "pool_path": get_property(device, "PoolPath", multiple=True),
                "python_path": get_property(device, "PythonPath", multiple=True),
                "measurement_groups": dict(sorted(find_measurement_groups(server))) or None,
                "instruments": dict(
                    build_instruments(get_property(device, "InstrumentList", multiple=True))
                ) or None,
                "controllers": dict(sort_controllers(find_controllers(server))),
            })
            for poolname, (srvrname, instname, server, devname, device) in pools.items()
        },
    }


if __name__ == "__main__":
    import sys
    import pydantic
    from ruamel.yaml import YAML

    from .validate import validate_config

    yaml = YAML(typ="rt")

    if len(sys.argv) == 3:
        with open(sys.argv[1]) as f:
            ds_config = json.load(f)
        sardana_config = build_sardana_config(ds_config, sys.argv[2])
    else:
        ds_config = json.load(sys.stdin)
        sardana_config = build_sardana_config(ds_config, sys.argv[1])
    try:
        validate_config(sardana_config)
    except pydantic.ValidationError as e:
        sys.exit(f"Output YAML config invalid! This is a bug!\n{e}")

    yaml.dump(sardana_config, sys.stdout, sort_keys=False)
