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

from ..dsconfig2yaml import find_measurement_groups

def test_find_measurement_group__elements_with_external():
    server = {
        "MeasurementGroup": {
            "mntgrp/pool_demo1_1/mntgrp01": {
                "alias": "mntgrp01",
                "properties": {
                    "elements": [
                        "ct01",
                        "sys/tg_test/1/ampli"
         
                    ]
                }
            }
        }
    }
    mntgrps = {alias: mntgrp for alias, mntgrp in find_measurement_groups(server)}
    assert mntgrps == \
        {"mntgrp01": {"channels": ["ct01", "sys/tg_test/1/ampli"]}}


def test_find_measurement_group__configuration(tango_host):
    server = {
        "MeasurementGroup": {
            "mntgrp/pool_demo1_1/mntgrp01": {
                "alias": "mntgrp01",
                "properties": {
                    "elements": [
                        "ct01",
                        "ct02",
                    ]
                },
                "attribute_properties": {
                    "Configuration": {
                        "__value": [json.dumps({
                            "controllers":{
                                f"tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01":{
                                    "synchronizer":"software",
                                    "synchronization":0,
                                    "timer":f"tango://{tango_host}/expchan/ctctrl01/1",
                                    "monitor":f"tango://{tango_host}/expchan/ctctrl01/1",
                                    "channels":{
                                        f"tango://{tango_host}/expchan/ctctrl01/1":{
                                            "index":0,
                                            "name":"ct01",
                                            "full_name":f"tango://{tango_host}/expchan/ctctrl01/1",
                                            "source":f"tango://{tango_host}/expchan/ctctrl01/1/Value",
                                            "enabled":True,
                                            "label":"ct01",
                                            "data_type": "float64",
                                            "data_units": "",
                                            "ndim":0,
                                            "output":True,
                                            "plot_type":0,
                                            "plot_axes":[],
                                            "conditioning":"",
                                            "normalization":0,
                                            "_controller_name":f"tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01"
                                        },
                                        f"tango://{tango_host}/expchan/ctctrl01/2":{
                                            "index":1,
                                            "name":"ct02",
                                            "full_name":f"tango://{tango_host}/expchan/ctctrl01/2",
                                            "source":f"tango://{tango_host}/expchan/ctctrl01/2/Value",
                                            "enabled":False,
                                            "label":"ct02",
                                            "data_type": "float64",
                                            "data_units": "",
                                            "ndim":0,
                                            "output":False,
                                            "plot_type":0,
                                            "plot_axes":[],
                                            "conditioning":"",
                                            "normalization":0,
                                            "_controller_name":f"tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01"
                                        }
                                    }
                                }
                            },
                            "label":"mntgrp01",
                            "description":"General purpose measurement configuration"
                        }, separators=(",", ":"))]
                    }
                }
            }
        }
    }
    mntgrps = {alias: mntgrp for alias, mntgrp in find_measurement_groups(server)}
    assert mntgrps == \
        {
            "mntgrp01": {
                "channels": [
                    "ct01",
                    {"ct02": {
                        "enabled": False,
                        "output": False
                        }
                    }
                ]
            }
        }


