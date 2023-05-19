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

    @staticmethod
    def getFieldTypeKindFromStr(type_kind_name: str) -> ProviderSchemaFieldTypeKind:
        if type_kind_name == None:
            # TODO: Is this an error?
            return None

        lowd_type_kind_name = type_kind_name.lower()
        
        if lowd_type_kind_name == "string":
            return ProviderSchemaFieldTypeKind.String
        elif lowd_type_kind_name == "bool" or lowd_type_kind_name == "false" or lowd_type_kind_name == "true":
            return ProviderSchemaFieldTypeKind.Boolean
        elif lowd_type_kind_name.startswith("['list', ['object',"):
            return ProviderSchemaFieldTypeKind.List_of_Objects
        else:
            # TODO: Have a decent catch-all
            print("UNKNOWN TYPE!!!! TypeStr was: " + str(type_kind_name))


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