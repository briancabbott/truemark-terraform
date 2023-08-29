from __future__ import annotations

import subprocess
import pathlib
import os
import json
import glob

import logging
from typing import MutableMapping

from terraform_schema.model.data_object import DataObject, DataField
from terraform_schema.model.schema import Schema
from terraform_schema.model.type import Type
from terraform_schema.model.provider_object import ProviderObject
from terraform_schema.model.resource_object import ResourceObject, ResourceAttribute

# class ProvidersSchemaJson:
#     format_version = ""
#     provider_schemas = {}

# class ProviderSchema():
#     provider
#     resource_schemas
#     data_source_schemas

##
# The Provider of the Schema for the Provider..
#
class TerraformSchemaProvider():
    def __init__(self, terraform_working_directory: str) -> None:
        self.terraform_working_directory = terraform_working_directory

    def acquire_schema_for_script(self):
        twd = pathlib.Path(self.terraform_working_directory)
        twd_path = twd.resolve()
        logging.debug("TerraForm Working Directory: {twd_path}".format(twd_path=twd_path.__str__()))
        
        os.chdir(str(twd_path))
        if not self.is_terraform_initd():
            logging.debug("TerraForm init needed. Executing now...")
            process_out = subprocess.run(["terraform", "init"], stdout=subprocess.PIPE)
            logging.debug(process_out.stdout)

        process_out = subprocess.run(["terraform", "providers", "schema", "-json"], stdout=subprocess.PIPE)
        json_text = process_out.stdout
        
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            with open(self.terraform_working_directory + "/providers_schema.json", "w") as file:
                file.write(str(json_text))

        # print(tf_schema)
        # if isinstance(tf_schema, dict):
        #     self.print_keys(tf_schema)
        tf_schema = json.loads(json_text)
        providers_dict = tf_schema['provider_schemas']
        schemas = []
        for provider in providers_dict.keys():
            providers_schema = providers_dict[provider]
            schemas.append(self.process_provider_schema(providers_schema))

        python_dist_files = self.generate_python_dists_for_schemas(schemas)
        

    def is_terraform_initd(self):
        terraform_initd = False
        if os.path.isdir(self.terraform_working_directory):
            tf_files = glob.glob(self.terraform_working_directory + "/*.tf")
            if len(tf_files) != 1:
                raise Exception("Only 1 .tf script per directory currently supported")
            if len(glob.glob(self.terraform_working_directory + "/.terraform.lock.hcl")) == 1 and len(glob.glob(self.terraform_working_directory + "/.terraform")) == 1:
                terraform_initd = True
        else:
            raise Exception("TerraForm Working Directory does not exist")
        return terraform_initd

    ## 
    # Process Providern Schema...
    #
    def process_provider_schema(self, providers_schema) -> Schema:
        provider_def = providers_schema['provider']
        prv_obj = self.produce_provider_object(provider_def)
        resources_def = providers_schema['resource_schemas']
        rs_objs = self.produce_resource_objects(resources_def)
        data_sources_def = providers_schema['data_source_schemas']
        ds_objs = self.produce_data_source_objects(data_sources_def)

        schema = Schema(provider = prv_obj, resources = rs_objs, data_sources = ds_objs)
        return schema

    def produce_provider_object(self, provider_dict):
        print(json.dumps(provider_dict, indent=4))

    def produce_resource_objects(self, resource_dict):
        json_text = json.dumps(resource_dict, indent=4)
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            with open(self.terraform_working_directory + "/resources_schema.json", "w") as file:
                file.write(str(json_text))

        resources = []
        for resource_key in resource_dict.keys():
            resource = resource_dict[resource_key]
            rs_val = resource['block']['attributes']

            attributes = []
            for attr_name in rs_val.keys():
                attr_props = rs_val[attr_name]
                if isinstance(attr_props, dict):
                    ttype = attr_props.pop('type') if 'type' in attr_props else None
                    computed = attr_props.pop('computed') if 'computed' in attr_props else None
                    optional = attr_props.pop('optional') if 'optional' in attr_props else None
                    attr_type = Type.getTypeFromStr(str(ttype))
                    attr_def = ResourceAttribute(attr_name = attr_name, attr_type = attr_type, computed = computed, optional = optional)
                    attributes.append(attr_def)
            resources.append(ResourceObject(name = resource_key, attributes = attributes))
        return resources

    def produce_data_source_objects(self, data_sources_dict: dict) -> list[DataObject]:
        logging.debug("STARTING: data_sources_dict")
        logging.debug(json.dumps(data_sources_dict, indent=4))
        logging.debug("ENDING: data_sources_dict")
        
        data_sources = []
        for data_source_key in data_sources_dict.keys():
            data_source = data_sources_dict[data_source_key]
            data_source = DataObject(name = str(data_source_key), fields = self.produce_data_source_object_fields(data_source))
            
            data_sources.append(data_source)
            
            # data_source_properties = data_source['block']['attributes']
            # for data_source_property in data_source_properties.keys():
            #     # print("\t" + data_source_property)

            #     ProviderSchemaDataFieldDefinition(field_name = data_source_property, 
            #                                       field_type = ProviderSchemaFieldTypeKind., 
            #                                       computed, 
            #                                       optional)
            #     property_attributes = data_source_properties[data_source_property]
            #     for attr in property_attributes.keys():
            #         print("\t\t" + attr + " :: " + str(property_attributes[attr]))
        return data_sources

    def produce_data_source_object_fields(self, data_source_dict: dict) -> list[DataField]:
        ds_val = data_source_dict['block']['attributes']
        fields = []

        for field_name in ds_val.keys():
            field_props = ds_val[field_name]
            if isinstance(field_props, dict):
                ttype = field_props.pop('type') if 'type' in field_props else None
                computed = field_props.pop('computed') if 'computed' in field_props else None
                optional = field_props.pop('optional') if 'optional' in field_props else None
                field_type = Type.getTypeFromStr(str(ttype))
                field_def = DataField(field_name = field_name, field_type = field_type, computed = computed, optional = optional)
                fields.append(field_def)    
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

    def generate_python_dists_for_schemas(self, schemas: list[Schema]) -> MutableMapping[str, 
                                                                            MutableMapping[str, 
                                                                                MutableMapping[str, str]]]:
        dists = {}
        for sch in schemas:
            dists[sch.provider_name] = self.generate_python_dist(sch)
        return dists

    def generate_python_dist(self, sch: Schema) -> MutableMapping[str, MutableMapping[str, str]]:
        dist_artifacts = {}        
        dist_artifacts['resources'] = {}
        for resource in sch.resources:
            py = resource.to_python()
            dist_artifacts['resources'][resource.name] = py
        dist_artifacts['data_sources'] = {}
        for data_obj in sch.data_sources:
            py = data_obj.to_python()
            dist_artifacts['data_sources'][data_obj.name] = py
        return dist_artifacts

