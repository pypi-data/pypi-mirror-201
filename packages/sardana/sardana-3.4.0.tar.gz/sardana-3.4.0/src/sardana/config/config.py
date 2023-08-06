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
Entry point for the "sardana config" command
"""

import logging

import click
import yaml

from .load import load_cmd
from .dump import dump_cmd
from .validate import validate_cmd
from .diff import diff_cmd
from .update import update_cmd


def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')


# Change the default representation of None/null to nothing
yaml.add_representer(type(None), represent_none)


@click.group("config")
@click.option("--debug", "-d", is_flag=True, default=False)
def config_grp(debug):
    """
    This command groups the various configuration actions available.
    In general, filename arguments may be replaced with "-" in order
    to read from stdin. Any YAML output is written to stdout.
    """
    if debug:
        # TODO I think this comes too late to have an effect..?
        logging.basicConfig(level=logging.DEBUG)


config_grp.command("load")(load_cmd)
config_grp.command("dump")(dump_cmd)
config_grp.command("validate")(validate_cmd)
config_grp.command("diff")(diff_cmd)
config_grp.command("update")(update_cmd)
