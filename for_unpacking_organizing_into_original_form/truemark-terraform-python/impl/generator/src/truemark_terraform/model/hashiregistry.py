from __future__ import annotations

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

    def __init__(self, ordinal: int, type: str, id: str, obj: object, referenced_by:list[RegisteredHashiObj], references:list[RegisteredHashiObj]) -> None:
        self.ordinal = ordinal
        self.type = type
        self.id = id
        self.obj = obj
        self.referenced_by = referenced_by
        self.references = references

class HashiReg(object):
    _instance = None

    def __init__(self) -> None:
        raise RuntimeError("Call instance instead")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.hashi_objs = []
        return cls._instance

    def reg_hashi(self, obj) -> None:
        if self.hashi_objs == None:   # unreachable but, ah-well... 
            self.hashi_objs = []
        hash_obj = RegisteredHashiObj(ordinal = len(self.hashi_objs), type = obj.HASHI_TYPE, id = "", obj = obj, referenced_by = None, references = None) 
        self.hashi_objs.append(hash_obj)

    def dereg_hashi(self, obj):
        print("TODO!")
        pass 

    def get_hashis(self):
        return self.hashi_objs

