from __future__ import annotations

from collections.abc import Sequence
from typing import List, Tuple

from truemark_terraform.model.core.hashiregistry import RegisteredHashiObj, HashiReg
from truemark_terraform.model.core.hashimetaobj import HashiObj

from truemark_terraform.model.provider import Provider
from truemark_terraform.model.resource import Resource
from truemark_terraform.model.module import Module
from truemark_terraform.model.data import Data

from truemark_terraform.utils.exception_utils import handle_exception
from truemark_terraform.utils.hcl.hcl_generation_config import HCLGen

## 
# Fundamentally handles HCL <=> Python type-system conversions.
# 
#   Python Type System:
#      - Numeric types:     int, float, complex
#      - Sequence types:    str, bytes, bytearray, list, tuple, range
#      - Set types:         set, frozenset
#      - Mapping types:     dict
#
#   TerraForm Type Information:   
#      - https://learn.hashicorp.com/tutorials/terraform/expressions
#      - https://learn.hashicorp.com/tutorials/terraform/variables
#      - https://www.terraform.io/docs/language/expressions/conditionals.html
#      - https://www.terraform.io/docs/language/expressions/dynamic-blocks.html
#      - https://www.terraform.io/docs/language/expressions/for.html
#      - https://www.terraform.io/docs/language/expressions/function-calls.html
#      - https://www.terraform.io/docs/language/expressions/operators.html
#      - https://www.terraform.io/docs/language/expressions/references.html
#      - https://www.terraform.io/docs/language/expressions/splat.html
#      - https://www.terraform.io/docs/language/expressions/strings.html
#      - https://www.terraform.io/docs/language/expressions/type-constraints.html
#      - https://www.terraform.io/docs/language/expressions/types.html
#      - https://www.terraform.io/docs/language/expressions/version-constraints.html
#      - https://www.terraform.io/docs/language/meta-arguments/for_each.html
#      - https://www.terraform.io/docs/language/values/locals.html
#
#   Python <=> HCL Type mappings
#      None                                   => null
#      int, float                             => number
#      str                                    => string
#      bool                                   => bool
#      list, tuple, range, set, frozenset     => list
#      dict                                   => map
#      (*)                                    => *Indices and Attributes
#   *Note: Indices and Attributes currently unsupported.

