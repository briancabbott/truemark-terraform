from __future__ import annotations

from truemark_terraform.model.core.hashimetaobj import HashiObj
from truemark_terraform.model.core.hashiregistry import HashiReg
from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json

## 
# A note on Provider's Name-ID: for a provider object the name-id is a composite value of:
#    "\"provider\" provider-name provider-source provider-version" 
# so, for the provider demonstrated below it would be:
#    "provider" provider-name ("aws") provider-source ("hashicorp/aws") provider-version ("~> 3.27") 
# or: 
#    "provider aws hashicorp/aws ~> 3.27" 
# from the HCL text:
# 
#    terraform {
#      required_providers {
#        aws = {
#          source  = "hashicorp/aws"
#          version = "~> 3.27"
#        }
#      }
#    }
#
#    provider "aws" {
#      profile = "default"
#      region  = "us-west-1"
#    }
# # provider-name-id: 
# ...
# }
class Provider(HashiObj): 
    HASHI_TYPE = "PROVIDER"

    def __init__(self, *args, **kwargs):
        super().__init__(HashiReg.generate_hashi_id(), 
                         "{provider} {provider_name} {provider_source} {provider_version}"
                         .format(provider = self.HASHI_TYPE.lower(), 
                                 provider_name = args[0], 
                                 provider_source = args[1], 
                                 provider_version=args[2]))
        if not len(args) == 3:
            print("error - args must be three in len()")
        self.provider_name = args[0]
        self.provider_source = args[1]
        self.provider_version = args[2]
        self.provider_properties = kwargs
        HashiReg.instance().reg_hashi(self)

    def __str__(self) -> str:
        return self.to_json()
    
    def __repr__(self) -> str:
        return f'Provider(provider_name={self.provider_name}, provider_source={self.provider_source}, provider_version={self.provider_version}, provider_properties={self.provider_properties})'

    def hashi_type(cls) -> str:
        return cls.HASHI_TYPE

    def property(self, key: str) -> object:
        return self.provider_properties.get(key)

    def to_dict(self) -> dict:
        d = dict()
        d['hashi_type'] = self.HASHI_TYPE
        d['provider_name'] = self.provider_name
        d['provider_source'] = self.provider_source
        d['provider_version'] = self.provider_version
        for prop_key in self.provider_properties.keys():
            prop_val = self.provider_properties.get(prop_key)
            d[str(prop_key)] = prop_val
        return d

    @staticmethod
    def from_dict(cls, d: dict) -> Provider:
        if not d['hashi_type'] == Provider.HASHI_TYPE:
            raise RuntimeError("HASHI_TYPE's dont match. transpose methods can only be called within same-type structures.")
        name = d.pop(['provider_name'])
        source = d.pop(['provider_source'])
        version = d.pop(['provider_version'])
        props = dict()
        for prop_key in d.keys():
            props[str(prop_key)] = d[prop_key]
        p = Provider()
        p.provider_name = name
        p.provider_source = source
        p.provider_version = version
        return p

    def to_json_dict(self) -> dict:
        return self.to_dict()

    def to_json(self) -> str:
        return serialize_obj_to_json(self)

    @staticmethod
    def from_json(cls, json_str: str) -> Provider:
        d = dict_to_json(json_str)
        return Provider.from_dict(d)