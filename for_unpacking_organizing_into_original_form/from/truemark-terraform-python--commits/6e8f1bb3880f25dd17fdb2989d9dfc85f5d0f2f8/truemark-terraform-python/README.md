# Welcome, to TrueMark-TerraForm


## Overview
Why? What? When? Where? How? Would? 


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
critical to maintain operations and development on Python-3.10. Additional 
requirements are: 
   - PIP Upgrade to the latest
   - setuptools (for the Egg and WHL file support)
   - wheel (for the Egg and WHL file support)

All dependencies necessary should be added to the ./bin/setup.sh file as they are added
which serves also as a record or which dependencies are necessary. 

### Building
You can simply build the WHL file from the ./bin/build.sh file which executes the
setup.py file to create a wheel file and then copies that into a ./dist folder. 

### Installing


### Development
In order to aid expedited development and always ensure a clean working environment 
with the most recent dependencies, we have a do_all.sh script in the ./bin folder. 
This file ensures that the ENV variables are created and set to the correct values, 
that the dependencies are all installed, and that the most current version of any
saved code is what is insalled in the PIP registry. Some operational configurations
cache certain settings, dependencies or code along the way which is why this script 
was created and is important to use during development so that there are no surprises.

In order to run the script, simply perform the following operation:

from the impl/generator folder, run the command:

➜  generator git:(develop) ✗ ./bin/do_all.sh

This will perform all actions needed to install the latest version as a py-wheel 
file. In order to execute TrueMark TerraForm Operations, simply run the terraform_cli.py
file from the current directory: 

➜  generator git:(develop) ✗ python3.10 ./src/truemark_terraform/driver/terraform_cli.py 
    generate --file ./test-verification/truemark/services/alerts-api/py/main.py

