terraform {
  required_providers {
    literal-test-provider = {
      source = "truemark-terraform/test-provider"
      version = "~> 1.0.100"
    }
  }
}

provider "literal-test-provider" {
  prop_1 = "prop-1"
  prop_2 = 9921
  prop_21 = 23.901
  prop_3 = true
  prop_31 = false
  prop_4 = null
  prop_5 = ["asdf", 23, 0.324343, true, false, null]
  prop_6 = ["asdf", 34, 0.434343, false, true, null]
  prop_7 = {
    key_1 = "val_1"
    key_2 = 112121
    key_3 = true
    key_4 = false
    null_1 = null
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
}

