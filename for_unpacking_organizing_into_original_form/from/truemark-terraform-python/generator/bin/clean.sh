#!/bin/bash

rm -rf ./dist
rm -rf ./src/build
rm -rf ./src/dist
rm -rf ./src/truemark_terraform.egg-info

pip3.10 uninstall --yes --verbose truemark-terraform