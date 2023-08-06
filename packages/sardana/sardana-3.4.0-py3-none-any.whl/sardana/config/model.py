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

import pathlib
from typing import Dict, List, Tuple, Optional, Union, Sequence, Any
from typing_extensions import Annotated, Literal
import re

from pydantic import BaseModel, Field, NegativeFloat, PositiveFloat, validator


class StrictBaseModel(BaseModel):
    """
    Base model that allows no members that aren't defined in the model
    This is intended to prevent e.g. typos, and there's no point in
    allowing things that we're not going to use anyway.
    """
    class Config:
        extra = "forbid"


class Name(str):

    """
    Custom string class for Sardana names.
    Validates that they are correctly formed.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Name must be a string")
        if " " in v:
            raise ValueError(f"Bad name '{v}': element names can't contain space")
        # TODO what else? Only characters allowed in tango aliases, I guess?
        return v


class PythonModule(str):

    """
    Custom string class for Sardana names.
    Validates that they are correctly formed.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Python module must be a string")
        if not v.endswith(".py"):
            raise ValueError("Python module must be a python file, name ending with '.py'.")
        return v


class DeviceName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Device name must be a string")
        if not len(v.split("/")) == 3:
            raise ValueError("Bad device name '{v}': should have form 'domain/family/member'")
        return v


class ServerName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Server name must be a string")
        if not 1 <= len(v.split("/")) <= 2:
            raise ValueError("Bad server name '{v}': should have form 'server/instance' or just server")
        return v


