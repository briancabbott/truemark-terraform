

from truemark_terraform.model.resource import Resource


class HCLConfig:
    ##
    # Configuration to use for Generation
    hcl_generation_config = HCLGenerationConfig()
    
    def __init__(self) -> None:
        pass
        
class HCLGenerationConfig():
    ##
    # The character to use for indentations. (Default: SPACE)
    hcl_indentation_character = " "

    ##
    # The number of times to pre-pend the indentation charachter to each indented block. (Default: 2)
    hcl_indentation_count = 2

    def __init__(self) -> None:
        pass

def get_type_map(obj) -> tuple:
    is_none = isinstance(obj, None)
    is_bool = isinstance(obj, bool)
    
    is_int = isinstance(obj, int)
    is_float = isinstance(obj, float)
    is_complex = isinstance(obj, complex)
    
    is_str = isinstance(obj, str)
    is_bytes = isinstance(obj, bytes)
    is_bytearray = isinstance(obj, bytearray)
    is_list = isinstance(obj, list)
    is_tuple = isinstance(obj, tuple)
    is_range = isinstance(obj, range)

    is_set = isinstance(obj, set)
    is_frozenset = isinstance(obj, frozenset)
    
    is_dict = isinstance(obj, dict)

    is_parent_childable = isinstance(obj, Resource) or issubclass(obj, Resource) # isinst Data isinst Var etc...
    return (is_none, is_bool, is_int, is_float, is_complex, is_str, is_bytes, is_bytearray, is_list, is_tuple, is_range, is_set, is_frozenset, is_dict, is_parent_childable)


def hcl_for_none(obj: None):
    pass 

def hcl_for_bool(obj: bool):
    pass
    
def hcl_for_int(obj: int):
    pass

def hcl_for_float(obj: float):
    pass

def hcl_for_complex(obj: complex):
    pass
    
def hcl_for_str(obj: str):
    pass

def hcl_for_bytes(obj: bytes):
    pass

def hcl_for_bytearray(obj: bytearray):
    pass

def hcl_for_list(obj: list):
    pass

def hcl_for_tuple(obj: tuple):
    pass

def hcl_for_range(obj: range):
    pass

def hcl_for_set(obj: set):
    pass

def hcl_for_frozenset(obj: frozenset):
    pass
    
def hcl_for_dict(obj: dict):
    pass

def hcl_for_parent_childable(obj): 
    # isinst Data isinst Var etc...
    pass

def has_children(obj) -> bool:
    is_resource = isinstance(obj, Resource)
    if is_resource:
        for prop_key in obj.resource_properties.keys():
            prop_val = obj.resource_properties.get(prop_key)
            if isinstance(prop_val, Resource):
                return True
    return False

def to_hcl(obj) -> str:
    # numeric types — int, float, complex
    # seq-types: str, bytes, bytearray, list, tuple, range
    # Set Types — set, frozenset¶
    # Mapping Types — dict¶
    # (is_none, is_bool, is_int, is_float, is_complex, 
    #  is_str, is_bytes, is_bytearray, is_list, is_tuple, 
    #  is_range, is_set, is_frozenset, is_dict, is_parent_childable) = get_type_map(obj)
    tup = get_type_map(obj)
    print(tup)

