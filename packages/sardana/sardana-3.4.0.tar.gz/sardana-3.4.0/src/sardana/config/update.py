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

import sys

import click
from jsonpatch import make_patch, apply_patch
from ruamel.yaml import YAML
import yaml

from .validate import sanity_check_config


def update_config(original_yaml, updated_config):
    """
    Apply a patch to a YAML file, preserving the original structure
    as far as possible
    """

    # Load only logical content
    original_config = yaml.load(original_yaml, Loader=yaml.Loader)
    try:
        sanity_check_config(original_config)
    except RuntimeError as e:
        sys.exit(f"Original config is not valid: {e}")

    try:
        sanity_check_config(updated_config)
    except RuntimeError as e:
        sys.exit(f"Updated config is not valid: {e}")

    patch = make_patch(original_config, updated_config)

    # Load original again but keeping comments and ordering
    ruaml_yaml = YAML(typ="rt")
    original = ruaml_yaml.load(original_yaml)
    apply_patch(original, patch, in_place=True)
    return original


@click.argument("original_yaml", type=click.File("r"), required=True)
@click.argument("new_yaml", type=click.File("r"), required=True)
def update_cmd(original_yaml, new_yaml):
    """
    Update configuration, maintaining order and comments.
    Takes two YAML config files; "original" and "new". This script will then
    apply the changes from the new config to the original, while keeping as
    much as possible of the original structure intact. This includes the order
    of things, comments, etc.

    The updated configuration is logically identical to the "new" one, but
    should be more friendly to e.g. storage in git.

    The resulting new YAML content is printed to stdout.
    """
    merged = update_config(original_yaml.read(),
                           yaml.load(new_yaml, Loader=yaml.Loader))
    ruamel = YAML(typ="rt")
    ruamel.dump(merged, sys.stdout)


def main():
    cmd = click.command("merge")(update_cmd)
    return cmd()


if __name__ == "__main__":
    main()
