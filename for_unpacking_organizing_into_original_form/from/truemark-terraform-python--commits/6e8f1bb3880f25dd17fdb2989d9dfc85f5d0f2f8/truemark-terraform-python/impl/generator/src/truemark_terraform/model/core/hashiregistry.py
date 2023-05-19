from __future__ import annotations

import uuid
from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json
from truemark_terraform.model.core.hashimetaobj import HashiObj

## Impl inspired, referenced From:
# https://python-patterns.guide/gang-of-four/singleton/
# https://python-patterns.guide/python/module-globals/
#
# For now we'll use the Singleton - I understand that 
# better and know how to incorporate into the design. 
#  -TODO: Go Back and review "Global Object Pattern - A more pythonic singleton"
#

## Maybe necessary/convenient to treat as both, order it was added, or by type, or by reference, etc...
class RegisteredHashiObj():
    def __init__(self, ordinal: int = None, hashi_object: HashiObj = None, hcl_text: str = None,
                       recursion_level: int = None, 
                       referenced_by: list[RegisteredHashiObj] = [], 
                       references: list[RegisteredHashiObj] = []) -> None:
        # id, name_id, and type are pass throughs
        self.id = hashi_object.id
        self.name_id = hashi_object.name_id
        self.type = hashi_object.HASHI_TYPE

        self.hashi_object = hashi_object
        self.ordinal = ordinal
        self.hcl_text = hcl_text
        self.recursion_level = recursion_level
        self.referenced_by = referenced_by
        self.references = references

    def __str__(self):
        return f'RegisteredHashiObj(id: {self.id}, name_id: {self.name_id}, type: {self.type}, hashi_object: {self.hashi_object}, \n\t \
                                    ordinal: {self.ordinal}, hcl_text: {self.hcl_text} recursion_level: {self.recursion_level}, \n\t \
                                    referenced_by: {self.referenced_by}, references: {self.references})'

    def __repr__(self):
        return f'RegisteredHashiObj(id={self.id}, name_id={self.name_id}, type={self.type}, hashi_object={self.hashi_object}, ordinal={self.ordinal}, hcl_text={self.hcl_text}, recursion_level={self.recursion_level}, referenced_by={self.referenced_by}, references={self.references})'

    def to_dict(self) -> dict:
        d = dict()
        d['id'] = self.id
        d['name_id'] = self.name_id
        d['type'] = self.type

        d['hashi_obj'] = self.hashi_obj
        d['ordinal'] = self.ordinal
        d['hcl_text'] = self.hcl_text
        d['recursion_level'] = self.recursion_level
        d['referenced_by'] = self.referenced_by
        d['references'] = self.references
        return d
    
    @staticmethod
    def from_dict(cls, d: dict) -> RegisteredHashiObj:
        r = RegisteredHashiObj(id =             d['id'],
                               name_id =        d['name_id'],
                               type =           d['type'],
                               
                               hashi_obj =      d['hashi_obj'], 
                               ordinal =        d['ordinal'], 
                               hcl_text=        d['hcl_text'],
                               recursion_level = d['recursion_level'], 
                               referenced_by =  d['referenced_by'],
                               references =     d['references'])
        return r
    
    def to_json_dict(self) -> dict:
        return self.to_dict()
    
    def to_json(self) -> str:
        return serialize_obj_to_json(self)
    
    @staticmethod
    def from_json(cls, json_str: str) -> RegisteredHashiObj:
        d = dict_to_json(json_str)
        return RegisteredHashiObj.from_dict(d)

class HashiReg(object):
    _instance: HashiReg = None

    def __init__(self) -> None:
        raise RuntimeError("Call instance instead")

    @classmethod
    def instance(cls) -> HashiReg:
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.hashi_objs = []
            cls._instance.hashi_objs_dict = {}
        return cls._instance

    @staticmethod
    def generate_hashi_id() -> str:
        hashi_obj_uuid = uuid.uuid4() #(uuid.NAMESPACE_URL, 'https://bitbucket.org/truemark/truemark-terraform-python')
        hashi_obj_uuid_str = str(hashi_obj_uuid)
        return str("{" + hashi_obj_uuid_str + "}")

    def reg_hashi(self, hashi_object: HashiObj) -> None:
        if self.hashi_objs == None:  
            self.hashi_objs = []
        if self.hashi_objs_dict == None:
            self.hashi_objs_dict = {}
        
        if not self.hashi_objs_dict.get(hashi_object.name_id):
            reg_hashi_obj = RegisteredHashiObj(ordinal = len(self.hashi_objs), 
                                        hashi_object = hashi_object, hcl_text = "", recursion_level = 0, referenced_by = None, references = None)
            self.hashi_objs_dict[reg_hashi_obj.name_id] = reg_hashi_obj 
            self.hashi_objs.append(reg_hashi_obj)
        else:
            print("HASHI ALREADY REGISTERED!!!")
            raise Exception("HashiAlreadyRegisteredException", 
               'the HashiObj provided (id: {id}, name_id: {name_id} has already been registered)'.format(id = hashi_object.id, name_id = hashi_object.name_id))

    def dereg_hashi(self, obj):
        print("TODO!")
        pass 

    def get_hashis(self) -> list[RegisteredHashiObj]:
        return self.hashi_objs
    
    def get_hashi_by_id(self, id) -> RegisteredHashiObj:
        for hashi_obj in self.hashi_objs:
            if hashi_obj.id == id:
                return hashi_obj

    def get_hashi_by_name_id(self, name_id) -> RegisteredHashiObj:
        return self.hashi_objs_dict.get(name_id)

    def clear_registry(self):
        self.hashi_objs_dict = {}
        self.hashi_objs = []