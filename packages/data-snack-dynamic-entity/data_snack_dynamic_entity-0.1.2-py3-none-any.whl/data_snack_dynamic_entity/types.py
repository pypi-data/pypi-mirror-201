from typing import TypedDict, Dict, Any


class FieldSchema(TypedDict):
    type: str
    key: bool
    excluded: bool
    optional: bool
    default: Any


class EntitySchema(TypedDict):
    properties: Dict[str, FieldSchema]


EntityTemplates = Dict[str, EntitySchema]
