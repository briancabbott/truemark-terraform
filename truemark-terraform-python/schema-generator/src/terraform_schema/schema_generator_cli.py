
import sys
import argparse
from os import stat
import logging

from terraform_schema.providers_schema_provider import TerraformSchemaProvider

class SchemaGeneratorCLI():
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def execute_cli():
        parser = argparse.ArgumentParser(prog = 'truemark-terraform', add_help = True, conflict_handler = 'resolve')
        parser.add_argument('--terraform-dir', type = str)
        parser.add_argument('--debug', dest='debug', default=False, action='store_true')
        argsg = parser.parse_args()
        # parser.add_argument('--loglevel', type=str)

        terraform_dir = argsg.terraform_dir
        if argsg.debug:
            logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

        print("terraform-dir: " + terraform_dir)
        terraform_schema_provider = TerraformSchemaProvider(terraform_dir)
        terraform_schema_provider.acquire_schema_for_script()

if __name__ == "__main__":
    SchemaGeneratorCLI.execute_cli()