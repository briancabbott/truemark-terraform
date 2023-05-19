from __future__ import annotations

import os
import tempfile

###
## This is the outter pythonic wrapper for the TrueMark-TerraForm schema generation process. The 
## idea with this component is to enforce or handle the overall process of the gen operation 
## end to end with the input being a single provider name and version and the output being
## a WHL file that can be installed on either a local or remote system that will be executing 
## TrueMark-TerraForm CLI Operations that is in need of terraform-provider-schema artifacts. 
##
## Operational Steps:
##    1. Create Tmp Dirs and CWD to them
##    2. Generate a TMTF Python File for the provider-schema/version of interest.
##    3. Execute TMTF to generate a TF file for our provider.
##    4. Execute the JSON command on the Generated TF File to produce the JSON definition of the schema.
##    5. Generate the python objects for the JSON schema.
##    6. Package everything into an installable python Wheel file.
##
class SchemaGenerator():
    def __init__(self, provider_name: str = None, provider_source: str = None, provider_version: str = None):
        self.provider_name = provider_name
        self.provider_source = provider_source
        self.provider_version = provider_version
        self.tmp_wkspace_dir = self.setup_tmp_wkspace()

    def setup_tmp_wkspace(self) -> str: 
        systmp = tempfile.gettempdir() 
        tmpdir = 'truemark-terraform-schemagen-tmpdir'
        tmppath = os.path.join(systmp, tmpdir)
        
        # Delete any previous contents if it already exists
        if os.is_dir(tmppath):
            os.remove(tmppath)
        os.mkdir(tmppath)
        return tmppath

    ##
    # Public outter, the rest of the methods in this class are inner private providers
    # TODO: Figure out how to make methods private in Py?
    def generate(self):
        self.start_generation()
        self.generate_python_file_for_provider()
        self.execute_tmtf_generation()
        pass

    def start_generation(self):
        pass

    def end_generation(self):
        pass

    def generate_python_file_for_provider(self):
        provider_code = 'from truemark_terraform.model.provider import Provider'\
                        'Provider("aws", "hashicorp/aws", "~> 3.27")'

        pass

    def generate_python_artifacts(self):
        pass

    def generate_wheel_file(self):
        pass