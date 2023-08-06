.. _sardana-configuration:

*********************
Sardana configuration
*********************

There are many configuration points in Sardana and unfortunately there is
no single configuration application neither interface to access all of them yet.

.. note::
    At the time of writing, Sardana system can :ref:`run
    only as Tango device server <sardana-getting-started-running-server>`
    and most of the configurations are stored in the Tango database (Tango DB).
    One can easily change them with the Jive client application,
    but it is highly recommended to use the Sardana configuration tools
    instead.

.. _sardana-configuration-format-and-tools:

Configuration format and tools
==============================

The Sardana 3.4.0 version including `SEP20 <https://gitlab.com/sardana-org/sardana/-/merge_requests/1749>`_
introduced a configuration text format based on `YAML <https://yaml.org/>`_
(see `sar_demo.yaml <https://gitlab.com/sardana-org/sardana/-/tree/develop/src/sardana/config/test/sar_demo.yaml>`_ example),
and a set of CLI tools for configuring Sardana systems (check ``sardana config --help``
to list all of them). In the future we plan to merge all the others configuration interfaces
into this format in order to provide a single point of configuration.

It is important to know that the Sardana config tools work "offline",
acting directly upon the Tango DB without requiring a running Sardana instance.
This means it can be used to set up a Sardana installation from scratch.
However this also means that it can not modify the state of the running
Sardana instance without restarting it or running
the `~sardana.macroserver.macros.expert.reconfig` macro afterwards.

This video shows a short demonstration on how to use it.

.. youtube:: 9oRYRXw-afs

.. |br| raw:: html

    <br>
    
|br|
In the following sketch you can see the main actions provided by these tools:

.. mermaid::
    :align: center
    :caption: Sardana CLI configuration tools

    flowchart TD
        DB[(Tango DB)] -->|dump| YAML("Sardana config (YAML)")
        YAML -->|load| DB
        YAML---|validate|YAML
        YAML2("Old Sardana config (YAML)")
        YAML---|diff|YAML2
        YAML---|update|YAML2
        style YAML2 stroke-dasharray: 5 5

In order to be ergonomic when it comes to comparing versions etc, the tools are written
to enable "roundtripping" as far as reasonably possible. This means that converting
e.g. from Tango DB -> YAML -> Tango DB again should result in a Sardana system
that is functionally identical to the original. The idea is to make actual changes easy to detect.
Perfect roundtripping may not always be possible, due to Tango's handling of properties
as strings, and case insensitivity, among other things.

The conversion does not persist things like key ordering, and YAML comments,
but only "logical" content. Take a look at the :ref:`sardana-config-update` command
for a solution to this.

In general, the commands read from files, and write to stdout. Therefore in order
to write the results to files, use shell redirection (see examples below).
It is also possible to substitute filenames with `-` which means
the command expects to read from stdin.
This enables piping the output of one command into another, useful for scripting.

Here follows a brief explanation of the commands available, with examples.
Use the ``--help`` option to get more details about each command.

.. _sardana-config-dump:

dump
----

This command "dumps" a Sardana system stored in the Tango DB
into a Sardana YAML configuration text. You must provide the device name
of the macro server, if there is more than one.

Example::

    sardana config dump macroserver/demo1/1 > my_config.yaml

.. _sardana-config-load:

load
----

Does the opposite of ``dump``, takes a Sardana YAML configuration and loads
it into a Tango DB. It also prints out information about the changes required
to bring the DB to the desired state. By default, this script runs in *dry run*
mode, meaning that it does not actually change the Tango DB,
but just simulates and reports what would change.

Use ``--write`` option to really change the Tango DB.

Example::
    
    sardana config load my_config.yaml  # dry run
    sardana config load --write my_config.yaml

.. _sardana-config-validate:
    
validate
--------

Reads a Sardana YAML configuration and checks that it is properly formatted.
By default, this command makes a syntactic check only. Use ``--check-code`` to enable
validation against the plugins code, which means that it must be run in
a sardana environment that has all used controllers installed.
The script is then able to do more sophisticated checks.

If problems are found, the script fails and some errors should be displayed
to help fixing the problems.

Example::

    sardana config validate my_config.yaml  # syntactic check
    sardana config validate --check-code my_config.yaml  # full check

.. _sardana-config-diff:

diff
----

Reads two Sardana YAML configurations and produces a list of what has changed
from the first to the second one. This can be useful when looking for differences between
e.g. two snapshots taken at different times. The output is intended mainly to be human readable.

Example::

    sardana config diff my_config.yaml my_config_update.yaml
    
    Pool: demo1
    - REPLACE /pools/demo1/controllers/slitctrl01/physical_roles/sl2b mot02 => mot03
    - REMOVE /pools/demo1/measurement_groups/mntgrp01/channels/3

.. _sardana-config-update:

update
------

(Note: this is a complex feature, we'll see how well it works in practice.)

One benefit of the YAML format is that it allows inline comments.
However since we cannot store these in the Tango DB, they will be lost in the conversion.
Also, the ordering of keys in the file will not persist when converting to Tango DB and back.

As a solution to that problem, this command allows you to "update" an existing YAML config.
The idea is that a YAML file that contains ordering and comments can be updated with the
current state of the installation, without losing all extra information.

Let's say you have a `my_config.yaml` where you have organized things nice and commented.
Now create an `my_config_dump.yaml` from a dump of the same Sardana installation
and then run the script like this::

    sardana config update my_config.yaml my_config_dump.yaml > my_config_updated.yaml
    
Now `my_config_updated.yaml` should contain the new config, but
keeping your comments and ordering from the original (as far as possible).

Another point is that this should make the commit diffs more readable if you intend
to manage the config with e.g. `git`. However, if you don't care about comments and
ordering, it is probably better to rely on the *diff* command above.

Configuration points
====================

This guide goes step-by-step through the Sardana system configuration
process and lists all of the configuration points linking to documents with
more detailed explanation. It starts from configuration of the
:ref:`sardana-spock` client, going through the
:ref:`MacroServer<sardana-macroserver-overview>` and finally ending on the
:ref:`Device Pool <sardana-pool-overview>`.

This chapter will not document itself all the different configuration
possibilities and will just link you to other documents explaining them in
details.

.. toctree::
    :maxdepth: 2

    Spock configuration <spock>
    Server configuration <server>
    MacroServer configuration <macroserver>
    Device Pool configuration <pool>
    Sardana Custom Settings <sardanacustomsettings>
    
