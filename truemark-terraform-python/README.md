# Welcome, to TrueMark-TerraForm

## Overview
TrueMark-TerraForm allows members of a DevOps team to write Python code that captures
and describes TerraForm operations and when executed from the supporting set of 
Command-Line tools, performs each action described in the Python code through the 
local TerraForm installation.  In effect, providing a bridge from Python to HCL script 
and then, as a convenience, total integration with the TerraForm CLI Application Space.
To achieve this, there is an ecosystem of supporting elements in addition to the primary
TerraForm driver. The TMTF subsystem elements are as follows:
   - bin-install
   - generator
   - schema-generator
   - schema-generator-data-defaults

### bin-install
This is a group of builder-installers and wrapper components that enable a nice 
and ergonomic CLI experience. Running this will install a set of CLI tools and add them 
to your system path. It also ensures that all dependencies are present, such as Python-3.10.

### generator
This is the primary and most significant component within TM-TF. It is the "driver" that 
adapts the Python code to TerraForm HCL.

### schema-generator
The schema-generator is a supporting component that takes a set of provider name/version pairs
and generates Python code from them so that a user can code against TerraForm Plugin Providers
as they would in HCL script without causing compilation errors or having to hardcode string values that
actually represent complex and highly structured HCL shapes but, are inaccessible to the python code. 
This allows us to avoid that and be able to either directly reference or directly set values of 
arbitrary depth within the overall TerraForm Provider Schemas.

### schema-generator-data-defaults
The Schema-Generator Data-Defaults is a supporting component to the Schema-Generator supporting 
component: a supporting component's supporting component. Data-Defaults works by bolting into a 
given plugin and breifly instantiating it. It then traverses its internal schema for any attribute 
with a set value. Upon locating a value it adds it to its internal list and, once the traversal is 
complete, it generates a JSON-Query compliant data structure, persisted to the file system that, 
when paired with a schema gen operation, creates a python object model of a Providers artifacts 
with the correct default values already set. 

## Building and Installing TrueMark-TerraForm
TrueMark-TerraForm (TMTF) is built and distributeed as a Python Wheel File. Once 
the Wheel-File is installed into the local Python PIP database, the CLI executables 
can either be referenced as absolute paths or added to either the User or System 
PATH variable, depending on the User's need. If necessary, we can also perform this 
during the wheel installation. 

### Requirements
TrueMark-TerraForm is built with Python-3.10. We use, although currently in a passive
non-critical way the Python-3.10 type-hinting functionality and, while it currently will
work with older versions such as Python-3.8 or Python-3.9, we may at some point utilize
this functionality to drive core features and functionality therefore, it is 
critical to maintain operations and development on Python-3.10. Additional requirements are: 
   - PIP Upgrade to the latest
   - setuptools (for the Egg and WHL file support)
   - wheel (for the Egg and WHL file support)

All dependencies necessary should be added to the ./bin/setup.sh file as they are added
which serves also as a record or which dependencies are necessary. 

### Building
You can simply build the WHL file from the ./bin/build.sh file which executes the
setup.py file to create a wheel file and then copies that into a ./dist folder. 

### Installation
An installation script is provided in the bin directory. It can be executed by running:

```console
➜  generator git:(develop) ✗ ./bin/install.sh
```

This commmand runs the wheel file generated from the build output, located at:
   ./dist/truemark_terraform-0.1.0-py3-none-any.whl

This will install the wheel into the Python PIP but not add it to the system $PATH 
variable so, it will need to be executed from the source directory. 

```console
➜  generator git:(develop) ✗ python3.10 ./src/truemark_terraform/driver/terraform_cli.py generate --file ./test/terraform-build-infrastructure-tutorial/main.py
```

## Development
In order to aid expedited development and always ensure a clean working environment 
with the most recent dependencies, we have a do_all.sh script in the ./bin folder. 
This file ensures that the ENV variables are created and set to the correct values, 
that the dependencies are all installed, and that the most current version of any
saved code is what is insalled in the PIP registry. Some operational configurations
cache certain settings, dependencies or code along the way which is why this script 
was created and is important to use during development so that there are no surprises.

In order to run the script, simply perform the following operation:

from the impl/generator folder, run the command:

```console
➜  generator git:(develop) ✗ ./bin/do_all.sh
```

This will perform all actions needed to install the latest version as a py-wheel 
file. In order to execute TrueMark TerraForm Operations, simply run the terraform_cli.py
file from the current directory: 

```console
➜  generator git:(develop) ✗ python3.10 ./src/truemark_terraform/driver/terraform_cli.py generate --file ./test-verification/truemark/services/alerts-api/py/main.py
```

