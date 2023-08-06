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
This script takes a YAML sardana config file and turns it into
a dsconfig compatible JSON string. Applying this with json2tango
should provide a corresponding configuration in the Tango db.
"""

from collections import ChainMap
from collections.abc import Sequence, Mapping
import logging
import json

import tango
from sardana.pool import AcqSynchType
from sardana.pool.pool import ElementType, TYPE_MAP_OBJ

from .common import clean_dict, get_full_name


logger = logging.getLogger(__name__)


# Some helper functions

def get_ctrls_by_type(ctrls, type_):
    for name, ctrl in ctrls.items():
        if ctrl["type"] == type_:
            yield name, ctrl


def get_tango_host(config):
    return config.get("tango_host", tango.ApiUtil.get_env_var("TANGO_HOST"))


def format_attr_prop(name, value):
    """
    Make sure attribute settings are in proper format for being stored
    as properties in the DB.
    """
    if name == "value":
        return "__value", ensure_list(value)
    elif name in {"abs_change",
                  "rel_change",
                  "archive_abs_change",
                  "archive_rel_change"}:
        if isinstance(value, Sequence):
            return name, [str(value[0]), str(value[1])]
        else:
            return name, [str(-value), str(value)]
    else:
        return name, [str(value)]
    return name


# Official tango attribute properties (are there any other?)
ATTR_CONFIG_PROPS = [
    "label",
    "format",
    "unit",
    "polling_period",
    "abs_change",
    "rel_change",
    "archive_abs_change",
    "archive_rel_change",
    "min_value",
    "max_value",
    "min_alarm",
    "max_alarm",
    "value"
]


def build_attr_props(props):
    if isinstance(props, Mapping):
        return dict(
            format_attr_prop(name, value)
            for name, value in props.items()
            if name in ATTR_CONFIG_PROPS
        )
    return {
        "__value": ensure_list(props)
    }


def stringify(value):
    """If the value is not already a string, turn it into one"""
    if isinstance(value, str):
        if value in {"true", "false"}:
            # This is bad because it will be interpreted as a boolean by json.loads().
            # That breaks the "roundtripping" idea.
            # TODO any other ambiguous cases?
            logger.warning(
                "'{value}' string detected, will be converted to bool when loading back.")
        return value
    # TODO test with all possible types
    return json.dumps(value)


def ensure_list(value):
    "Dsconfig expects properties to be described as lists of strings"
    if isinstance(value, (list, tuple)):
        return [stringify(v) for v in value]
    return [stringify(value)]


def build_props(**props):
    "Return properly formated properties (and exclude empty ones)"
    return {
        name: ensure_list(value)
        for name, value in props.items()
        if value is not None
    } or None


def get_controller_props(ctrl):
    if ctrl["type"] in ("PseudoMotor", "PseudoCounter"):
        physical_roles = []
        for role, mot_name in ctrl.get("physical_roles", {}).items():
            physical_roles.extend((role, mot_name))
        if physical_roles:
            return {
                "physical_roles": physical_roles
            }
    return {}


def get_element_ctrl(config, element):
    for pool in config["pools"].values():
        for name, ctrl in pool["controllers"].items():
            if element in ctrl.get("elements", {}):
                return name, ctrl
    raise KeyError(f"Could not find element {element}")


def get_elements(config):
    """Return a mapping of element name to element and controller info"""
    elements = {}
    for _, pool in config.get("pools", {}).items():
        for ctrl_name, ctrl in pool.get("controllers", {}).items():
            # ctrls[ctrl_name.lower()] = ctrl
            for el_name, element in ctrl.get("elements", {}).items():
                elements[el_name.lower()] = (element, ctrl_name, ctrl)
    return elements


def get_channels_by_ctrl(config, mntgrp):
    controllers = {}
    elements = get_elements(config)
    for idx, channel in enumerate(mntgrp["channels"]):
        if isinstance(channel, str):
            ch_name = channel
            channel = {}
        else:
            ch_name = list(channel.keys())[0]
            channel = list(channel.values())[0]
        try:
            ctrl_name, ctrl_info = get_element_ctrl(config, ch_name)
        except KeyError as e:
            if "/" in ch_name:
                ctrl_name = "__tango__"
                ctrl_info = None
            else:
                raise e

        tango_host = get_tango_host(config)
        if ctrl_info is not None:
            ctrl_device = get_controller_device_name(ctrl_name, ctrl_info)
            ctrl_full_name = get_full_name(ctrl_device, tango_host)
        else:
            ctrl_full_name = "__tango__"
        ctrl_conf = controllers.get(ctrl_full_name)

        if ctrl_conf is None:
            # New controller
            ctrl_conf = {
                "channels": {}
            }
            if ctrl_full_name != "__tango__":
                timer = channel.get("timer", ch_name)
                timer_element, timer_ctrl_name, timer_ctrl = elements[timer]
                timer_device_name = get_element_device_name(
                    timer_ctrl["type"], timer, timer_element, timer_ctrl_name, timer_ctrl)
                timer_full_name = get_full_name(timer_device_name, tango_host)

                monitor = channel.get("monitor", ch_name)
                monitor_element, monitor_ctrl_name, monitor_ctrl = elements[monitor]
                monitor_device_name = get_element_device_name(
                    monitor_ctrl["type"], monitor, monitor_element, monitor_ctrl_name, monitor_ctrl)
                monitor_full_name = get_full_name(monitor_device_name, tango_host)

                synchronizer = channel.get("synchronizer", "software")
                if synchronizer == "software":
                    synchronizer_full_name = synchronizer
                else:
                    synchronizer_element, synchronizer_ctrl_name, synchronizer_ctrl = elements[synchronizer]
                    synchronizer_device_name = get_element_device_name(
                    synchronizer_ctrl["type"], synchronizer, synchronizer_element, synchronizer_ctrl_name, synchronizer_ctrl)
                    synchronizer_full_name = get_full_name(synchronizer_device_name, tango_host)
                ctrl_conf["synchronizer"] = synchronizer_full_name
                ctrl_conf["synchronization"] = AcqSynchType.get(channel.get("synchronization", "Trigger"))
                ctrl_conf["timer"] = timer_full_name
                ctrl_conf["monitor"] = monitor_full_name                
            controllers[ctrl_full_name] = ctrl_conf

        if ctrl_full_name == "__tango__":
            name = ch_name.split("/")[-1]
            ch_fullname = get_full_name(ch_name, tango_host)
        else:
            name = ch_name
            channel_element, _, _ = elements[ch_name]
            ch_device_name = get_element_device_name(
                ctrl_info["type"], ch_name, channel_element, ctrl_name, ctrl_info)
            ch_fullname = get_full_name(ch_device_name, tango_host)
        ctrl_conf["channels"][ch_fullname] = {
            "name": name,
            "label": ch_name,
            "full_name": ch_fullname,
            "enabled": channel.get("enabled", True),
            "output": channel.get("output", True),
            "data_type": channel.get("data_type", "float64"),
            "data_units": channel.get("data_units", ""),
            "conditioning": "",
            "normalization": 0,
            "nexus_path": channel.get("nexus_path", ""),
            "plot_type": 0,
            "plot_axes": [],
            "_controller_name": ctrl_full_name,
            "index": idx,
        }
    return controllers


"""
Example measurement group:
{
    "controllers": {
        "tango://w-johfor-pc-0:10000/controller/dummyonedcontroller/onedctrl02": {
            "synchronizer": "software",
            "synchronization": 0,
            "channels": {
                "tango://w-johfor-pc-0:10000/expchan/onedctrl02/1": {
                    "name": "oned02",
                    "label": "oned02",
                    "full_name": "tango://w-johfor-pc-0:10000/expchan/onedctrl02/1",
                    "enabled": true,
                    "output": true,
                    "data_type": "float64",
                    "data_units": "",
                    "conditioning": "",
                    "normalization": 0,
                    "nexus_path": "",
                    "plot_type": 0,
                    "plot_axes": [],
                    "_controller_name": "tango://w-johfor-pc-0:10000/controller/dummyonedcontroller/onedctrl02",
                    "index": 0,
                    "ndim": 1
                }
            },
            "timer": "tango://w-johfor-pc-0:10000/expchan/onedctrl02/1",
            "monitor": "tango://w-johfor-pc-0:10000/expchan/onedctrl02/1"
        },
        "__tango__": {
            "channels": {
                "tango://w-johfor-pc-0.maxiv.lu.se:10000/sys/tg_test/1/boolean_scalar": {
                    "name": "boolean_scalar",
                    "label": "sys/tg_test/1/boolean_scalar",
                    "full_name": "tango://w-johfor-pc-0.maxiv.lu.se:10000/sys/tg_test/1/boolean_scalar",
                    "enabled": true,
                    "output": true,
                    "data_type": "bool8",
                    "data_units": "",
                    "conditioning": "",
                    "normalization": 0,
                    "nexus_path": "",
                    "plot_type": 0,
                    "plot_axes": [],
                    "_controller_name": "__tango__",
                    "index": 1,
                    "ndim": null
                }
            }
        }
    },
    "label": "fiskelifisk2",
    "description": "General purpose measurement configuration",
    "timer": "tango://w-johfor-pc-0:10000/expchan/onedctrl02/1",
    "monitor": "tango://w-johfor-pc-0:10000/expchan/onedctrl02/1"
}
"""


def build_mntgrp_config(config, mntgrp, name):
    mntgrp_config = {
        "controllers": get_channels_by_ctrl(config, mntgrp),
        "label": name,
    }
    description = mntgrp.get("description")
    if description is None:
        description = "General purpose measurement configuration"
    mntgrp_config["description"] = description
    return json.dumps(mntgrp_config)


def get_element_device_name(el_type, el_name, el_info, ctrl_name, ctrl):
    # Allow specifying device name
    tmpl = el_info.get("tango_device")
    if tmpl:
        device_name = tmpl.format(type=el_type, name=el_name, ctrl=ctrl_name, axis=el_info["axis"])
    else:
        # Otherwise use the default sardana naming schema
        type_data = TYPE_MAP_OBJ[ElementType[el_type]]
        device_name = type_data.auto_full_name.format(ctrl_name=ctrl_name, **el_info)
    return device_name


def get_device_name(default, name, info):
    base = info.get("tango_device")
    if base:
        device_name = base.format(name=name, **info)
    else:
        device_name = default.format(name=name, **info)
    return device_name


def get_polled_attr(device):
    polled_attr = []
    attributes = device.get("attributes", {})
    for name, config in attributes.items():
        if isinstance(config, Mapping):
            polling_period = config.get("polling_period")
            if polling_period:
                polled_attr.extend([name, str(polling_period)])
    return polled_attr or None


def get_pool_alias(pool_name, pool):
    return pool.get("alias", f"Pool_{pool_name}_1")


def build_pool_device(pool_name, pool):
    return {
        get_device_name("Pool/{name}/1", pool_name, pool):
        clean_dict({
            "alias": get_pool_alias(pool_name, pool),
            "properties": build_props(
                PoolPath=pool.get("pool_path"),
                PythonPath=pool.get("python_path"),
                InstrumentList=sum(
                    [
                        [
                            instr["class"],
                            instr_name,
                        ]
                        for instr_name, instr
                        in pool.get("instruments", {}).items()
                    ], []
                ) or None
            ),
        })
    }


def get_controller_device_name(ctrl_name, ctrl_info):
    # TODO also use TYPE_MAP_OBJ for the template
    return get_device_name(
        "controller/{lower_class}/{name}",
        ctrl_name,
        {
            **ctrl_info,
            "lower_class": ctrl_info["python_class"].lower()  # Note lowercaseing here, for sardana compat
        })


def build_controller_devices(pool_info):
    return {
        get_controller_device_name(ctrl_name, ctrl): clean_dict({
            "alias": ctrl_name,
            "properties": build_props(
                type=ctrl["type"],
                klass=ctrl["python_class"],
                library=ctrl.get("python_module"),
                # Properties special for some controller types
                **get_controller_props(ctrl),
                # Extra properties, e.g. for settings
                **{
                    prop: ensure_list(value)
                    for prop, value in ctrl.get("properties", {}).items()
                }
            ),
            "attribute_properties": clean_dict({
                attr_name: build_props(**build_attr_props(props))
                for attr_name, props
                in ctrl.get("attributes", {}).items()
            }) or None,
        })
        for ctrl_name, ctrl in pool_info.get("controllers", {}).items()
    }


def build_controller_element_devices(pool):
    return {
        el_type: dict(ChainMap(*(
            {
                get_element_device_name(el_type, el_name, el, ctrl_name, ctrl):
                clean_dict({
                    "alias": el_name,
                    "properties": build_props(
                        axis=el["axis"],
                        ctrl_id=ctrl_name,
                        Instrument_id=el.get("instrument"),
                        DriftCorrection=el.get("drift_correction"),
                        polled_attr=get_polled_attr(el),
                    ) or None,
                    "attribute_properties": clean_dict({
                        attr_name: build_props(**build_attr_props(props))
                        for attr_name, props
                        in el.get("attributes", {}).items()
                    }) or None,
                })
                for el_name, el in ctrl["elements"].items()
            }
            for ctrl_name, ctrl
            in get_ctrls_by_type(pool["controllers"], el_type)
        )))
        for el_type in [
            "Motor",
            "PseudoMotor",
            "ZeroDExpChannel",
            "OneDExpChannel",
            "TwoDExpChannel",
            "TriggerGate",
            "PseudoCounter",
            "CTExpChannel",
            "IORegister",
            # ...?
        ]
        if list(get_ctrls_by_type(pool["controllers"], el_type))
    }


def build_measurement_group_devices(pool_name, pool_info, config):
    pool_alias = get_pool_alias(pool_name, pool_info)
    devices = {}
    for i, (mntgrp_name, mntgrp) in enumerate(pool_info.get("measurement_groups", {}).items(), start=1):
        device_name = f"mntgrp/{pool_alias.lower()}/{mntgrp_name}"
        elements = []
        synchronizers = []
        basic_config = True
        for chn in mntgrp.get("channels", []):
            if isinstance(chn, dict):
                synchronizer = list(chn.values())[0].get("synchronizer", "software")
                if synchronizer != "software":
                    synchronizers.append(synchronizer)
                chn = list(chn.keys())[0]                
                basic_config = False                    
            elements.append(chn)
        elements.extend(synchronizers)
        device_config = clean_dict({
            "alias": mntgrp_name,
            "properties": build_props(
                elements=elements
            )})
        if not basic_config:
            device_config["attribute_properties"] = {
                "Configuration": build_props(
                    __value=build_mntgrp_config(config, mntgrp, mntgrp_name))
            }
        devices[device_name] = device_config
    return devices


def build_macro_server_device(ms_name, ms_info, config):
    pools = ms_info.get("pools")
    if pools:
        pool_names = []
        for pool_name in pools:
            # Here we allow referring to pools by name
            pool = config["pools"].get(pool_name)
            if pool:
                pool_alias = get_pool_alias(pool_name, pool)
                pool_names.append(pool_alias)
            else:
                # It's also legal to refer to pools outside of the config.
                pool_names.append(pool_name)
    else:
        # If the "pools" key is not set, we just put in all the
        # pools in the config. This should cover the most common cases.
        pool_names = [
            get_pool_alias(pool_name, pool)
            for pool_name, pool in config.get("pools", {}).items()
        ]
    return {
        get_device_name("MacroServer/{name}/1", ms_name, ms_info):
        clean_dict({
            "alias": ms_info.get("alias") or f"MS_{ms_name}_1",
            "properties": build_props(
                EnvironmentDb=ms_info.get("environment", {}).get("path"),
                PoolNames=pool_names,
                RecorderPath=ms_info.get("recorder_path"),
                MacroPath=ms_info.get("macro_path"),
            )
            # TODO what to do with env vars...
        })
    }


def build_door_devices(ms_name, ms_info):
    return {
        door_name.replace("_", "/"): clean_dict({
            "alias": door_name,
            "properties": build_props()
        })
        for door_name, door in ms_info.get("doors", {}).items()
    }


def build_dsconfig(config):
    """
    Convert a sardana config into a dsconfig one
    """

    servers = {}

    # Collect pools/ms into Tango servers
    for pool_name, pool in config["pools"].items():
        server = pool.get("tango_server")
        if server:
            if "/" in server:
                # User specified full server name
                srv, inst = server.split("/")
                assert srv in {"Pool", "Sardana"}, f"Bad Pool server name {server}"
                servers.setdefault(srv, []).append((inst, pool_name, "Pool", pool))
            else:
                # User specified only server name (must be Pool!)
                assert server in {"Pool", "Sardana"}, f"Bad Pool server name {server}"
                servers.setdefault(server, []).append((pool_name, pool_name,"Pool", pool))
        else:
            # Run in default server (Sardana)
            servers.setdefault("Sardana", []).append((pool_name, pool_name, "Pool", pool))

    for ms_name, ms in config["macro_servers"].items():
        server = ms.get("tango_server")
        if server:
            if "/" in server:
                # User specified full server name
                srv, inst = server.split("/")
                assert srv in {"MacroServer", "Sardana"}, f"Bad MS server name {server}"
                servers.setdefault(srv, []).append((inst, ms_name, "MacroServer", ms))
            else:
                # User specified only server name
                assert server in {"MacroServer", "Sardana"}, f"Bad MS server name {server}"
                servers.setdefault(server, []).append((ms_name, ms_name, "MacroServer", ms))
        else:
            # Run in default server (Sardana)
            servers.setdefault("Sardana", []).append((ms_name, ms_name, "MacroServer", ms))

    dsconfig = {
        "servers": {

        }
    }
    for server_type, instances in servers.items():
        server = dsconfig["servers"].setdefault(server_type, {})
        for inst, name, config_type, info in instances:
            instance = server.setdefault(inst, {})
            if config_type == "Pool":
                instance.update({
                    # Pool
                    "Pool": build_pool_device(name, info),
                    "Controller": build_controller_devices(info),
                    **build_controller_element_devices(info),
                    "MeasurementGroup": build_measurement_group_devices(name, info, config),
                })
            elif config_type == "MacroServer":
                instance.update({
                    "MacroServer": build_macro_server_device(name, info, config),
                    "Door": build_door_devices(name, info),
                })
    return dsconfig


if __name__ == "__main__":
    import sys

    import pydantic
    from ruamel.yaml import YAML

    from .validate import validate_config

    # Ruamel is a YAML loader/dumper that keeps order and comments intact
    # We need this in order for things to be consistent.
    yaml = YAML(typ="rt")  # "Roundtrip" setting

    if (len(sys.argv) > 1):
        with open(sys.argv[1]) as f:
            sardana_config = yaml.load(f)
    else:
        sardana_config = yaml.load(sys.stdin)
    #
    try:
        validate_config(sardana_config)
    except pydantic.ValidationError as e:
        sys.exit(f"Input YAML config invalid!\n{e}")
    dsconfig = build_dsconfig(sardana_config)
    print(json.dumps(dsconfig, indent=4, sort_keys=True))
