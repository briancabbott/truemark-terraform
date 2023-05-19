
from __future__ import annotations

from truemark_terraform.model.core.hashimetaobj import HashiObj
from truemark_terraform.model.core.hashiregistry import HashiReg
from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json

# Using Data Sources
# A data source is accessed via a special kind of resource known as a data 
# resource, declared using a data block:
# 
# data "aws_ami" "example" {
#   most_recent = true
# 
#   owners = ["self"]
#   tags = {
#     Name   = "app-server"
#     Tested = "true"
#   }
# }
# 
# A data block requests that Terraform read from a given data source ("aws_ami") 
# and export the result under the given local name ("example"). The name is used 
# to refer to this resource from elsewhere in the same Terraform module, but has 
# no significance outside of the scope of a module.
# 
# The data source and name together serve as an identifier for a given resource 
# and so must be unique within a module.
#
class Data(HashiObj): 
    HASHI_TYPE = "DATA"
    
    def __init__(self, *args, **kwargs):
        # TODO: On load, we need to capture a reference to the data-element from 
        #       either the terraform-registry or a local source.
        super().__init__(HashiReg.generate_hashi_id(), 
                         "{type} {source} {name}".format(type = self.HASHI_TYPE.lower(), source = args[0], name = args[1]))
        if not len(args) == 2:
            print("error - args must be two in len()")
        self.data_source = args[0]
        self.data_name = args[1]
        self.data_properties = kwargs

        HashiReg.instance().reg_hashi(self)

    def hashi_type(cls) -> str:
        return cls.HASHI_TYPE

    def property(self, key: str) -> object:
        return self.module_properties.get(key)

    def to_dict(self) -> dict:
        d = dict()
        d['hashi_type'] = self.HASHI_TYPE
        d['data_source'] = self.data_source
        d['data_name'] = self.data_name
        for prop_key in self.data_properties.keys():
            prop_val = self.data_properties.get(prop_key)
            d[str(prop_key)] = prop_val
        return d

    @staticmethod
    def from_dict(cls, d: dict) -> Data:
        if not d['hashi_type'] == Data.HASHI_TYPE:
            raise RuntimeError("HASHI_TYPE's dont match. transpose methods can only be called within same-type structures.")
        source = d.pop(['data_source'])
        name = d.pop(['data_name'])
        props = dict()
        for prop_key in d.keys():
            props[str(prop_key)] = d[prop_key]
        d = Data([source, name], props)
        return d

    def to_json_dict(self) -> dict:
        return self.to_dict()

    def to_json(self) -> str:
        return serialize_obj_to_json(self)

    @staticmethod
    def from_json(cls, json_str: str) -> Data:
        d = dict_to_json(json_str)
        return Data.from_dict(d)
