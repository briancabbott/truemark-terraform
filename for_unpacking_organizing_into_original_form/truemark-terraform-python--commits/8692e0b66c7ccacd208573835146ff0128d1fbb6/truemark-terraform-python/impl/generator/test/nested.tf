# r2_innerProps = Resource(
#     "resource", 
#     "$INST", 
#     prop1 = "",
#     prop2 = 1+1,
#     prop3 = 1.68504835098,
#     prop4 = True,
#     prop5_innerObject1 = Resource(
#         "inner-object_resource", 
#         "innerObject$INST", 
#         innerProp1 = "", 
#         innerProp2 = 2 + 2, 
#         innerProp3 = 2.1732434234244, 
#         innerProp4 = False),
#     prop6 = "adsf",
#     prop7 = None,
#     prop8_innerObject2 = Resource(
#         "inner_resource", 
#         "inner$INST", 
#         prop_innerObject_innerInner = Resource(
#             "inner-inner_resource", 
#             "innerInner$INST", 
#             innerInner_prop1 = "34",
#             innerInner_prop2 = 34,
#             innerInner_prop3 = 3324.3242434343,
#             innerInnerInner_prop1 = Resource(
#                 "inner-Inner-Inner_resource", 
#                 "innerInnerInner$INST", 
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
terraform {
  required_providers {
    truemark-bitbucket = {
      source = "truemark.io/terraform/truemark-bitbucket"
      version = "1.0.0"
    }
  }
}

resource "resource" "INST" {
  prop1 = ""
  prop2 = 1+1
  prop3 = 1.68504835098
  prop4 = True
  prop5_innerObject1 = {
      
  }
}

# resource "resource" "$INST" {

}