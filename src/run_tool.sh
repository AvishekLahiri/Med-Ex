#!/bin/sh

# Install Prerequisites
sudo apt install python3 python3-pip
pip3 install pycrypto
pip3 install bullet
pip3 install prettytable

# Run the tool
python3 main.py
