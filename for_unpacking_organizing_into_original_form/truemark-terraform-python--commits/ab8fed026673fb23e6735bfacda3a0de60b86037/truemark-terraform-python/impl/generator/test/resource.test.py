

from truemark_terraform.model.resource import Resource
from truemark_terraform.utils.hcl.hcl_utils import to_hcl

## TODO: Lookup Unit Testing in Python:


## Basic Native Props... 
def run_test_1():
    r = Resource("resource-of-kind_for_me", "myResourceOfAKind", prop1="prop1")
    dict_val = r.to_dict()
    json_str = r.to_json()
    
## MAKE ME WORK!!!!
def run_innerprops_test_nested_times_four():
    r2_innerProps = Resource(
        "resource", 
        "INST", 
        prop1 = "afe",
        prop2 = 1+1,
        prop3 = 1.68504835098,
        prop4 = True,
        prop5 = Resource(
            res = ""
        ))

    #     prop5_innerObject1 = Resource(
    #         "inner-object_resource", 
    #         "innerObjectINST", 
    #         innerProp1 = "", 
    #         innerProp2 = 2 + 2, 
    #         innerProp3 = 2.1732434234244, 
    #         innerProp4 = False),
    #     prop6 = "adsf",
    #     prop7 = None,
    #     prop8_innerObject2 = Resource(
    #         "inner_resource", 
    #         "innerINST", 
    #         prop_innerObject_innerInner = Resource(
    #             "inner-inner_resource", 
    #             "innerInnerINST", 
    #             innerInner_prop1 = "34",
    #             innerInner_prop2 = 34,
    #             innerInner_prop3 = 3324.3242434343,
    #             innerInnerInner_prop1 = Resource(
    #                 "inner-Inner-Inner_resource", 
    #                 "innerInnerInnerINST", 
    #                 innerInnerInner_prop1 = "",
    #                 innerInnerInnerInner_innerProp1 = Resource(
    #                     "innerInnerInnerInner", 
    #                     "innerInnerInnerInner", 
    #                     innerInnerInnerInner_prop1 = "", 
    #                     innerInnerInnerInner_prop2 = 343, 
    #                     innerInnerInnerInner_prop3 = 0.342383433898, 
    #                     innerInnerInnerInner_prop4 = False)))) 

    # )
    # r2_innerProps.property("innerObject").prop_key = "value"
    hcl = to_hcl(r2_innerProps)
    print(hcl)

# Like the above but, use .property("name") to perform it all in a single column line
def run_innerprops_test_linear_times_four():
    pass

if __name__ == "__main__":
    # run_test_1()
    run_innerprops_test_nested_times_four()
    # run_innerprops_test()