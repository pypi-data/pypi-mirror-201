from io import StringIO
import json
from ruamel.yaml import YAML

from dsconfig.dump import get_db_data
import pytest
import tango

from ..load import load_cmd
from ..dsconfig2yaml import build_sardana_config


def test_load_cmd(sar_demo_json_unique):
    """
    Basic test that loads a sardana config into the Tango DB and
    then checks that it is the same as expected.
    """
    # This is a dsconfig, where all tango names have been uniquified.
    name, config_json = sar_demo_json_unique

    # Create a YAML config from the dsconfig
    yaml = YAML(typ="rt")
    yaml_config = build_sardana_config(config_json, f"MacroServer/{name}/1")
    fake_yaml_config_file = StringIO()
    yaml.dump(yaml_config, fake_yaml_config_file)
    fake_yaml_config_file.seek(0)

    # Load the YAML config into the Tango DB
    load_cmd(fake_yaml_config_file, write=True)

    # Get a dsconfig back from the DB, and compare to the original
    # They should be the same (we allow different ordering of keys)
    db = tango.Database()
    dump = get_db_data(db, patterns=[f"server:Sardana/{name}"])
    assert (json.dumps(dump, indent=2, sort_keys=True) ==
            json.dumps(config_json, indent=2, sort_keys=True))

    # Clean up
    db.delete_server(f"Sardana/{name}")


def test_load_cmd__wrong_tango_host(sar_demo_json_unique):
    """
    Check that we don't allow applying config to the wrong host.
    """
    name, config_json = sar_demo_json_unique

    yaml = YAML(typ="rt")
    yaml_config = build_sardana_config(config_json, f"MacroServer/{name}/1")

    yaml_config["tango_host"] = "i.am.not.a.real.tango.host:1234567890"
    fake_yaml_config_file = StringIO()
    yaml.dump(yaml_config, fake_yaml_config_file)
    fake_yaml_config_file.seek(0)

    with pytest.raises(SystemExit):
        load_cmd(fake_yaml_config_file, write=True)