class HCLConverter():
    def __init__(self, hashi_obj: RegisteredHashiObj = None):
        self.hashi_obj = hashi_obj

    def hcl_for_obj(self):
        # TODO: Finish me... 
        o = self.hashi_obj.hashi_object
        t = self.hasi_obj.type
        
    @staticmethod
    def hcl_for_none(obj: None) -> str:
        return "null"

    @staticmethod
    def hcl_for_bool(obj: bool) -> str:
        return str(obj).lower()

    @staticmethod    
    def hcl_for_int(obj: int) -> str:
        return str(obj)

    @staticmethod
    def hcl_for_float(obj: float) -> str:
        return str(obj)

    @staticmethod
    def hcl_for_complex(obj: complex) -> str:
        raise TypeConversionNotSupportedException()
        
    @staticmethod
    def hcl_for_str(obj: str) -> str:
        ## TODO: Will need to look into more adv issues here...
        return "\"{obj}\"".format(obj=obj) 

    @staticmethod
    def hcl_for_bytes(obj: bytes) -> str:
        raise TypeConversionNotSupportedException()

    @staticmethod
    def hcl_for_bytearray(obj: bytearray) -> str:
        raise TypeConversionNotSupportedException()

    @staticmethod
    def hcl_for_list(obj: list) -> str:
        list_elems = ""
        for e in obj:
            et = PyTypeMap.get_type_map(e)
            cfn = et.get_converter()
            val = cfn(e)
            list_elems += "{val}{sep}".format(val = val, sep = HCLGen.sep) 
        list_elems = list_elems.removesuffix(HCLGen.sep)
        return "[{list_elems}]".format(list_elems = list_elems)

    @staticmethod
    def hcl_for_tuple(obj: tuple) -> str:
        return HCLConverter.hcl_for_list(list(obj))

    @staticmethod
    def hcl_for_range(obj: range) -> str:
        return HCLConverter.hcl_for_list(list(obj))

    @staticmethod
    def hcl_for_set(obj: set) -> str:
        return HCLConverter.hcl_for_list(list(obj))

    @staticmethod
    def hcl_for_frozenset(obj: frozenset) -> str:
        return HCLConverter.hcl_for_list(list(obj))
        
    @staticmethod
    def hcl_for_dict(obj: dict) -> str:
        hcl_map_elems = ""
        for k in obj.keys():
            v = obj.get(k)
            tv = PyTypeMap.get_type_map(v).get_converter()(v)
            elem = "{k} = {v}".format(k = k, v = tv, line = HCLGen.line)
            hcl_map_elems += "{indent}{indent}{elem}{line}".format(indent = HCLGen.indent, elem = elem, line = HCLGen.line)
        return "{start}{line}{elems}{indent}{end}".format(start = HCLGen.block_start, line = HCLGen.line, 
                                                        elems = hcl_map_elems, end = HCLGen.block_end, 
                                                        indent = HCLGen.indent)

    @staticmethod
    def hcl_for_parent_childable(obj) -> str: 
        if isinstance(obj, Resource):
            body = ""
            for prop_key in obj.resource_properties.keys():
                prop_val = obj.resource_properties.get(prop_key)

                type_map = PyTypeMap.get_type_map(prop_val)
                cfn = type_map.get_converter()
                hcl_val = cfn(prop_val)

                # hcl_val = to_hcl(prop_val)
                body += "{indent}{prop_key} = {prop_val}{line}".format(indent = HCLGen.indent, 
                    prop_key = prop_key, prop_val = hcl_val, line = HCLGen.line)
            
            header = "resource \"{resource_type_name}\" \"{resource_inst_name}\" "
            header = header.format(resource_type_name = obj.resource_type_name, 
                                resource_inst_name = obj.resource_inst_name)
            header = header + HCLGen.block_start + HCLGen.line
            footer = HCLGen.block_end + HCLGen.line
            return str(header + body + footer)
        else:
            raise ObjNotHashiObjException("Obj must be a resource instance.")


    @staticmethod
    def hcl_for_provider(obj):
        required_providers_fragment = ""
        provider_configuration_fragment = ""

        provider_name = "{type} = {blockstart}{line}".format(type=obj.provider_name, blockstart=HCLGen.block_start, line=HCLGen.line)
        provider_source = "{indent}source = {source}{line}".format(indent=HCLGen.indent, source = obj.provider_source, line = HCLGen.line)
        provider_version = "{indent}version = {version}{line}".format(indent = HCLGen.indent, version=obj.provider_version, line=HCLGen.line)
        line_end = "{blockend}".format(blockend=HCLGen.block_end)
        required_providers_fragment = str(provider_name + provider_source + provider_version + line_end)

        header = "provider \"{type}\" {block}{line}".format(type=obj.provider_name, block=HCLGen.block_start, line=HCLGen.line)
        body = ""
        for prop_key in obj.provider_properties.keys():
            prop_val = obj.provider_properties.get(prop_key)
            hcl_val = to_hcl(prop_val)
            body += "{indent}{prop_key} = {prop_val}{line}".format(indent = HCLGen.indent, 
                prop_key = prop_key, prop_val = hcl_val, line = HCLGen.line)
        footer = HCLGen.block_end + HCLGen.line
        provider_configuration_fragment = str(header + body + footer)
        return (required_providers_fragment, provider_configuration_fragment)

    @staticmethod
    def hcl_for_module(obj):
        header = "module \"{name}\" {block}{line}".format(name = obj.module_name, block=HCLGen.block_start, line=HCLGen.line)
        source = "{indent}source = {source}{line}".format(source = obj.module_source, indent = HCLGen.indent, line = HCLGen.line)
        version = "{indent}version = {version}{line}".format(version = obj.module_version, indent = HCLGen.indent, line = HCLGen.line)
        property_text = ""
        for prop_key in obj.module_properties.keys():
            prop_val = obj.module_properties.get(prop_key)

            type_map = PyTypeMap.get_type_map(prop_val)
            cfn = type_map.get_converter()
            prop_hcl_val = cfn(prop_val)
            # TODO: Handle complex properties (end-block properties...)
            property_text += "{indent}{prop_name} = {prop_val}{line}".format(indent = HCLGen.indent, prop_name = prop_key, 
                                                                                     prop_val = prop_hcl_val, line = HCLGen.line)
        footer = HCLGen.block_end + HCLGen.line
        module_hcl_fragment = str(header + source + version + property_text + footer)
        return module_hcl_fragment

    @staticmethod
    def hcl_for_data(obj):
        header = "data \"{source}\" \"{name}\" {block}{line}".format(source = obj.data_source, name = obj.data_name, 
                                                                        block=HCLGen.block_start, line=HCLGen.line)
        property_text = ""
        for prop_key in obj.data_properties.keys():
            prop_val = obj.data_properties.get(prop_key)
            # TODO: Create a single 'native' provider generator instance
            type_map = PyTypeMap.get_type_map(prop_val)
            cfn = type_map.get_converter()
            prop_hcl_val = cfn(prop_val)

            # TODO: Handle complex properties (end-block properties...)
            property_text += "{indent}{prop_name} = {prop_val}{line}".format(indent = HCLGen.indent, prop_name = prop_key, 
                                                                                     prop_val = prop_hcl_val, line = HCLGen.line)
        footer = HCLGen.block_end + HCLGen.line
        data_hcl_fragment = str(header + property_text + footer)
        return data_hcl_fragment


