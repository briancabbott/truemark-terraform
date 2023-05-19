#!/bin/bash

export WHL=truemark_terraform_schema_generator-0.1.0-py3-none-any.whl
pip3.10 install --force-reinstall --ignore-installed --verbose ./dist/$WHL