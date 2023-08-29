from __future__ import annotations

import json

from collections.abc import Sequence
from terraform_schema.model.type import Type

class ResourceObject():
    def __init__(self, name: str = None, attributes: Sequence[ResourceAttribute] = None) -> None:
        self.name = name
        # self.version = version
        self.attributes = attributes

    def to_python(self) -> str:
        pass

    def __dict__(self) -> dict:
        d = {}
        d['name'] = self.name
        d['version'] = self.version
        dict_attrs = []
        for a in self.attributes:
            dict_attrs.append(a.to_dict())
        d['attributes'] = dict_attrs
        return d

    def to_dict(self) -> dict:
        return self.__dict__()

    @staticmethod
    def from_dict(d: dict) -> ResourceAttribute:
        return ResourceAttribute(name = d['name'], version = d['version'], attributes = d['attributes'])
        
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_str: str) -> ResourceAttribute:
        return ResourceAttribute.from_dict(json.loads(json_str))

class ResourceAttribute():
    def __init__(self, attr_name: str = None, 
                       attr_type: Type = None, 
                       computed: bool = None, 
                       optional: bool = None) -> None:
        self.attr_name = attr_name
        self.attr_type = attr_type
        self.computed = computed
        self.optional = optional
        
    def to_python(self) -> str:
        pass

    def __dict__(self) -> dict:
        d = {}
        d['attr_name'] = self.attr_name
        d['attr_type'] = self.attr_type
        d['computed'] = self.computed
        d['optional'] = self.optional
        return d

    def to_dict(self) -> dict:
        return self.__dict__()

    @staticmethod
    def from_dict(d: dict) -> ResourceAttribute:
        return ResourceAttribute(attr_name = d['attr_name'], 
                                 attr_type = d['attr_type'], 
                                 computed = d['computed'], 
                                 optional = d['optional'])
        
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_str: str) -> ResourceAttribute:
        d = json.loads(json_str)
        return ResourceAttribute.from_dict(d)