class PyTypeMap:
    # TODO: Add not found:
        # else:
        # raise TypeConverterFnNotFoundException()

    def __init__(self, is_none: bool = False, is_bool: bool = False, is_int: bool = False, is_float: bool = False, is_complex: bool = False, 
                       is_str: bool = False, is_bytes: bool = False, is_bytearray: bool = False, is_list: bool = False, is_tuple: bool = False, 
                       is_range: bool = False, is_set: bool = False, is_frozenset: bool = False, is_dict: bool = False, 
                       is_parent_childable: bool = False, is_provider: bool = False, is_module: bool = False, is_data: bool = False):
        self.is_none = is_none
        self.is_bool = is_bool
        self.is_int = is_int
        self.is_float = is_float
        self.is_complex = is_complex
        self.is_str = is_str
        self.is_bytes = is_bytes
        self.is_bytearray = is_bytearray
        self.is_list = is_list
        self.is_tuple = is_tuple
        self.is_range = is_range
        self.is_set = is_set
        self.is_frozenset = is_frozenset
        self.is_dict = is_dict
        self.is_parent_childable = is_parent_childable
        self.is_provider = is_provider
        self.is_module = is_module
        self.is_data = is_data

    def __str__(self):
        return f'PyTypeMap(\n\t \
            is_none = {self.is_none}, \n\t \
            is_bool = {self.is_bool}, \n\t \
            is_int = {self.is_int}, \n\t \
            is_float = {self.is_float}, \n\t \
            is_complex = {self.is_complex}, \n\t \
            is_str = {self.is_str}, \n\t \
            is_bytes = {self.is_bytes}, \n\t \
            is_bytearray = {self.is_bytearray}, \n\t \
            is_list = {self.is_list}, \n\t \
            is_tuple = {self.is_tuple}, \n\t \
            is_range = {self.is_range}, \n\t \
            is_set = {self.is_set}, \n\t \
            is_frozenset = {self.is_frozenset}, \n\t \
            is_dict = {self.is_dict}, \n\t \
            is_parent_childable = {self.is_parent_childable}, \n\t \
            is_provider = {self.is_provider}, \n\t \
            is_module = {self.is_module}, \n\t \
            is_data = {self.is_data})'

    def get_converter(self) -> function:
        type_converter_map = {
            'is_none': HCLConverter.hcl_for_none,
            'is_bool': HCLConverter.hcl_for_bool,
            'is_int': HCLConverter.hcl_for_int,
            'is_float': HCLConverter.hcl_for_float,
            'is_complex': HCLConverter.hcl_for_complex,
            'is_str': HCLConverter.hcl_for_str,
            'is_bytes': HCLConverter.hcl_for_bytes,
            'is_bytearray': HCLConverter.hcl_for_bytearray,
            'is_list': HCLConverter.hcl_for_list,
            'is_tuple': HCLConverter.hcl_for_tuple,
            'is_range': HCLConverter.hcl_for_range,
            'is_set': HCLConverter.hcl_for_set,
            'is_frozenset': HCLConverter.hcl_for_frozenset,
            'is_dict': HCLConverter.hcl_for_dict,
            'is_parent_childable': HCLConverter.hcl_for_parent_childable,
            'is_provider': HCLConverter.hcl_for_provider,
            'is_module': HCLConverter.hcl_for_module,
            'is_data': HCLConverter.hcl_for_data
        }

        for k in type_converter_map.keys():
            if self.__getattribute__(k) == True:
                fn = type_converter_map.get(k)
                return fn
        # return self.type_converter_map[type]
    
    @staticmethod
    def get_type_map(obj) -> PyTypeMap:
        pytype = PyTypeMap()
        if obj == None: 
            pytype.is_none = True
        
        pytype.is_bool = isinstance(obj, bool)
        pytype.is_int = isinstance(obj, int)
        pytype.is_float = isinstance(obj, float)
        pytype.is_complex = isinstance(obj, complex)
        pytype.is_str = isinstance(obj, str)
        pytype.is_bytes = isinstance(obj, bytes)
        pytype.is_bytearray = isinstance(obj, bytearray)
        pytype.is_list = isinstance(obj, list)
        pytype.is_tuple = isinstance(obj, tuple)
        pytype.is_range = isinstance(obj, range)
        pytype.is_set = isinstance(obj, set)
        pytype.is_frozenset = isinstance(obj, frozenset)
        pytype.is_dict = isinstance(obj, dict)
        pytype.is_parent_childable = isinstance(obj, Resource) or issubclass(obj.__class__, Resource) # isinst Data isinst Var etc...
        pytype.is_provider = isinstance(obj, Provider)
        pytype.is_module = isinstance(obj, Module)
        pytype.is_data = isinstance(obj, Data)
        
        return pytype


