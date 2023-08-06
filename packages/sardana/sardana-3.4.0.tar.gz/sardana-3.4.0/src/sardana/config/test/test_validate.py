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

from ..validate import sanity_check_config


def test_sanity_check_config__basic(sar_demo_yaml):
    sanity_check_config(sar_demo_yaml)


def test_sanity_check_config__bad_channel(sar_demo_yaml):
    sar_demo_yaml["pools"]["demo1"]["measurement_groups"]["mntgrp01"]["channels"][2] = "ct03_wrong"
    with pytest.raises(RuntimeError) as exc_info:
        sanity_check_config(sar_demo_yaml)
    assert "ct03_wrong" in str(exc_info.value)
