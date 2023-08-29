#!/bin/bash

# echo 'export PATH="/usr/local/opt/openssl@1.1/bin:$PATH"' >> ~/.zshrc
# export PATH="/usr/local/opt/openssl@1.1/bin:$PATH"

export PIP="pip3"
export PYTHON="python3"
export INSTALLEXE_DIR="./build/dist"

python3.10 -m pip install --upgrade pip
python3.10 -m pip install --user --upgrade setuptools wheel