def test_find_measurement_group__configuration_hw_synchronizer(tango_host):
    server = {
        "TriggerGate": {
            "triggergate/tgctrl01/1": {
                "alias": "tg01",
                "properties": {
                    "axis": [
                        "1"
                    ],
                    "ctrl_id": [
                        "tgctrl01"
                    ]
                }
            }
        },
        "MeasurementGroup": {
            "mntgrp/pool_demo1_1/mntgrp01": {
                "alias": "mntgrp01",
                "properties": {
                    "elements": [
                        "ct01"
                    ]
                },
                "attribute_properties": {
                    "Configuration": {
                        "__value": [json.dumps({
                            "controllers":{
                                f"tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01":{
                                    "synchronizer":f"tango://{tango_host}/triggergate/tgctrl01/1",
                                    "synchronization":2,
                                    "timer":f"tango://{tango_host}/expchan/ctctrl01/1",
                                    "monitor":f"tango://{tango_host}/expchan/ctctrl01/1",
                                    "channels":{
                                        f"tango://{tango_host}/expchan/ctctrl01/1":{
                                            "index":0,
                                            "name":"ct01",
                                            "full_name":f"tango://{tango_host}/expchan/ctctrl01/1",
                                            "source":f"tango://{tango_host}/expchan/ctctrl01/1/Value",
                                            "enabled":True,
                                            "label":"ct01",
                                            "data_type": "float64",
                                            "data_units": "",
                                            "ndim":0,
                                            "output":True,
                                            "plot_type":0,
                                            "plot_axes":[],
                                            "conditioning":"",
                                            "normalization":0,
                                            "_controller_name":f"tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01"
                                        }
                                    }
                                }
                            },
                            "label":"mntgrp01",
                            "description":"General purpose measurement configuration"
                        }, separators=(",", ":"))]
                    }
                }
            }
        }
    }
    mntgrps = {alias: mntgrp for alias, mntgrp in find_measurement_groups(server)}
    assert mntgrps == \
        {
            "mntgrp01": {
                "channels": [
                    {"ct01": {
                        "synchronizer": "tg01",
                        "synchronization": "Start"
                        }
                    }
                ]
            }
        }


def test_find_measurement_group__configuration_with_external():
    server = {
        "MeasurementGroup": {
            "mntgrp/pool_demo1_1/mntgrp01": {
                "alias": "mntgrp01",
                "properties": {
                    "elements": [
                        "ct01",
                        "tango://{tango_host}/sys/tg_test/1/ampli",
                    ]
                },
                "attribute_properties": {
                    "Configuration": {
                        "__value": ["""{
                            "controllers":{
                                "tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01":{
                                    "synchronizer":"software",
                                    "synchronization":0,
                                    "timer":"tango://{tango_host}/expchan/ctctrl01/1",
                                    "monitor":"tango://{tango_host}/expchan/ctctrl01/1",
                                    "channels":{
                                        "tango://{tango_host}/expchan/ctctrl01/1":{
                                            "index":0,
                                            "name":"ct01",
                                            "full_name":"tango://{tango_host}/expchan/ctctrl01/1",
                                            "enabled":true,
                                            "label":"ct01",
                                            "data_type": "float64",
                                            "data_units": "",
                                            "ndim":0,
                                            "output":true,
                                            "plot_type":0,
                                            "plot_axes":[],
                                            "conditioning":"",
                                            "normalization":0,
                                            "_controller_name":"tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01"
                                        }
                                    }
                                },
                                "__tango__":{
                                    "channels":{
                                        "tango://{tango_host}/sys/tg_test/1/ampli":{
                                            "name":"ampli",
                                            "label":"sys/tg_test/1/ampli",
                                            "full_name":"tango://{tango_host}/sys/tg_test/1/ampli",
                                            "enabled":true,
                                            "output":true,
                                            "data_type":"float64",
                                            "data_units":"millimeters",
                                            "conditioning":"",
                                            "normalization":0,
                                            "nexus_path":"",
                                            "plot_type":0,
                                            "plot_axes":[],
                                            "_controller_name":"__tango__",
                                            "index":1
                                        }
                                    }
                                }
                            },
                            "label":"mntgrp01",
                            "description":"General purpose measurement configuration"
                        }"""]
                    }
                }
            }
        }
    }
    mntgrps = {alias: mntgrp for alias, mntgrp in find_measurement_groups(server)}
    assert mntgrps == \
        {
            "mntgrp01": {
                "channels": [
                    "ct01",
                    {
                        "sys/tg_test/1/ampli": {
                            "data_units": "millimeters"
                        }
                    }
                ]
            }
        }
