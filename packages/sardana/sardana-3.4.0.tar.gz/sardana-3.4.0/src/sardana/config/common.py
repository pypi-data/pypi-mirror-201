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

import copy


def clean_dict(d):
    """Just drop keys where value is None. We don't want empty stuff."""
    return {
        key: value
        for key, value in d.items()
        if value is not None
    }


def get_full_name(devname, tango_host):
    # TODO check if the name is already full
    return f"tango://{tango_host}/{devname}"


channel_defaults = {
    "enabled": True,
    "output": True,
    "synchronizer": "software",
    "synchronization": "Trigger",
}


def remove_defaults(config):
    """Remove parts of the configuration that are equal to the sardana defaults"""
    config = copy.deepcopy(config)
    for pool in config["pools"].values():
        for meas_grp in pool.get("measurement_groups", {}).values():
            channels = list(meas_grp["channels"])
            for i, ch in enumerate(channels):
                if isinstance(ch, dict):
                    ch_name, ch_config = list(ch.items())[0]
                    for k, v in channel_defaults.items():
                        if ch_config.get(k) == v:
                            ch_config.pop(k)
                    if not ch_config:
                        meas_grp["channels"][i] = ch_name                    
    return config
