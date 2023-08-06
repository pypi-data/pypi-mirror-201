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

import pytest

from ..check import check_config


def test_check_config__basic(sar_demo_yaml):
    errors = list(check_config(sar_demo_yaml))
    assert not errors


def set_path(path, config, value):
    for step in path[:-1]:
        config = config[step]
    config[path[-1]] = value


def test_check_config__bad_controller_module(sar_demo_yaml):
    bad_controller_module = "NonExistingController123.py"
    path = ["pools", "demo1", "controllers", "motctrl01"]
    set_path([*path, "python_module"], sar_demo_yaml, bad_controller_module)

    errors = check_config(sar_demo_yaml, load_code=True)

    (pos, message), = list(errors)
    assert pos == path
    assert bad_controller_module in message


def test_check_config__bad_controller_class(sar_demo_yaml):
    bad_controller_class = "NonExistingControllerClass"
    path = ["pools", "demo1", "controllers", "motctrl01"]
    set_path([*path, "python_class"], sar_demo_yaml, bad_controller_class)

    errors = check_config(sar_demo_yaml, load_code=True)

    (pos, message), = list(errors)
    assert pos == path
    assert bad_controller_class in message


def test_check_config__missing_instrument(sar_demo_yaml):
    bad_instrument = "/badinstrument123"
    path = ["pools", "demo1", "controllers", "motctrl01", "elements", "mot02", "instrument"]
    set_path(path, sar_demo_yaml, bad_instrument)

    errors = check_config(sar_demo_yaml)
    (pos, message), = list(errors)
    assert pos == path
    assert bad_instrument in message


def test_check_config__bad_physical_role(sar_demo_yaml):
    bad_role = "abc123"
    path = ["pools", "demo1", "controllers", "slitctrl01", "physical_roles", bad_role]
    set_path(path, sar_demo_yaml, "something")

    errors = check_config(sar_demo_yaml)

    (pos, message), = list(errors)
    assert pos == path
    assert bad_role in message


def test_check_config__bad_physical_role_element(sar_demo_yaml):
    bad_phys_role = "abc123"
    path = ["pools", "demo1", "controllers", "slitctrl01", "physical_roles", "sl2t"]
    set_path(path, sar_demo_yaml, bad_phys_role)

    errors = check_config(sar_demo_yaml)

    (pos, message), = list(errors)
    assert pos == path
    assert bad_phys_role in message


def test_check_config__missing_pseudo_role(sar_demo_yaml):
    path = ["pools", "demo1", "controllers", "slitctrl01", "elements"]

    del sar_demo_yaml["pools"]["demo1"]["controllers"]["slitctrl01"]["elements"]["gap01"]

    errors = list(check_config(sar_demo_yaml))

    pos, message = errors[0]
    assert pos == path
    assert "Gap" in message


def test_check_config__bad_pseudo_role_axis(sar_demo_yaml):
    bad_axis = 42
    path = ["pools", "demo1", "controllers", "slitctrl01", "elements", "gap01"]
    set_path(path, sar_demo_yaml, {"axis": bad_axis})

    errors = list(check_config(sar_demo_yaml))

    # Expect message about bad axis
    pos, message = errors[0]
    assert pos == path
    assert str(bad_axis) in message

    # Also expect a message about missing role
    pos, message = errors[1]
    assert pos == path[:-1]
    assert "Gap" in message


def test_check_config__bad_meas_grp_channel(sar_demo_yaml):
    bad_channel = "baaaaaad123"
    path = ["pools", "demo1", "measurement_groups", "mntgrp01", "channels", 2]
    set_path(path, sar_demo_yaml, bad_channel)

    errors = list(check_config(sar_demo_yaml))

    # Expect message about bad axis
    pos, message = errors[0]
    assert pos == path
    assert str(bad_channel) in message
