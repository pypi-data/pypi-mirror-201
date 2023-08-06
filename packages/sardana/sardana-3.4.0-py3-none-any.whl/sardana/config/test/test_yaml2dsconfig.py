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

import json

from ..yaml2dsconfig import build_dsconfig, build_measurement_group_devices


def test_build_dsconfig__basic(sar_demo_yaml, sar_demo_json):
    dsconfig = build_dsconfig(sar_demo_yaml)
    assert dsconfig == sar_demo_json


def test_build_dsconfig__attribute_config(sar_demo_yaml, sar_demo_json):
    sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]["mot03"] \
        ["attributes"] = {
            "TestAttribute": {
                "value": 67.5,
                "rel_change": 8,
                "archive_abs_change": [-3, 5],
                "label": "Bananas",
                "min_value": 782.3,
            }
        }

    dsconfig = build_dsconfig(sar_demo_yaml)

    # TODO once meas grps work, it's probably better to instead modify sar_demo_json
    # as expected, and compare. This way we can check that nothing else changed.
    attr_props = dsconfig["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/3"] \
        ["attribute_properties"]["TestAttribute"]
    assert attr_props["__value"] == ["67.5"]
    assert attr_props["rel_change"] == ["-8", "8"]
    assert attr_props["archive_abs_change"] == ["-3", "5"]
    assert attr_props["label"] == ["Bananas"]
    assert attr_props["min_value"] == ["782.3"]


def test_build_dsconfig__attribute_value(sar_demo_yaml, sar_demo_json):
    sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]["mot03"] \
        ["attributes"] = {
            "Simple": 983.1,
            "WithOtherStuff": {
                "value": 5,
                "rel_change": [-1, 5]
            }
        }

    dsconfig = build_dsconfig(sar_demo_yaml)

    attr_props = dsconfig["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/3"] \
        ["attribute_properties"]
    assert attr_props["Simple"]["__value"] == ["983.1"]
    assert attr_props["WithOtherStuff"]["__value"] == ["5"]
    assert attr_props["WithOtherStuff"]["rel_change"] == ["-1", "5"]


def test_build_dsconfig__polling(sar_demo_yaml, sar_demo_json):

    sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]["mot03"] \
        ["attributes"] = {
            "SomeCoolAttribute": {
                "polling_period": 5000
            }
        }

    dsconfig = build_dsconfig(sar_demo_yaml)

    assert dsconfig["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/3"]["properties"] \
        ["polled_attr"] == ["SomeCoolAttribute", "5000"]


def test_build_dsconfig__element_device_name(sar_demo_yaml, sar_demo_json):

    default_name = "motor/motctrl01/3"
    new_name = "my/TEST/name"

    # Check default name
    dsconfig = build_dsconfig(sar_demo_yaml)
    element = dsconfig["servers"]["Sardana"]["demo1"]["Motor"][default_name]

    sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]["mot03"] \
        ["tango_device"] = new_name

    dsconfig = build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    assert not dsconfig["servers"]["Sardana"]["demo1"]["Motor"].get(default_name)
    assert dsconfig["servers"]["Sardana"]["demo1"]["Motor"].get(new_name) == element


def test_build_dsconfig__controller_device_name(sar_demo_yaml, sar_demo_json):

    default_name = "controller/dummymotorcontroller/motctrl01"
    new_name = "ctrl/TEST/name"

    # Check default name
    dsconfig = build_dsconfig(sar_demo_yaml)
    controller = dsconfig["servers"]["Sardana"]["demo1"]["Controller"][default_name]

    sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"] \
        ["tango_device"] = new_name

    dsconfig = build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    assert default_name not in dsconfig["servers"]["Sardana"]["demo1"]["Controller"]
    assert dsconfig["servers"]["Sardana"]["demo1"]["Controller"].get(new_name) == controller


def test_build_dsconfig__pool_device_name(sar_demo_yaml, sar_demo_json):

    default_name = "Pool/demo1/1"
    new_name = "pool/BANANAS/7"

    # Check default name
    dsconfig = build_dsconfig(sar_demo_yaml)
    pool = dsconfig["servers"]["Sardana"]["demo1"]["Pool"][default_name]

    sar_demo_yaml["pools"]["demo1"]["tango_device"] = new_name

    dsconfig = build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    assert default_name not in dsconfig["servers"]["Sardana"]["demo1"]["Pool"]
    assert dsconfig["servers"]["Sardana"]["demo1"]["Pool"].get(new_name) == pool


def test_build_dsconfig__pool_server_name(sar_demo_yaml, sar_demo_json):

    default_name = "Sardana/test"
    new_name = "Pool/hello"

    # Check default name
    dsconfig = build_dsconfig(sar_demo_yaml)
    pool = dsconfig["servers"]["Sardana"]["demo1"]["Pool"]["Pool/demo1/1"]

    sar_demo_yaml["pools"]["demo1"]["tango_server"] = new_name

    dsconfig = build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    def_srv, def_inst = default_name.split("/")
    assert def_inst not in dsconfig["servers"]
    new_srv, new_inst = new_name.split("/")
    assert dsconfig["servers"][new_srv][new_inst]["Pool"]["Pool/demo1/1"] == pool


def test_build_dsconfig__ms_device_name(sar_demo_yaml, sar_demo_json):

    default_name = "MacroServer/demo1/1"
    new_name = "ms/BANANAS/7"

    # Check default name
    dsconfig = build_dsconfig(sar_demo_yaml)
    ms = dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"][default_name]

    sar_demo_yaml["macro_servers"]["demo1"]["tango_device"] = new_name

    dsconfig = build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    ms_devices = dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]
    assert ms_devices[new_name] == ms
    assert default_name not in ms_devices


def test_build_dsconfig__ms_server_name(sar_demo_yaml, sar_demo_json):

    default_name = "Sardana/test"
    new_name = "MacroServer/hello"

    # Check default name
    dsconfig = build_dsconfig(sar_demo_yaml)
    ms = dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]

    sar_demo_yaml["macro_servers"]["demo1"]["tango_server"] = new_name

    dsconfig = build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    def_srv, def_inst = default_name.split("/")
    assert def_inst not in dsconfig["servers"]
    new_srv, new_inst = new_name.split("/")
    assert dsconfig["servers"][new_srv][new_inst]["MacroServer"]["MacroServer/demo1/1"] == ms


def test_build_dsconfig__controller_properties(sar_demo_yaml, sar_demo_json):

    controller = sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"]
    controller["properties"] = {
        "OneLiner": "I'll be back",
        "SeveralLines": ["a", "longer", "one"]
    }

    dsconfig = build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    ctrl_name = "controller/dummymotorcontroller/motctrl01"
    print(dsconfig["servers"]["Sardana"]["demo1"]["Controller"])
    ctrl_props = dsconfig["servers"]["Sardana"]["demo1"]["Controller"][ctrl_name]["properties"]
    assert ctrl_props["OneLiner"] == ["I'll be back"]
    assert ctrl_props["SeveralLines"] == ["a", "longer", "one"]


def test_build_dsconfig__pool_names(sar_demo_yaml):
    sar_demo_yaml["macro_servers"]["demo1"]["pools"] = ["demo1", "abc"]

    dsconfig = build_dsconfig(sar_demo_yaml)

    ms = dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]
    assert ms["properties"]["PoolNames"] == ["Pool_demo1_1", "abc"]


# TODO test physical_roles
