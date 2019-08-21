#!/bin/bash

# Add the location of the python scripts to PYTHONPATH (path/to/RIPS/lib/PyScripts)
export PYTHONPATH="$HOME/git-RIPS/RIPS/lib/PyScripts:$PYTHONPATH"

# Run the thermal expansion python script
python3 runThermExp.py
