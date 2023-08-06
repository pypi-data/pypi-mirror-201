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
import dsconfig
import yaml
import tango

from .dsconfig2yaml import build_sardana_config


@click.argument("macro_server", required=False)
def dump_cmd(macro_server):
    """
    Export an existing Sardana install to YAML.
    If there is only one macro server in the database, use that. Otherwise
    the user must specify the device name of the relevant macro server.
    """
    db = tango.Database()
    if macro_server is None:
        # Try to auto-detect macro server
        # TODO use a better way that includes unexported devices
        macro_servers = db.get_device_exported_for_class("MacroServer")
        if len(macro_servers) == 0:
            sys.exit("No MacroServer found; nothing to dump!")
        if len(macro_servers) > 1:
            sys.exit(f"Found several MacroServers: {', '.join(macro_servers)}."
                     " Please specify which to use.")
        macro_server = macro_servers[0]
    try:
        current_config = dump_sardana_config(db, macro_server)
    except RuntimeError as e:
        sys.exit(str(e))
    try:
        yaml.dump(current_config, sys.stdout, sort_keys=False)
    except TypeError:
        # compatibility with PyYAML < 5.1
        # dump will be ordered alphabetically
        yaml.dump(current_config, sys.stdout, default_flow_style=False)


def dump_sardana_config(db: tango.Database, macro_server: str) -> dict:
    "Helper to dump data from the Tango DB"
    # Find the relevant pools
    # TODO handle errors
    servers = set()
    try:
        ms_server = db.get_device_info(macro_server).ds_full_name
    except tango.DevFailed as e:
        raise RuntimeError(f"Unable to get info about MacroServer {macro_server}: {e}")
    servers.add(ms_server)
    pool_names = db.get_device_property(macro_server, "PoolNames")["PoolNames"]
    pool_devices = [
        name if "/" in name else db.get_device_from_alias(name)
        for name in pool_names
    ]
    pool_servers = set(
        db.get_device_info(pd).ds_full_name
        for pd in pool_devices
    )
    servers.update(pool_servers)

    # Dump the relevant data from the Tango database
    ds_config = dsconfig.dump.get_db_data(db, [f"server:{s}" for s in servers])

    try:
        return build_sardana_config(ds_config, macro_server)
    except RuntimeError as e:
        sys.exit(f"Error: {e}")


def main():
    cmd = click.command("dump")(dump_cmd)
    return cmd()


if __name__ == "__main__":
    main()
