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
Very basic diffing functionality for sardana YAML config files.

The point compared to regular "diff" is we don't care about
things like dict ordering, only structure. Since we know about
the structure, we could improve the output further to make it more
user friendly.

TODO allow outputting computer friendly format e.g. JSON
"""

from textwrap import indent

import click
from jsonpatch import make_patch
from jsonpointer import resolve_pointer
from yaml import load, Loader, dump
from .common import remove_defaults


def make_diff(original, new):
    patch = make_patch(original, new)
    pool_changes = {}
    ms_changes = {}
    for line in patch:
        path = line["path"].split("/")
        if path[1] == "pools":
            pool_changes.setdefault(path[2], []).append(line)
        elif path[1] == "macro_servers":
            ms_changes.setdefault(path[2], []).append(line)
    return {
        pool: list(format_changes(original, changes))
        for pool, changes in pool_changes.items()
    }, {
        ms: list(format_changes(original, changes))
        for ms, changes in ms_changes.items()
    }


def format_changes(original, changes):
    for line in changes:
        op = line["op"]
        if op == "move":
            # Don't care about changes only in casing
            if line["from"].lower() != line["path"].lower():
                yield "- MOVE {from}\n    to {path}".format(**line)
        elif op == "remove":
            yield "- REMOVE {path}".format(**line)
        elif op == "add":
            yield ("- ADD {path}\n".format(**line)
                   + indent(dump(line["value"]), " " * 4))
        elif op == "replace":
            path = line["path"]
            value = line["value"]
            old_value = resolve_pointer(original, path)
            yield f"- REPLACE {path} {old_value} => {value}"
        else:
            yield line


def print_diff(pool_diff, ms_diff):
    if not pool_diff and not ms_diff:
        print("No differences!")
        return
    for pool, changes in pool_diff.items():
        print("Pool: {}".format(pool))
        for change in changes:
            print(change)
    for ms, changes in ms_diff.items():
        print("Macroserver: {}".format(ms))
        for change in changes:
            print(change)


@click.argument("old_config", type=click.File("r"))
@click.argument("new_config", type=click.File("r"))
def diff_cmd(old_config, new_config):
    """
    Compare two given YAML sardana configuration files.
    """
    pool_diff, ms_diff = make_diff(
        remove_defaults(load(old_config, Loader=Loader)),
        remove_defaults(load(new_config, Loader=Loader)))
    print_diff(pool_diff, ms_diff)


def main():
    cmd = click.command("diff")(diff_cmd)
    return cmd()


if __name__ == "__main__":
    main()
