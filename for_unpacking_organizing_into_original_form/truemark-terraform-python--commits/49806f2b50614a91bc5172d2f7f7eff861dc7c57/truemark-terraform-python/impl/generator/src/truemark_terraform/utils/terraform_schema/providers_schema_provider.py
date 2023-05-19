
import subprocess
import pathlib
import os
import json

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
        provider_def = providers_schema['provider']
        resources_def = providers_schema['resource_schemas']

        ## Process Data-Source 
        data_sources_def = providers_schema['data_source_schemas']
        for data_source_key in data_sources_def.keys():
            data_source = data_sources_def[data_source_key]
            print("key: " + data_source_key)
            data_source_properties = data_source['block']['attributes']
            for prop_key in data_source_properties.keys():
                print("\t" + prop_key)
                property_attributes = data_source_properties[prop_key]
                for attr in property_attributes.keys():
                    print("\t\t" + attr + " :: " + str(property_attributes[attr]))


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