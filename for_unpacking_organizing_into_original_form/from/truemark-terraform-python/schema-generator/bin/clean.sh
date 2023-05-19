#!/bin/bash

rm -rf ./dist
rm -rf ./src/build
rm -rf ./src/dist

rm -rf ./truemark_terraform_schema_generator.egg-info

pip3.10 uninstall --yes --verbose truemark-terraform-schema-generator