from __future__ import annotations

from truemark_terraform.model.core.hashimetaobj import HashiObj
from truemark_terraform.model.core.hashiregistry import HashiReg
from truemark_terraform.utils.json_utils import serialize_obj_to_json, dict_to_json
# from truemark_terraform.utils.hcl.hcl_utils import to_hcl as gen_hcl

def setup_parent_child():
    # recur-descent on each obj. Iff O.Type === Resource, set parent and, descend into it...
    pass 

class Resource(HashiObj): 
    HASHI_TYPE = "RESOURCE"

    def __init__(self, *args, **kwargs):
        super().__init__(HashiReg.generate_hashi_id(), 
                         "{type} {type_name} {name}".format(type = self.HASHI_TYPE.lower(), type_name = args[0], name = args[1]))
        if not len(args) == 2:
            print("error - args must be two in len()")
        self.resource_type_name = args[0]
        self.resource_inst_name = args[1]
        # TODO: Figure this out: handle TypeList, TypeSet, TypeMap, what others were there again? The nature of inneras is, if this is a child property of another resource, how do we serialize to/from HCL. How should/do we validate it if/when necessary? Etc... Will we need a parent property if this is populated? 
        if len(args) == 3:
            self.resource_inneras = args[3] 
        self.resource_properties = kwargs
        
        HashiReg.instance().reg_hashi(self)

    def hashi_type(cls) -> str:
        return cls.HASHI_TYPE

    def property(self, key: str) -> object:
        return self.resource_properties.get(key)

    def to_dict(self) -> dict:
        d = dict()
        d['hashi_type'] = self.HASHI_TYPE
        d['resource_type_name'] = self.resource_type_name
        d['resource_inst_name'] = self.resource_inst_name
        for prop_key in self.resource_properties.keys():
            prop_val = self.resource_properties.get(prop_key)
            d[str(prop_key)] = prop_val
        return d

    @staticmethod
    def from_dict(cls, d: dict) -> Resource:
        if not d['hashi_type'] == Resource.HASHI_TYPE:
            raise RuntimeError("HASHI_TYPE's dont match. transpose methods can only be called within same-type structures.")
        t_name = d.pop(['resource_type_name'])
        i_name = d.pop(['resource_inst_name'])
        props = dict()
        for prop_key in d.keys():
            props[str(prop_key)] = d[prop_key]
        r = Resource()
        r.resource_type_name = t_name
        r.resource_inst_name = i_name
        r.resource_properties = props
        return r

    def to_json_dict(self) -> dict:
        return self.to_dict()

    def to_json(self) -> str:
        return serialize_obj_to_json(self)

    @staticmethod
    def from_json(cls, json_str: str) -> Resource:
        d = dict_to_json(json_str)
        return Resource.from_dict(d)

    # def to_hcl(self) -> str:
    #     # body = ""
    #     # for prop_key in self.resource_properties.keys():
    #     #     body += "  " + prop_key + " = " + hcl_utils.to_hcl(self.resource_properties.get(prop_key)) + "\n"
    #     # header = "resource \"{resource_type_name}\" \"{resource_inst_name}\" "
    #     # header = header.format(resource_type_name = self.resource_type_name, resource_inst_name = self.resource_inst_name)
    #     # header += "{\n"
    #     # footer = "}\n"
    #     # return str(header + body + footer)
    #     hcl = gen_hcl([self])
    #     return hcl

    # @staticmethod
    # def from_hcl(cls, hashi_str: str) -> Resource:
    #     raise RuntimeError("We dont really do this kind of stuff yet... Do we need to? -> babbott@truemark.io")