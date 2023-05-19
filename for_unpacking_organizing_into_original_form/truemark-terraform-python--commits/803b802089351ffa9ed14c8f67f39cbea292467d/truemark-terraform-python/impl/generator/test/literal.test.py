###
# Literal Expressions
# A literal expression is an expression that directly represents a particular 
# constant value. Terraform has a literal expression syntax for each of the 
# value types described above.
# 
# »Strings
# Strings are usually represented by a double-quoted sequence of Unicode 
# characters, "like this". There is also a "heredoc" syntax for more complex 
# strings.
# 
# String literals are the most complex kind of literal expression in 
# Terraform, and have their own page of documentation. See Strings for 
# information about escape sequences, the heredoc syntax, interpolation, 
# and template directives.
# 
# »Numbers
# Numbers are represented by unquoted sequences of digits with or without 
# a decimal point, like 15 or 6.283185.
# 
# »Bools
# Bools are represented by the unquoted symbols true and false.
# 
# »Null
# The null value is represented by the unquoted symbol null.
# 
# »Lists/Tuples
# Lists/tuples are represented by a pair of square brackets containing a
#  comma-separated sequence of values, like ["a", 15, true].
# 
# List literals can be split into multiple lines for readability, but 
# always require a comma between values. A comma after the final value 
# is allowed, but not required. Values in a list can be arbitrary expressions.
# 
# »Maps/Objects
# Maps/objects are represented by a pair of curly braces containing a series 
# of <KEY> = <VALUE> pairs:
# {
#   name = "John"
#   age  = 52
# }
# Key/value pairs can be separated by either a comma or a line break.
# 
# The values in a map can be arbitrary expressions.
# 
# The keys in a map must be strings; they can be left unquoted if they are a 
# valid identifier, but must be quoted otherwise. You can use a non-literal 
# string expression as a key by wrapping it in parentheses, 
# like (var.business_unit_tag_name) = "SRE".
# 
# »Indices and Attributes
# Elements of list/tuple and map/object values can be accessed using the square-bracket
# index notation, like local.list[3]. The expression within the brackets must be a 
# whole number for list and tuple values or a string for map and object values.
# 
# Map/object attributes with names that are valid identifiers can also be accessed 
# using the dot-separated attribute notation, like local.object.attrname. In cases 
# where a map might contain arbitrary user-specified keys, we recommend using only 
# the square-bracket index notation (local.map["keyname"]).
# 
# »More About Complex Types
# In most situations, lists and tuples behave identically, as do maps and objects. 
# Whenever the distinction isn't relevant, the Terraform documentation uses each pair 
# of terms interchangeably (with a historical preference for "list" and "map").
# 
# However, module authors and provider developers should understand the differences
# between these similar types (and the related set type), since they offer different 
# ways to restrict the allowed values for input variables and resource arguments.

from truemark_terraform.model.resource import Resource
from truemark_terraform.model.provider import Provider

from truemark_terraform.driver.terraform import Terraform

Provider("literal-test-provider", "truemark-terraform/test-provider", "~> 1.0.100", 
    prop_1="prop-1", 
    prop_2=9921, # Int/Number
    prop_21=23.901,
    prop_3=True,  # Boolean
    prop_31=False,
    prop_4=None,  # None/Null
    prop_5=["asdf", 23, 0.324343, True, False, None],  # list()
    prop_6=("asdf", 34, 0.434343, False, True, None), # tuple()
    prop_7 = {'key_1': "val_1", 'key_2': 112121, 'key_3':True, 'key_4':False, 'null_1':None})

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
    map_1 = {'key_1': "val_1", 'key_2': 112121, 'key_3':True, 'key_4':False, 'null_1':None}
)