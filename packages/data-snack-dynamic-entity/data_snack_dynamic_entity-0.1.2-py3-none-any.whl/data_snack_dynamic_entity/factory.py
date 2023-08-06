import builtins
from data_snack.entities import Entity
from dataclasses import dataclass, field, make_dataclass
from typing import Dict, Type, Any, List, Optional

from data_snack_dynamic_entity.types import EntitySchema, FieldSchema, EntityTemplates
from data_snack_dynamic_entity.validate import validate_entity_templates


@dataclass
class EntityFactory:
    types_mapping: Dict[str, Any] = field(
        default_factory=dict
    )  # this will store custom mappings

    def load_entities(self, templates: EntityTemplates) -> Dict[str, Type]:
        """
        Creates new Entity types based on provided config.
        Config should contain a valid template that is created according to the schema (see README).

        :param templates: input config containing templates
        :returns: a dictionary with all created Entity types
        """

        validate_entity_templates(templates)
        return {
            entity_name: self._create_entity(entity_name, entity_schema)
            for entity_name, entity_schema in templates.items()
        }

    def _create_entity(self, entity_name: str, entity_schema: EntitySchema) -> Type:
        """
        Creates entity of given name according to given schema.
        :param entity_name: new entity name
        :param entity_schema: new entity schema
        :return: new entity type
        """
        fields = []
        fields_with_defaults = []
        keys = []
        excluded_fields = []
        for field_name, field_schema in entity_schema["properties"].items():
            field_type = self._get_entity_type(field_schema["type"])

            if field_schema.get("key"):
                keys.append(field_name)
            if field_schema.get("excluded"):
                excluded_fields.append(field_name)
            if field_schema.get("optional"):
                field_type = Optional[field_type]
            if "default" in field_schema:
                fields_with_defaults.append(
                    (field_name, field_type, field(default=field_schema["default"]))
                )
            else:
                fields.append((field_name, field_type))

        entity_template = self._create_entity_template(
            entity_name=entity_name, keys=keys, excluded_fields=excluded_fields
        )
        return make_dataclass(
            entity_name,
            fields + fields_with_defaults,
            bases=(entity_template,),
            namespace={"__module__": __name__},
        )

    def _get_entity_type(self, name: str) -> Type:
        try:
            t = getattr(builtins, name)
            if not isinstance(t, type):
                raise ValueError(name)
            return t
        except AttributeError as e:
            if t := self.types_mapping.get(name):
                return t
            raise ValueError(name) from e

    @staticmethod
    def _create_entity_template(
        entity_name: str, keys: List[str], excluded_fields: List[str]
    ) -> Type:
        return type(
            f"{entity_name}Template",
            (Entity,),
            {
                "Meta": type(
                    "Meta",
                    (object,),
                    {"keys": keys, "excluded_fields": excluded_fields},
                )
            },
        )


def load_entities(
    templates: EntityTemplates, types_mapping: Dict[str, Any] = None
) -> Dict[str, Type]:
    if not types_mapping:
        types_mapping = {}
    return EntityFactory(types_mapping).load_entities(templates)
