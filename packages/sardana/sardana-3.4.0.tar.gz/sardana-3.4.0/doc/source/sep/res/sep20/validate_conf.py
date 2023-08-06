import yaml
from jsonschema import validate

test_yaml = """
attributes:
  velocity: 1.23
  acceleration:
    value: 4.56
    label: Acc
    format: \%6.2f
    unit: s
    polling_period: 3    
    abs_change: 1
    rel_change: 0.1
    min_value: 0
    max_value: 5
    min_alarm: 1
    max_alarm: 4
"""

obj = yaml.safe_load(test_yaml)

attr_value_types = [
    {"type": "number"},
    {"type": "string"},
    {"type": "array"}
]

schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/product.schema.json",
  "title": "Attributes",
  "description": "Attributes configuration",
  "type": "object",
  "properties": {
    "attributes": {
      "description": "Mapping with attributes",
      "type": "object",
      "patternProperties": {
        ".*": {
          "oneOf": attr_value_types +
            [{
              "type": "object",
              "properties": {
                "value": {"oneOf": attr_value_types},
                "label": {"type": "string"},
                "format": {"type": "string"},
                "unit": {"type": "string"},
                "polling_period": {"type": "number"},
                "abs_change": {"type": "number"},
                "rel_change": {"type": "number"},
                "min_value": {"type": "number"},
                "max_value": {"type": "number"},
                "min_alarm": {"type": "number"},
                "max_alarm": {"type": "number"}
              }
            }]
        }
      }
    }
  }
}

validate(obj, schema)