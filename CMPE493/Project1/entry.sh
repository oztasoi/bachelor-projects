#!/usr/bin/env sh
echo "Time consumption for creating a virtual environment:"
time python3 -m venv venv
source ./venv/bin/activate
echo "Time consumption for downloading & installing packages for visual upgrage:"
time pip3 install -r requirements.txt 1>/dev/null 2>/dev/null
echo "Time consumption for runtime of the calculation of the edit distance between two words:"
time python3 runner.py "$1" "$2"
deactivate
rm -rf ./__pycache__ venv