from typing import Any, Dict, Optional, Type

from apispec import APISpec
from mashumaro.jsonschema import OPEN_API_3_1, JSONSchemaBuilder


def build_json_schema(
    instance_type: Type, spec: Optional[APISpec] = None
) -> Optional[Dict[str, Any]]:
    builder = JSONSchemaBuilder(dialect=OPEN_API_3_1)
    try:
        json_schema = builder.build(instance_type)
    except Exception:
        return None
    if spec is not None:
        for name, schema in builder.context.definitions.items():
            spec.components.schemas[name] = schema.to_dict()
    return json_schema.to_dict()