class HCLGenerator(object):
    def __init__(self, hashis: list[RegisteredHashiObj]) -> None:
        super().__init__()
        self.providers = []
        self.hashi_objects = []
        for regd_hashi in hashis:
            if isinstance(regd_hashi.hashi_object, Provider):
                self.providers.append(regd_hashi)
            else:
                self.hashi_objects.append(regd_hashi)

    ##
    # Single instance HCL-value processor
    def convert_value_for_type(self, typemap: PyTypeMap, obj: object, sibling_nodes: list, ref_fn: function, recursion_level: int) -> object:
        try:
            converterfn = typemap.get_converter()
            hcl_val = converterfn(obj)
            ref_fn(typemap, obj, hcl_val, sibling_nodes, recursion_level)

            if self.has_children(obj):
                children = self.get_childable_nodes(obj)
                siblings_list = []
                for c in children:
                    t = PyTypeMap.get_type_map(c)
                    rcl_n = recursion_level + 1
                    siblings_list.append(self.convert_value_for_type(t, c, siblings_list, ref_fn, rcl_n))
        except TypeConversionNotSupportedException as tcon:
            handle_exception(tcon)
        except TypeConverterFnNotFoundException as tfn:
            handle_exception(tfn)

    ##
    # Processes a multi-nested structure of python value-instance objects into 
    # individual HCL calls and then recombines them into an HCL Object (currently a string)
    #
    def process_hcl_conversion(self, orig_obj: object):
        root = []

        def ref_fn(typ, obj, hcl_value, parents_children, recursion_level):   
            d = {'type': typ, 'py_object': obj, 'hcl_value': hcl_value, 'children': [], 'recursion_level': recursion_level}
            parents_children.append(d)

        if isinstance(orig_obj, Sequence) and not isinstance(orig_obj, str):
            for o in orig_obj:
                val = None
                if isinstance(o, RegisteredHashiObj):
                    val = o.hashi_object
                elif isinstance(o, HashiObj):
                    regd_hashi_obj = HashiReg.instance().get_hashi_by_id(o.id)
                    val = regd_hashi_obj.hashi_object
                else:
                    val = o
                tm = PyTypeMap.get_type_map(val)
                self.convert_value_for_type(tm, val, root, ref_fn, 0)
            return root
        # else:
        #     raise Exception("Type not supported for HCL C")

    def has_children(self, obj) -> bool:
        if PyTypeMap.get_type_map(obj).is_parent_childable: 
            for prop_key in obj.resource_properties.keys():
                prop_val = obj.resource_properties.get(prop_key)
                if PyTypeMap.get_type_map(prop_val).is_parent_childable: 
                    return True
        return False

    def get_childable_nodes(self, obj) -> bool:
        childable: List[dict] = []
        if PyTypeMap.get_type_map(obj).is_parent_childable:
            for prop_key in obj.resource_properties.keys():
                prop_val = obj.resource_properties.get(prop_key)
                if PyTypeMap.get_type_map(prop_val).is_parent_childable:
                    childable.append(prop_val)
        return childable


    def to_hcl_node_doc(self, node: dict) -> str:
        hcl_value = node.get('hcl_value')
        type_val = node.get('type')
        if type_val.is_provider:
            self.providers.append(node)

        node_doc = ""
        if type_val.is_parent_childable or type_val.is_provider: 
            node_doc = "{line}{node}{line}"
        else: 
            node_doc = "{node}"
        node_doc = node_doc.format(line = HCLGen.line, node = hcl_value)
        children = node.get('children')
        
        if len(children) > 0:
            for c in children:
                node_doc += self.to_hcl_node_doc(c)
        return node_doc

    def generate_hcl_header(self) -> str:
        # Note: this isnt part of the PyType Generation objects because it doesnt reside 
        # in a dynamically available location, its a header generation sequence.

        header_text = ""
        header_text += "terraform {block_start}{line}".format(block_start = HCLGen.block_start, line = HCLGen.line)
        if self.providers and len(self.providers) > 0:
            header_text += "{indent}required_providers {block_start}{line}".format(indent = HCLGen.indent, block_start = HCLGen.block_start, line = HCLGen.line)
            for regd_hashi in self.providers:
                provider = regd_hashi.hashi_object
                provider_text = ""
                provider_text += "{indent}{indent}{name} = {block_start}{line}".format(indent = HCLGen.indent, name = provider.provider_name, block_start = HCLGen.block_start, line = HCLGen.line)
                provider_text += "{indent}{indent}{indent}source = \"{source}\"{line}".format(indent = HCLGen.indent, source = provider.provider_source, line=HCLGen.line)
                provider_text += "{indent}{indent}{indent}version = \"{version}\"{line}".format(indent = HCLGen.indent, version = provider.provider_version, line=HCLGen.line)
                provider_text += "{indent}{indent}{block_end}{line}".format(indent = HCLGen.indent, block_end = HCLGen.block_end, line=HCLGen.line)
                header_text += provider_text
            header_text += "{indent}{block_end}{line}".format(indent = HCLGen.indent, block_end = HCLGen.block_end, line = HCLGen.line)
        
        header_text += "{block_end}{line}".format(block_end = HCLGen.block_end, line = HCLGen.line)
        header_text += "{line}".format(line = HCLGen.line)
        
        return header_text

    def generate_hcl_providers(self) -> str:
        providers_text = ""
        for regd_provider in self.providers:
            provider = regd_provider.hashi_object
            if provider.provider_properties:
                provider_text = ""
                provider_text += "provider \"{provider_name}\" {start_block}{line}".format(provider_name = provider.provider_name, start_block=HCLGen.block_start, line = HCLGen.line)
                for prop_key in provider.provider_properties.keys():
                    prop_val = provider.provider_properties.get(prop_key)
                    
                    type_map = PyTypeMap.get_type_map(prop_val)
                    cfn = type_map.get_converter()
                    prop_hcl_val = cfn(prop_val)

                    provider_text += "{indent}{prop_name} = {prop_val}{line}".format(indent = HCLGen.indent, prop_name = prop_key, 
                                                                                     prop_val = prop_hcl_val, line = HCLGen.line)
                provider_text += "{block_end}{line}".format(block_end = HCLGen.block_end, line = HCLGen.line)
                # provider_text += "{line}".format(line = HCLGen.line)
                providers_text += provider_text
        return providers_text

    def generate_hcl_body(self): #, *obj) -> str:
        hcl_body = ""
        for o in self.hashi_objects:             
            root_obj_tree = self.process_hcl_conversion([o.hashi_object])
            for node in root_obj_tree:
                hcl_text = self.to_hcl_node_doc(node)
                hcl_body += hcl_text
        return hcl_body

        # header = "terraform {block_start}{line}".format(block_start=HCLGen.block_start, line = HCLGen.line)
        # providers_block = []
        # if self.providers:
        #     providers_block.append("{indent}required_providers {block_start}{line}".format(indent=HCLGen.indent, block_start=HCLGen.block_start, line=HCLGen.line))
        #     for provider in self.providers:
        #         providers_block.append(provider)
        # providers_footer = "{indent}{block_end}{line}".format(indent=HCLGen.indent, block_end=HCLGen.block_end, line=HCLGen.line)
        # headers_footer = "{block_end}{line}".format(block_end=HCLGen.block_end, line=HCLGen.line)
        # hcl_header = str(header + HCLGen.line.join(providers_block) + providers_footer + headers_footer)

        # return str(hcl_header + HCLGen.line + hcl_body)
                

# def to_hcl(generator, *obj) -> str:
#     hcldoc = ""
#     hcldoc += generator.generate_hcl_body(obj)
#     return hcldoc

# def to_hcl_list(hashis) -> List[str]:
#     hclgen = HCLGenerator()
    
#     hashi_hcls = []
#     for hashi in hashis:
#         # print("hashi_obj: ", hashi)

#         print("hashi_obj.__dict__", hashi.__dict__)
#         generated_hashi = to_hcl(hclgen, hashi)
#         hashi_hcls.append(generated_hashi)

#     header = hclgen.generate_hcl_header()
#     print(header)
#     return hashi_hcls

def new_hcl(hashis):
    hclgen = HCLGenerator(hashis)

    body = hclgen.generate_hcl_body()
    providers = hclgen.generate_hcl_providers()
    header = hclgen.generate_hcl_header()

    hcl = "{header}{providers}{body}".format(header = header, providers = providers, body = body)
    return hcl

##
# Exception handler for unsupported Type Conversion Errors 
class TypeConversionNotSupportedException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class TypeConverterFnNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        if len(args) == 1:
            self.type = args[0]

class ObjNotHashiObjException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        if len(args) == 1:
            self.type = args[0]