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

from dsconfig.json2tango import apply_config
import tango
from yaml import load, Loader

from ..dump import dump_cmd
from ..dsconfig2yaml import build_sardana_config


def test_dump_cmd(sar_demo_json_unique, capsys):
    """
    Basic test that configures a sar_demo environment in the Tango DB,
    then dumps it back out and checks that we get the same thing back.
    """
    db = tango.Database()
    name, config = sar_demo_json_unique
    apply_config(config, db, write=True)

    ms_device = f"MacroServer/{name}/1"
    dump_cmd(ms_device)
    captured = capsys.readouterr()
    yaml_config = load(captured.out, Loader=Loader)

    assert yaml_config == build_sardana_config(config, ms_device)

    db.delete_server(f"Sardana/{name}")
