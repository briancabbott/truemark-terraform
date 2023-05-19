# TrueMark-TerraForm Schema Generator

Schema Generator for TerraForm Provider Schemas referenced from within the Providers 
section of a TerraForm (.tf) script.

Design Note: 
This really should be thought of as a standalone component, at least for now. A ClI component 
that generates .whl files for a given name/version combination of a provider, grabs its schema, 
then generates all artifacts in a tmp-gen directory and creates a whl file around that directory
and optionally installs it. In addition to having it operationally ideal (cleanest possible), This
approach ensures that anything that we need to have during the runtime will not only be there but, 
be facilitated in a way that doesnt confuse the boundary lines between generated artifacts for 
TM-TF and actual runtime elements that should be kept seperate from a 