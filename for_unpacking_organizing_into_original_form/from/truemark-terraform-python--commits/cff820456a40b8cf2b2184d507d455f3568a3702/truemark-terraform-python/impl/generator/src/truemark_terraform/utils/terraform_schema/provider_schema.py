from __future__ import annotations

from enum import Enum
from io import StringIO


# class ProvidersSchemaJson:

#     format_version = ""
#     provider_schemas = {}


# class ProviderSchema():
#     provider
#     resource_schemas
#     data_source_schemas


class ProviderSchemaFieldTypeKind(Enum):
    String = "STRING"
    Boolean = "BOOL"
    Number = "NUMBER"
    List_of_Primitives = "LIST_OF_PRIMITIVES"
    List_of_Objects = "LIST_OF_OBJECTS"


class ProviderSchemaDataObjectDefinition:
    def __init__(self, data_object_name: str = None, data_fields: list[ProviderSchemaDataFieldDefinition] = None):
        self.data_object_name = data_object_name
        self.data_fields = data_fields

class ProviderSchemaDataFieldDefinition:    
    def __init__(self, field_name: str = None, field_type: ProviderSchemaFieldTypeKind = None, computed: bool = None, optional: bool = None) -> None:
        self.field_name = field_name
        self.field_type = field_type
        self.computed = computed
        self.optional = optional