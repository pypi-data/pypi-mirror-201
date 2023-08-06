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
import pydantic

import click
from ruamel.yaml import YAML

from .check import check_config
from .model import Configuration


def sanity_check_config(sardana_config, check_code=False):
    "Do some checks to be (pretty) sure the configuration makes sense"

    # Check file format
    try:
        Configuration(**sardana_config)
    except pydantic.ValidationError as e:
        raise RuntimeError(f"Input YAML format invalid!\n{e}")

    # Check internal consistency
    errors = list(check_config(sardana_config, check_code))
    if errors:

        def format_path(path):
            "Note that the path may contain strings and integers (indexes)"
            return " -> ".join(map(str, path))

        error_str = "\n".join(
            f"{format_path(path)}:\n  {error}"
            for path, error in errors
        )
        raise RuntimeError(f"Configuration contains errors!\n{error_str}")


@click.argument("config_file", type=click.File("r"))
@click.option("--check-code", is_flag=True, help="Enable loading controller source code")
def validate_cmd(config_file, check_code):
    """
    Check the given YAML sardana config file for errors.

    "--check-code" enables more advanced checks against controller code.
    This requres that the script runs in an environment where the
    configuration will be used, so that relevant code can be imported and
    inspected.
    """
    # TODO handle YAML loading errors nicely
    yaml = YAML(typ="rt")
    sardana_config = yaml.load(config_file)
    try:
        sanity_check_config(sardana_config, check_code)
    except RuntimeError as e:
        sys.exit(f"Error: {e}")


def main():
    cmd = click.command("validate")(validate_cmd)
    return cmd()


if __name__ == "__main__":
    main()
