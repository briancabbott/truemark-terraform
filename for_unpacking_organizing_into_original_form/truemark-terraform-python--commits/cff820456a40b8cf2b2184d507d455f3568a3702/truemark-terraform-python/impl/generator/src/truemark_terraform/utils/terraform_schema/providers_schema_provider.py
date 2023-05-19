from __future__ import annotations

import subprocess
import pathlib
import os
import json

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
        new_ds_objs = self.produce_data_source_objects(data_sources_def)
        # Now, add all these into the current sys-path, test that they are code-accessible:

    def produce_provider_objects(self, provider_dict):
        pass

    def produce_resource_objects(self, resource_dict):
        pass

    def produce_data_source_objects(self, data_sources_dict: dict):
        for data_source_key in data_sources_dict.keys():
            data_source = data_sources_dict[data_source_key]
            print(data_source_key)
            self.produce_data_source_object(data_source)

            # print("key: " + data_source_key)

            # data_source_properties = data_source['block']['attributes']
            # for prop_key in data_source_properties.keys():
            #     # print("\t" + prop_key)
            #     property_attributes = data_source_properties[prop_key]
            #     for attr in property_attributes.keys():
            #         # print("\t\t" + attr + " :: " + str(property_attributes[attr]))
            #         pass

    def produce_data_source_object(self, data_source_dict: dict):
        ds_val = data_source_dict['block']['attributes']

        for ds_key in ds_val.keys():
            print("\tkey name: " + ds_key)
            fields = ds_val[ds_key]
            if isinstance(fields, dict):
                print("\t\tDICTIONARY!!!")
                ttype = fields.pop('type') if 'type' in fields else None
                computed = fields.pop('computed') if 'computed' in fields else None
                optional = fields.pop('optional') if 'optional' in fields else None
                fields.pop('type')
                fields.pop('computed')
                fields.pop('optional')
                        
            else: 
                print("\t\tVar")


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