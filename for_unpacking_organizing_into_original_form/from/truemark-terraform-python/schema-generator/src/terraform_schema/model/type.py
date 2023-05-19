from __future__ import annotations

from enum import Enum

##
# Type vs Kind: Type -> Unique Element, in a Class(OOP) Specific Context
#
class Type(Enum):
    String = "STRING"
    Boolean = "BOOL"
    Number = "NUMBER"
    
    List_of_Primitives = "LIST_OF_PRIMITIVES"
    List_of_Strings = "LIST_OF_STRINGS"  
    List_of_Bools = "LIST_OF_BOOLS"   
    List_of_Numbers = "LIST_OF_NUMBERS"
    List_of_Objects = "LIST_OF_OBJECTS"
    
    Set_of_Strings = "SET_OF_STRINGS"
    Set_of_Bools = "SET_OF_BOOLS"
    Set_of_Numbers = "SET_OF_NUMBERS"
    Set_of_Objects = "SET_OF_OBJECTS"

    Map_of_Strings = "MAP_OF_STRINGS"
    Map_of_Bools = "MAP_OF_BOOLS"
    Map_of_Numbers = "MAP_OF_NUMBERS"
    Map_of_Objects = "MAP_OF_OBJECTS"

    @staticmethod
    def getTypeFromStr(type_name: str) -> Type:
        if type_name == None:
            return None
        kind_name = type_name.lower()

        if kind_name == "string":
            return Type.String
        elif kind_name == "bool" or kind_name == "false" or kind_name == "true":
            return Type.Boolean
        elif kind_name == "number":
            return Type.Number
        elif kind_name.startswith("['set', 'string'") or kind_name.startswith("['set', ['string'"):
            return Type.Set_of_Strings
        elif kind_name.startswith("['set', 'bool'") or kind_name.startswith("['set', ['bool'"):
            return Type.Set_of_Bools
        elif kind_name.startswith("['set', 'number'") or kind_name.startswith("['set', ['number'"):
            return Type.Set_of_Numbers
        elif kind_name.startswith("['set', 'object'") or kind_name.startswith("['set', ['object'"):
            return Type.Set_of_Objects
        elif kind_name.startswith("['list', 'string'") or kind_name.startswith("['list', ['string'"):
            return Type.List_of_Strings
        elif kind_name.startswith("['list', 'bool'") or kind_name.startswith("['list', ['bool'"):
            return Type.List_of_Bools
        elif kind_name.startswith("['list', 'number'") or kind_name.startswith("['list', ['number'"):
            return Type.List_of_Numbers
        elif kind_name.startswith("['list', 'object'") or kind_name.startswith("['list', ['object'"):
            return Type.List_of_Objects

        # elif kind_name.startswith("['list', ['object"):
        # elif kind_name.startswith("['list', ['object'"):
        #     return Type.List_of_Objects

        elif kind_name.startswith("['map', 'string'") or kind_name.startswith("['map', ['string'"):
            return Type.Map_of_Strings
        elif kind_name.startswith("['map', 'bool'") or kind_name.startswith("['map', ['bool'"):
            return Type.Map_of_Bools
        elif kind_name.startswith("['map', 'number'") or kind_name.startswith("['map', ['number'"):
            return Type.Map_of_Numbers
        elif kind_name.startswith("['map', 'object'") or kind_name.startswith("['map', ['object'"):
            return Type.Map_of_Objects
        else:
            # TODO: Have a decent catch-all
            print("UNKNOWN TYPE!!!! TypeStr was: " + str(type_name))