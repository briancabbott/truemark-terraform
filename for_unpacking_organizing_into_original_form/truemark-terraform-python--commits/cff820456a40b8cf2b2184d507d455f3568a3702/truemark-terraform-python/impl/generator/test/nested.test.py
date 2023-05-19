from truemark_terraform.model.resource import Resource
from truemark_terraform.driver.terraform import Terraform

r = Resource("resource-provider_type", "resource-name", 
    # »Strings
    str_1 = "my_test_string",
    # »Numbers
    num_1 = 238233,
    num_2 = 23.3483,
    # »Bools
    bool_1 = True,
    bool_2 = False,
    # »Null
    null_1 = None,
    # »Lists/Tuples
    list_1 = ["asdf", 23, 0.324343, True, False, None],
    tuple_1 = ("asdf", 34, 0.434343, False, True, None),
    # # »Maps/Objects
    map_1 = {'key_1': "val_1", 'key_2': 112121, 'key_3':True, 'key_4':False, 'null_1':None},

    child_1 = Resource("child-1_resource", "child-1_INST", 
                        prop1 = "", prop2 = 2 + 2, prop3 = 2.17324, prop4 = False),
    prop6 = "adsf",
    prop7 = None,
    # iO = Inner-Object
    # Dn = Depth-Value, 1 deep, 2 deep ... N deep
    prop8_iO_innerD1 = Resource("child-D1_resource", "child-D1", 
        prop_iO_innerD2 = Resource("child-D2_resource", "child-D2", prop1 = "34", prop2 = 34, prop3 = 3324.3242434343, 
            prop_iO_innerD3 = Resource("child-D3_resource", "child-D3", prop1 = "string-val!@#", 
                prop_iO_innerD4 = Resource("child-D4_resource", "child-D4", prop1 = "string-val", prop2 = 343, prop3 = 0.342383433898, prop4 = False)))) 
)