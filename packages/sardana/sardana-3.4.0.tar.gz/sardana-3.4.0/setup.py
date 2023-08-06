#!/usr/bin/env python

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

import os
import sys
import imp
from setuptools import setup, find_packages


def get_release_info():
    name = "release"
    setup_dir = os.path.dirname(os.path.abspath(__file__))
    release_dir = os.path.join(setup_dir, "src", "sardana")
    data = imp.find_module(name, [release_dir])
    release = imp.load_module(name, *data)
    return release

release = get_release_info()

package_dir = {"": "src"}

packages = find_packages(where="src")

provides = [
    'sardana',
    # 'sardana.pool',
    # 'sardana.macroserver',
    # 'sardana.spock',
    # 'sardana.tango',
]

install_requires = [
    'PyTango>=9.2.5',
    'itango>=0.1.6',
    'taurus >=5.0.0',
    'lxml>=2.3',
    'click',
]

extras_require = {
    "config": [
        "dsconfig>=1.6.7",
        "PyYAML",
        "ruamel.yaml",
        "pydantic",
        "jsonpatch",
    ]
}

console_scripts = [
    "MacroServer = sardana.tango.macroserver:main",
    "Pool = sardana.tango.pool:main",
    "Sardana = sardana.tango:main",
    "spock = sardana.spock:main",
    "diffractometeralignment = sardana.taurus.qt.qtgui.extra_hkl.diffractometeralignment:main",
    "hklscan = sardana.taurus.qt.qtgui.extra_hkl.hklscan:main",
    "macroexecutor = sardana.taurus.qt.qtgui.extra_macroexecutor.macroexecutor:_main",
    "sequencer = sardana.taurus.qt.qtgui.extra_macroexecutor.sequenceeditor:_main",
    "ubmatrix = sardana.taurus.qt.qtgui.extra_hkl.ubmatrix:main",
    "showscan = sardana.taurus.qt.qtgui.extra_sardana.showscanonline:_main",
]

sardana_script_name = "sardana"
# Sardana server script collides with sardana common script on Windows
# since Windows file system by default is case insensitive
# See: https://gitlab.com/sardana-org/sardana/-/issues/286
if os.name == "nt":
    sardana_script_name += "cli"

console_scripts.append(
    "{} = sardana.cli:main".format(sardana_script_name)
)

sardana_subcommands = [
    "expconf = sardana.taurus.qt.qtgui.extra_sardana.expdescription:expconf_cmd",
    "macroexecutor = sardana.taurus.qt.qtgui.extra_macroexecutor.macroexecutor:macroexecutor_cmd",
    "sequencer = sardana.taurus.qt.qtgui.extra_macroexecutor.sequenceeditor.sequenceeditor:sequencer_cmd",
    "showscan = sardana.taurus.qt.qtgui.extra_sardana.showscanonline:showscan_cmd",
    "spock = sardana.spock:spock_cmd",
]
if sys.version_info >= (3, 6):
    # Currently the config scripts don't support older python versions.
    sardana_subcommands.append("config = sardana.config.config:config_grp")


form_factories = [
    "sardana.pool = sardana.taurus.qt.qtgui.extra_pool.formitemfactory:pool_item_factory"  # noqa
]

pytest_plugins = [
    "sardana_pool_plugins = sardana.pool.test.util"
]

entry_points = {
    'console_scripts': console_scripts,
    'sardana.cli.subcommands': sardana_subcommands,
    'taurus.form.item_factories': form_factories,
    'pytest11': pytest_plugins
}

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Environment :: No Input/Output (Daemon)',
    'Environment :: Win32 (MS Windows)',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.5',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Libraries',
]

setup(name='sardana',
      version=release.version,
      description=release.description,
      long_description=release.long_description,
      author=release.authors['Tiago_et_al'][0],
      maintainer=release.authors['Community'][0],
      maintainer_email=release.authors['Community'][1],
      url=release.url,
      download_url=release.download_url,
      platforms=release.platforms,
      license=release.license,
      keywords=release.keywords,
      packages=packages,
      package_dir=package_dir,
      include_package_data=True,
      classifiers=classifiers,
      entry_points=entry_points,
      provides=provides,
      install_requires=install_requires,
      extras_require=extras_require,
      )
