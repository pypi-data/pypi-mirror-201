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
import os
import sys
from pathlib import Path
from uuid import uuid4

from pytest import fixture
import yaml

if sys.version_info < (3, 7):
    # For now, the config scripts are not compatible with older
    # python versions. Since we still need to test sardana on
    # python 3.5, we exclude these tests from the suite.
    collect_ignore_glob = ["*.py"]


@fixture
def tango_host():
    """Set the TANGO_HOST environment variable"""
    original_tango_host = os.environ.get("TANGO_HOST")
    TANGO_HOST = "some.test.host:10000"
    os.environ["TANGO_HOST"] = TANGO_HOST
    yield TANGO_HOST
    if original_tango_host:
        os.environ["TANGO_HOST"] = original_tango_host
    else:
        del os.environ["TANGO_HOST"]


@fixture
def sar_demo_json():
    with open(Path(__file__).parent / "sar_demo.json") as f:
        return json.load(f)


@fixture
def sar_demo_json_unique():
    unique_name = "test" + str(uuid4()).replace("-", "")
    with open(Path(__file__).parent / "sar_demo_template.json") as f:
        config = f.read()
        return unique_name, json.loads(config.replace("{name}", unique_name))


@fixture
def sar_demo_yaml():
    with open(Path(__file__).parent / "sar_demo.yaml") as f:
        return yaml.load(f, Loader=yaml.Loader)
