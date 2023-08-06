"""
Requires: 
 - `dictdiffer` package for finding differences in between 
   dictionaries
"""

import os
import inspect
from pathlib import Path
from pprint import pprint

import yaml

try:
    import dictdiffer
except ImportError:
    dictdiffer = None


current_dir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)


def load_yaml_from_file(file_path, load_all=False):
    with file_path.open(mode="rt", encoding="utf-8") as file:
        if load_all:
            return [document for document in yaml.safe_load_all(file)]
        else:
            return yaml.safe_load(file)


def load_yaml_from_dir(dir_path):
    document = {}
    for item_path in dir_path.iterdir():
        if item_path.is_dir():
            name = item_path.name
            document[name] = load_yaml_from_dir(item_path)
        else:
            yaml = load_yaml_from_file(item_path)
            name = item_path.stem
            if name == dir_path.name:
                document.update(yaml)
            else:
                document[name] = yaml
    return document


def load_single():
    file_path = Path(current_dir, "sar_demo.yaml")
    return load_yaml_from_file(file_path, load_all=True)


def load_multi():
    dir_path = Path(current_dir, "sar_demo")
    documents = []
    for item_path in dir_path.iterdir():
        if item_path.is_dir():
            document = load_yaml_from_dir(item_path)
        else:
            document = load_yaml_from_file(item_path)
        documents.append(document)
    return documents


def assert_equivalent(first, second):

    def pop_item_with_name(items, name):
        for item in items:
            if item["name"] == name:
                break
        return items.pop(items.index(item))

    for item_from_first in first:
        name = item_from_first["name"]
        item_from_second = pop_item_with_name(second, name)
        if dictdiffer:
            diff = [d for d in dictdiffer.diff(item_from_first, item_from_second)]
            if diff:
                raise AssertionError(diff)
        else:
            assert item_from_first == item_from_second
        
    assert len(second) == 0


if __name__ == "__main__":
    single = load_single()
    multi = load_multi()
    assert_equivalent(single, multi)
