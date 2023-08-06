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

from copy import deepcopy

from ..diff import make_diff
from ..common import channel_defaults, remove_defaults


def test_diff__basic(sar_demo_yaml):
    pool, ms = make_diff(sar_demo_yaml, sar_demo_yaml)
    assert not pool
    assert not ms


def test_diff__ms_rename_door(sar_demo_yaml):
    modified = deepcopy(sar_demo_yaml)
    del modified["macro_servers"]["demo1"]["doors"]["Door_demo1_1"]
    modified["macro_servers"]["demo1"]["doors"]["My_new_door"] = {}
    pool, ms = make_diff(sar_demo_yaml, modified)
    changes = ms["demo1"]
    change1, change2 = changes
    assert "REMOVE" in change1
    assert "Door_demo1_1" in change1
    assert "ADD" in change2
    assert "My_new_door" in change2


def test_diff__pool_change_instrument(sar_demo_yaml):
    modified = deepcopy(sar_demo_yaml)
    ctrl = modified["pools"]["demo1"]["controllers"]["motctrl01"]
    ctrl["elements"]["mot02"]["instrument"] = "/mirror"
    pool, ms = make_diff(sar_demo_yaml, modified)
    assert not ms
    changes = pool["demo1"]
    assert len(changes) == 1
    change = changes[0]
    assert "REPLACE" in change
    assert "/mirror" in change


def test_diff__pool_add_controller(sar_demo_yaml):
    modified = deepcopy(sar_demo_yaml)
    ctrl = modified["pools"]["demo1"]["controllers"]["motctrl01"]
    ctrl["elements"]["mot05"] = {"axis": 5}
    pool, ms = make_diff(sar_demo_yaml, modified)
    assert not ms
    changes = pool["demo1"]
    assert len(changes) == 1
    change = changes[0]
    assert "ADD" in change
    assert "mot05" in change


def test_diff__pool_remove_element(sar_demo_yaml):
    modified = deepcopy(sar_demo_yaml)
    del modified["pools"]["demo1"]["controllers"]["motctrl01"]
    pool, ms = make_diff(sar_demo_yaml, modified)
    assert not ms
    changes = pool["demo1"]
    assert len(changes) == 1
    change = changes[0]
    assert "REMOVE" in change
    assert "motctrl01" in change


def test_diff__pool_renamed_element(sar_demo_yaml):
    modified = deepcopy(sar_demo_yaml)
    ctrl = modified["pools"]["demo1"]["controllers"].pop("motctrl01")
    modified["pools"]["demo1"]["controllers"]["renamed_ctrl"] = ctrl
    pool, ms = make_diff(sar_demo_yaml, modified)
    assert not ms
    changes = pool["demo1"]
    assert len(changes) == 1
    change = changes[0]
    assert "MOVE" in change
    assert "renamed_ctrl" in change


def test_diff__pool_mntgrp_defaults(sar_demo_yaml):
    modified = deepcopy(sar_demo_yaml)
    modified["pools"]["demo1"]["measurement_groups"]["mntgrp01"]["channels"][0] = \
        {"ct01": channel_defaults}
    pool, ms = make_diff(sar_demo_yaml, remove_defaults(modified))
    assert not pool
    assert not ms
    

