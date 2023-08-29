terraform {
}


resource "child-1_resource" "child-1_INST" {
  prop1 = ""
  prop2 = 4
  prop3 = 2.17324
  prop4 = false
}


resource "child-D4_resource" "child-D4" {
  prop1 = "string-val"
  prop2 = 343
  prop3 = 0.342383433898
  prop4 = false
}


resource "child-D3_resource" "child-D3" {
  prop1 = "string-val!@#"
  prop_iO_innerD4 = resource "child-D4_resource" "child-D4" {
  prop1 = "string-val"
  prop2 = 343
  prop3 = 0.342383433898
  prop4 = false
}

}


resource "child-D2_resource" "child-D2" {
  prop1 = "34"
  prop2 = 34
  prop3 = 3324.3242434343
  prop_iO_innerD3 = resource "child-D3_resource" "child-D3" {
  prop1 = "string-val!@#"
  prop_iO_innerD4 = resource "child-D4_resource" "child-D4" {
  prop1 = "string-val"
  prop2 = 343
  prop3 = 0.342383433898
  prop4 = false
}

}

}


resource "child-D1_resource" "child-D1" {
  prop_iO_innerD2 = resource "child-D2_resource" "child-D2" {
  prop1 = "34"
  prop2 = 34
  prop3 = 3324.3242434343
  prop_iO_innerD3 = resource "child-D3_resource" "child-D3" {
  prop1 = "string-val!@#"
  prop_iO_innerD4 = resource "child-D4_resource" "child-D4" {
  prop1 = "string-val"
  prop2 = 343
  prop3 = 0.342383433898
  prop4 = false
}

}

}

}


resource "resource-provider_type" "resource-name" {
  str_1 = "my_test_string"
  num_1 = 238233
  num_2 = 23.3483
  bool_1 = true
  bool_2 = false
  null_1 = null
  list_1 = ["asdf", 23, 0.324343, true, false, null]
  tuple_1 = ["asdf", 34, 0.434343, false, true, null]
  map_1 = {
    key_1 = "val_1"
    key_2 = 112121
    key_3 = true
    key_4 = false
    null_1 = null
  }
  child_1 = resource "child-1_resource" "child-1_INST" {
  prop1 = ""
  prop2 = 4
  prop3 = 2.17324
  prop4 = false
}

  prop6 = "adsf"
  prop7 = null
  prop8_iO_innerD1 = resource "child-D1_resource" "child-D1" {
  prop_iO_innerD2 = resource "child-D2_resource" "child-D2" {
  prop1 = "34"
  prop2 = 34
  prop3 = 3324.3242434343
  prop_iO_innerD3 = resource "child-D3_resource" "child-D3" {
  prop1 = "string-val!@#"
  prop_iO_innerD4 = resource "child-D4_resource" "child-D4" {
  prop1 = "string-val"
  prop2 = 343
  prop3 = 0.342383433898
  prop4 = false
}

}

}

}

}