class TangoHost(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Tango host must be a string")
        if not re.match(r".*:\d+", v):
            raise ValueError("Bad Tango host: should be <hostname>:<port>")


class FullDeviceName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not re.match(r"tango://.*:\d+/[^/]+/[^/]+/[^/+]", v):
            raise ValueError("Bad full device name: should be tango://<hostname>:<port>/<device>")


# ==== MacroServer ====

class Environment(StrictBaseModel):
    "Environment"
    # TODO
    path: Optional[pathlib.Path]
    variables: Optional[Dict[str, str]]


class MacroServer(StrictBaseModel):
    "The MacroServer runs macros, and generally runs the show"
    # tango: Optional[Dict[str, str]]   # TODO; should we remove it?
    tango_alias: Optional[Name]
    tango_device: Optional[DeviceName]
    tango_server: Optional[ServerName]
    macro_path: Optional[Sequence[pathlib.Path]]
    recorder_path: Optional[Sequence[pathlib.Path]]
    python_path: Optional[Sequence[pathlib.Path]]
    doors: Dict[Name, Union[Dict[str, str], None]]  # TODO
    pools: Optional[Sequence[Name]]
    environment: Optional[Environment]


# ==== Pool ====

class Instrument(StrictBaseModel):
    "An instrument is a collection of elements"
    cls: str = Field(alias="class")


AttributeValue = Union[int, float, bool, str]

Change = Union[PositiveFloat, Tuple[NegativeFloat, PositiveFloat]]


class AttributeConfig(StrictBaseModel):
    "Tango attribute condfiguration parameters"
    value: Optional[AttributeValue]
    label: Optional[str]
    format: Optional[str]
    unit: Optional[str]
    polling_period: Optional[int]
    abs_change: Optional[Change]
    rel_change: Optional[Change]
    archive_abs_change: Optional[Change]
    archive_rel_change: Optional[Change]
    min_value: Optional[float]
    max_value: Optional[float]
    min_alarm: Optional[float]
    max_alarm: Optional[float]


class Element(StrictBaseModel):
    """
    A single sardana element.
    """
    axis: int
    attributes: Optional[Dict[str, Union[AttributeValue, AttributeConfig]]]
    properties: Optional[Dict[str, Union[str, List[str]]]]
    instrument: Optional[Name]
    tango_device: Optional[DeviceName]
    drift_correction: Optional[bool]


class BaseController(StrictBaseModel):
    "A controller"
    python_module: PythonModule
    python_class: str
    tango_device: Optional[DeviceName]
    elements: Dict[Name, Element]
    attributes: Optional[Dict[str, Union[AttributeValue, AttributeConfig]]]
    properties: Optional[Dict[str, Union[str, List[str]]]]


# TODO would be nice if we could get controller types from sardana itself..?
class MotorController(BaseController):
    "A motor controller"
    type: Literal["Motor"]


class CTExpChannelController(BaseController):
    "Counter Experimental Channel"
    type: Literal["CTExpChannel"]


class ZeroDExpChannelController(BaseController):
    "Zero Dimensional (scalar) experimental channel"
    type: Literal["ZeroDExpChannel"]


class OneDExpChannelController(BaseController):
    "One dimensional (array) experimental channel"
    type: Literal["OneDExpChannel"]


class TwoDExpChannelController(BaseController):
    "Two dimensional (image) experimental channel"
    type: Literal["TwoDExpChannel"]


class IORegisterController(BaseController):
    "IO register"
    type: Literal["IORegister"]


class TriggerGateController(BaseController):
    "Trigger gate controller"
    type: Literal["TriggerGate"]


class PseudoMotorController(BaseController):
    "Pseudo motor controller"
    type: Literal["PseudoMotor"]
    physical_roles: Dict[str, Name]


class PseudoCounterController(BaseController):
    "Pseudo counter controller"
    type: Literal["PseudoCounter"]
    physical_roles: Optional[Dict[str, Name]]


Controller = Annotated[
    Union[
        MotorController, CTExpChannelController,
        ZeroDExpChannelController, OneDExpChannelController, TwoDExpChannelController,
        PseudoMotorController, PseudoCounterController,
        TriggerGateController, IORegisterController
    ],
    Field(discriminator="type")
]


class MeasurementGroupChannel(StrictBaseModel):
    """Configuration for a measurement group channel"""
    enabled: Optional[bool]
    synchronization: Optional[str]  # TODO enum?
    synchronizer: Optional[Union[Name, DeviceName, FullDeviceName]]
    timer: Optional[Union[Name, DeviceName, FullDeviceName]]
    monitor: Optional[Union[Name, DeviceName, FullDeviceName]]
    output: Optional[bool]
    data_type: Optional[str]  # TODO check valid tango type?
    data_units: Optional[str]
    nexus_path: Optional[pathlib.Path]


class MeasurementGroup(StrictBaseModel):
    "A measurement group"
    label: Optional[str]
    description: Optional[str]
    channels: List[Union[Name, DeviceName, Dict[Name, MeasurementGroupChannel]]]

    @validator("channels", each_item=True, pre=True)
    def check_channels(cls, c):
        if isinstance(c, dict):
            if len(c) > 1:
                raise ValueError(f"Expected one key (channel name), got {list(c.keys())}")
        return c


class Pool(StrictBaseModel):
    "The pool handles interfacing with hardware and the control system"
    # tango: Optional[Dict[str, Any]]   # TODO; should we remove it?
    tango_alias: Optional[Name]
    tango_device: Optional[DeviceName]
    tango_server: Optional[ServerName]
    # alias: Optional[Name]
    pool_path: Optional[Sequence[pathlib.Path]]
    python_path: Optional[Sequence[pathlib.Path]]
    instruments: Optional[Dict[Name, Instrument]]
    controllers: Dict[Name, Controller]
    measurement_groups: Optional[Dict[Name, MeasurementGroup]]


class Configuration(StrictBaseModel):
    "Collects all of the configuration for a Sardana installation"
    tango_host: Optional[TangoHost]
    pools: Dict[Name, Pool]
    macro_servers: Optional[Dict[Name, MacroServer]]

    @validator("pools")
    def check_pools(cls, v):
        assert len(v) > 0
        return v

    @validator("macro_servers")
    def check_macro_servers(cls, v):
        assert len(v) > 0
        return v


if __name__ == "__main__":
    print(Configuration.schema_json(indent=4))
