#!/bin/bash

cd src
python3.10 setup.py bdist_wheel
mv ./dist ../
cd ..