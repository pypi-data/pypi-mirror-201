import json
from jsonschema import Draft7Validator
from pathlib import Path

from data_snack_dynamic_entity.types import EntityTemplates

_SCHEMA = json.load(
    open(Path(__file__).resolve().parent / "./entityTemplates.schema.json")
)


class ValidationError(Exception):
    ...


def validate_entity_templates(templates: EntityTemplates) -> None:
    """
    Validates if provided templates config follows the right schema.

    :param templates: input config containing templates
    :raises:
        ValidationError: if templates don't follow the schema.
    """
    validator = Draft7Validator(_SCHEMA)
    if errors := sorted(validator.iter_errors(templates), key=lambda x: x.path):
        raise ValidationError(errors)
