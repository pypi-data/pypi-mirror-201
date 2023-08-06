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

from ..yaml2dsconfig import build_measurement_group_devices


def test_build_measurement_group_devices__elements_with_external():
    pool_name = "demo1"
    mntgrp_config = {
        "measurement_groups":{
            "mntgrp01": {
                "channels": [
                    "ct01", 
                    "sys/tg_test/1/ampli"
                ]
            }
        }
    }
    mntgrp_devices = build_measurement_group_devices(pool_name, mntgrp_config, {})
    assert mntgrp_devices == {
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


def test_build_measurement_group_devices__configuration(tango_host):
    pool_name = "demo1"
    mntgrp_config = {
        "measurement_groups":{
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
    }
    config = {
        "pools": {
            "demo1": {
                "controllers": {
                    "ctctrl01": {
                        "type": "CTExpChannel",
                        "python_module": "DummyCounterTimerController.py",
                        "python_class": "DummyCounterTimerController",
                        "elements": {
                            "ct01": {
                                "axis": 1
                            },   
                            "ct02": {
                                "axis": 2
                            }
                        }
                    }
                }
            }
        }
    }
    mntgrp_devices = build_measurement_group_devices(pool_name, mntgrp_config, config)
    # load JSON string for reliable comparison
    mntgrp_devices["mntgrp/pool_demo1_1/mntgrp01"]["attribute_properties"]["Configuration"]["__value"][0] = \
        json.loads(mntgrp_devices["mntgrp/pool_demo1_1/mntgrp01"]["attribute_properties"]["Configuration"]["__value"][0])
    assert mntgrp_devices == {
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
                    "__value": [{
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
                                        "full_name": f"tango://{tango_host}/expchan/ctctrl01/1",
                                        "enabled":True,
                                        "label":"ct01",
                                        "data_type": "float64",
                                        "data_units": "",
                                        "output":True,
                                        "plot_type":0,
                                        "plot_axes":[],
                                        "nexus_path": "",
                                        "conditioning":"",
                                        "normalization":0,
                                        "_controller_name":f"tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01"
                                    },
                                    f"tango://{tango_host}/expchan/ctctrl01/2":{
                                        "index":1,
                                        "name":"ct02",
                                        "full_name":f"tango://{tango_host}/expchan/ctctrl01/2",
                                        "enabled":False,
                                        "label":"ct02",
                                        "data_type": "float64",
                                        "data_units": "",
                                        "output":False,
                                        "plot_type":0,
                                        "plot_axes":[],
                                        "nexus_path": "",
                                        "conditioning":"",
                                        "normalization":0,
                                        "_controller_name":f"tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01"
                                    }
                                }
                            }
                        },
                        "label":"mntgrp01",
                        "description":"General purpose measurement configuration"
                    }]
                }
            }
        }
    }


def test_build_measurement_group_devices__configuration_hw_synchronization(tango_host):
    pool_name = "demo1"
    mntgrp_config = {
        "measurement_groups":{
            "mntgrp01": {
                "channels": [
                    {"ct01": {
                        "synchronization": "Start",
                        "synchronizer": "tg01"
                        }
                    }
                ]
            }
        }
    }
    config = {
        "pools": {
            "demo1": {
                "controllers": {
                    "ctctrl01": {
                        "type": "CTExpChannel",
                        "python_module": "DummyCounterTimerController.py",
                        "python_class": "DummyCounterTimerController",
                        "elements": {
                            "ct01": {
                                "axis": 1
                            }
                        }
                    },
                    "tgctrl01": {
                        "type": "TriggerGate",
                        "python_module": "DummyTriggerGateController.py",
                        "python_class": "DummyTriggerGateController",
                        "elements": {
                            "tg01": {
                                "axis": 1
                            }
                        }
                    }
                }
            }
        }
    }
    mntgrp_devices = build_measurement_group_devices(pool_name, mntgrp_config, config)
    # load JSON string for reliable comparison
    mntgrp_devices["mntgrp/pool_demo1_1/mntgrp01"]["attribute_properties"]["Configuration"]["__value"][0] = \
        json.loads(mntgrp_devices["mntgrp/pool_demo1_1/mntgrp01"]["attribute_properties"]["Configuration"]["__value"][0])
    assert mntgrp_devices == {
        "mntgrp/pool_demo1_1/mntgrp01": {
            "alias": "mntgrp01",
            "properties": {
                "elements": [
                    "ct01",
                    "tg01"                    
                ]
            },
            "attribute_properties": {
                "Configuration": {
                    "__value": [{
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
                                        "enabled":True,
                                        "label":"ct01",
                                        "data_type": "float64",
                                        "data_units": "",
                                        "output":True,
                                        "plot_type":0,
                                        "plot_axes":[],
                                        "nexus_path": "",
                                        "conditioning":"",
                                        "normalization":0,
                                        "_controller_name":f"tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01"
                                    }
                                }
                            }
                        },
                        "label":"mntgrp01",
                        "description":"General purpose measurement configuration"
                    }]
                }
            }
        }
    }



def test_build_measurement_group_devices__configuration_with_external(tango_host):
    pool_name = "demo1"
    mntgrp_config = {
        "measurement_groups":{
            "mntgrp01": {
                "channels": [
                    "ct01",
                    {"sys/tg_test/1/ampli": {
                        "enabled": False,
                        "output": False,
                        "data_units": "millimeters"
                        }
                    }
                ]
            }
        }
    }
    config = {
        "pools": {
            "demo1": {
                "controllers": {
                    "ctctrl01": {
                        "type": "CTExpChannel",
                        "python_module": "DummyCounterTimerController.py",
                        "python_class": "DummyCounterTimerController",
                        "elements": {
                            "ct01": {
                                "axis": 1
                            }
                        }
                    }
                }
            }
        }
    }
    mntgrp_devices = build_measurement_group_devices(pool_name, mntgrp_config, config)
    # load JSON string for reliable comparison
    mntgrp_devices["mntgrp/pool_demo1_1/mntgrp01"]["attribute_properties"]["Configuration"]["__value"][0] = \
        json.loads(mntgrp_devices["mntgrp/pool_demo1_1/mntgrp01"]["attribute_properties"]["Configuration"]["__value"][0])
    assert mntgrp_devices == {
        "mntgrp/pool_demo1_1/mntgrp01": {
            "alias": "mntgrp01",
            "properties": {
                "elements": [
                    "ct01",
                    "sys/tg_test/1/ampli",
                ]
            },
            "attribute_properties": {
                "Configuration": {
                    "__value": [{
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
                                        "enabled":True,
                                        "label":"ct01",
                                        "data_type": "float64",
                                        "data_units": "",
                                        "output":True,
                                        "plot_type":0,
                                        "plot_axes":[],
                                        "nexus_path": "",
                                        "conditioning":"",
                                        "normalization":0,
                                        "_controller_name":f"tango://{tango_host}/controller/dummycountertimercontroller/ctctrl01"
                                    }
                                }
                            },
                            "__tango__":{
                                "channels":{
                                    f"tango://{tango_host}/sys/tg_test/1/ampli":{
                                        "name":"ampli",
                                        "label":"sys/tg_test/1/ampli",
                                        "full_name":f"tango://{tango_host}/sys/tg_test/1/ampli",
                                        "enabled":False,
                                        "output":False,
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
                    }]
                }
            }
        }
    }
