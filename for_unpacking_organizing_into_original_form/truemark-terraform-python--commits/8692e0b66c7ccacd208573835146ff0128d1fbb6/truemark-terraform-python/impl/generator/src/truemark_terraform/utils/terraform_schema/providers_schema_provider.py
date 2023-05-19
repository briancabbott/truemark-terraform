from __future__ import annotations

import subprocess
import pathlib
import os
import json

# from .truemark_terraform import ProviderSchemaDataFieldDefinition, ProviderSchemaFieldTypeKind


from enum import Enum
# from io import StringIO


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

    def to_python(self):
        "class "

class ProviderSchemaDataFieldDefinition:    
    def __init__(self, field_name: str = None, field_type: ProviderSchemaFieldTypeKind = None, computed: bool = None, optional: bool = None) -> None:
        self.field_name = field_name
        self.field_type = field_type
        self.computed = computed
        self.optional = optional


##
# The Provider of the Schema for the Provider..
#
class TerraformSchemaProvider():

    def __init__(self, terraform_working_directory: str) -> None:
        self.terraform_working_directory = terraform_working_directory 

    def acquire_schema_for_script(self):
        # terraform providers schema -json
        twd = pathlib.Path(self.terraform_working_directory)
        os.chdir(str(twd.resolve().__str__()))
        process_out = subprocess.run(["terraform", "providers", "schema", "-json"], stdout=subprocess.PIPE)
        json_text = process_out.stdout
        tf_schema = json.loads(json_text)
        # print(tf_schema)
        # if isinstance(tf_schema, dict):
        #     self.print_keys(tf_schema)
        providers_dict = tf_schema['provider_schemas']
        for provider in providers_dict.keys():
            print(provider)
            providers_schema = providers_dict[provider]
            self.process_provider_schema(providers_schema)
        # print(type(providers_dict))

    def process_provider_schema(self, providers_schema):
        ## Process Providern Schema...
        provider_def = providers_schema['provider']
        new_prv_objs = self.produce_provider_objects(provider_def)

        ## Process Resources Schema...
        resources_def = providers_schema['resource_schemas']
        new_rs_objs = self.produce_resource_objects(resources_def)

        ## Process Data-Sources Schema...
        data_sources_def = providers_schema['data_source_schemas']
        print("Data Source Production started....")
        new_ds_objs = self.produce_data_source_objects(data_sources_def)
        print("Data Source Production finished....")
        len(new_ds_objs)
        # Now, add all these into the current sys-path, test that they are code-accessible:

    def produce_provider_objects(self, provider_dict):
        pass

    def produce_resource_objects(self, resource_dict):
        pass

    def produce_data_source_objects(self, data_sources_dict: dict) -> list[ProviderSchemaDataObjectDefinition]:
        data_source_object_defs = []
        for data_source_key in data_sources_dict.keys():
            data_source = data_sources_dict[data_source_key]
            print("DATA SOURCE KEY")
            print(data_source_key)
            data_source_object_def = ProviderSchemaDataObjectDefinition()
            data_source_object_def.data_object_name = str(data_source_key)
            data_source_object_def.data_fields = self.produce_data_source_object_fields(data_source)
            data_source_object_defs.append(data_source_object_def)
        return data_source_object_defs
            # print("key: " + data_source_key)

            # data_source_properties = data_source['block']['attributes']
            # for prop_key in data_source_properties.keys():
            #     # print("\t" + prop_key)
            #     property_attributes = data_source_properties[prop_key]
            #     for attr in property_attributes.keys():
            #         # print("\t\t" + attr + " :: " + str(property_attributes[attr]))
            #         pass

    def produce_data_source_object_fields(self, data_source_dict: dict) -> list[ProviderSchemaDataFieldDefinition]:
        ds_val = data_source_dict['block']['attributes']
        print(ds_val)
        keys_len = len(list(ds_val.keys()))
        print(keys_len)
        # input()
        fields = []
        for field_name in ds_val.keys():
            field_props = ds_val[field_name]
            if isinstance(field_props, dict):
                ttype = field_props.pop('type') if 'type' in field_props else None
                computed = field_props.pop('computed') if 'computed' in field_props else None
                optional = field_props.pop('optional') if 'optional' in field_props else None
                
                field_type = ProviderSchemaFieldTypeKind.getFieldTypeKindFromStr(str(ttype))

                field_def = ProviderSchemaDataFieldDefinition(field_name = field_name, field_type = field_type,
                                                            computed = computed, optional = optional)
                fields.append(field_def)
            else: 
                print("\t\tVar TYPE!!!")
        return fields


    def print_keys(self, tfs: dict, indent:int = 0):
        dict_keys = []
        for key in tfs.keys():
            val = tfs[key]
            if not isinstance(val, dict):
                ind_lvl = "\t" * indent
                print(ind_lvl + key + ":  " + str(val))
            else:
                dict_keys.append((key, val))
        for dk in dict_keys:
            # dv = tfs[dk]
            ins = "\t" * indent
            print(ins + "obj: " + dk[0])
            self.print_keys(dk[1], indent + 1)

if __name__ == "__main__":
    TerraformSchemaProvider(".").acquire_schema_for_script()