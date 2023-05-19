from __future__ import annotations

from enum import Enum
from io import StringIO

import json

from terraform_schema.model.data_object import DataObject, DataField
from terraform_schema.model.resource_object import ResourceObject
from terraform_schema.model.provider_object import ProviderObject

##
# Per-Provider Schema Object
class Schema():
    def __init__(self, provider_name: str = None,  
                       resources: dict[str, ResourceObject] = {}, 
                       data_sources: dict[str, DataObject] = {}):
        self.provider_name = provider_name
        self.resources = resources
        self.data_sources = data_sources

    def to_python(self):
        pass

    def __dict__(self) -> dict:
        d = {}
        d['provider_name'] = self.provider_name
        d['resources'] = self.resources
        d['data_sources'] = self.data_sources
        return d

    def to_dict(self) -> dict:
        return self.__dict__()

    @staticmethod
    def from_dict(d: dict) -> Schema:
        ps = Schema()
        ps.provider_name = d['provider_name']
        ps.resources = d['resources']
        ps.data_sources = d['data_sources']
        return ps

    def to_json(self) -> str:        
        json_str = json.dumps(self.to_dict())
        return json_str

    @staticmethod
    def from_json(json_str: str) -> Schema:
        json_dict = json.loads(json_str)
        return Schema.from_dict(json_dict)