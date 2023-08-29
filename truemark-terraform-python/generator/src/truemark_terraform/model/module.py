
from __future__ import annotations

from truemark_terraform.model.core.hashimetaobj import HashiObj
from truemark_terraform.model.core.hashiregistry import HashiReg
from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json

class Module(HashiObj): 
    HASHI_TYPE = "MODULE"
    
    def __init__(self, *args, **kwargs):
        super().__init__(HashiReg.generate_hashi_id(), 
                         "{type} {name} {source} {version}".format(type = self.HASHI_TYPE.lower(), name = args[0], 
                                                                   source = args[1], version = args[2]))
        if not len(args) == 3:
            print("error - args must be two in len()")
        self.module_name = args[0]
        self.module_source = args[1]
        self.module_version = args[2] 
        self.module_properties = kwargs
        HashiReg.instance().reg_hashi(self)

    def hashi_type(cls) -> str:
        return cls.HASHI_TYPE

    def property(self, key: str) -> object:
        return self.module_properties.get(key)

    def to_dict(self) -> dict:
        d = dict()
        d['hashi_type'] = self.HASHI_TYPE
        d['module_name'] = self.module_name
        d['module_source'] = self.module_source
        d['module_version'] = self.module_version 
        for prop_key in self.module_properties.keys():
            prop_val = self.module_properties.get(prop_key)
            d[str(prop_key)] = prop_val
        return d

    @staticmethod
    def from_dict(cls, d: dict) -> Module:
        if not d['hashi_type'] == Module.HASHI_TYPE:
            raise RuntimeError("HASHI_TYPE's dont match. transpose methods can only be called within same-type structures.")
        name = d.pop(['module_name'])
        source = d.pop(['module_source'])
        version = d.pop(['module_version'])
        props = dict()
        for prop_key in d.keys():
            props[str(prop_key)] = d[prop_key]
        m = Module([name, source, version], props)
        return m

    def to_json_dict(self) -> dict:
        return self.to_dict()

    def to_json(self) -> str:
        return serialize_obj_to_json(self)

    @staticmethod
    def from_json(cls, json_str: str) -> Module:
        d = dict_to_json(json_str)
        return Module.from_dict(d)