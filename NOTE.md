Currently, this is my commits and some other misc. code as I lost the original changeset during a security issue 
with my work laptop. I will un-pack them from the commit history and move them into a python project layout structure.


This code has been relinquished from TrueMark and is free for any commercial or academic use and is free to adopt.

The design basis is superior to CDK as this is a general purpose HCL generator and, any component can be 
described and generated in the Python Syntax. 

There is one caveat. Any package you want to use in python, including if you are building your own,
you must provide it as a loadable Go-Lang TerraForm Plugin as that is how the default values are 
extracted. Currently there is no mechanism to communicate the defaults in or to Python as that would have
required an excessive (almost unusable) amount of basic value-structure coding using the HCL representative
APIs provided in the TM-TF package. 