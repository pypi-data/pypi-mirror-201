#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
##
# This file is part of Sardana
##
# http://www.sardana-controls.org/
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Sardana is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Sardana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""This package provides spock"""

import click
from .genutils import (load_ipython_extension, unload_ipython_extension,  # noqa
    load_config, run)  # noqa


def main():
    import taurus
    taurus.setLogLevel(getattr(taurus, "Warning"))
    run()


@click.command("spock")
@click.option("--profile", 
              help=("use custom IPython profile, for example, "
                    "to connect to your Door."))
def spock_cmd(*args, **kwargs):
    """CLI for executing macros and general control.
    
    For full list of arguments and options check IPython's help:
    `ipython --help`
    """
    import sys
    import taurus
    # taurus.setLogLevel(getattr(taurus, "Warning"))
    sys.argv = sys.argv[sys.argv.index("spock"):]  # necessary for IPython to work
    run()

# in order to click not intercept and complain about
# arguments/options passed to IPython
spock_cmd.allow_extra_args=True
spock_cmd.ignore_unknown_options=True
