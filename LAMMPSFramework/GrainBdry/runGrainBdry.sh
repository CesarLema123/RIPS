#!/bin/bash

# Please make sure that you have a python3 command

# Appending the path to the python scripts to the PYTHONPATH variable
export PYTHONPATH="$HOME/git-RIPS/RIPS/LAMMPSFramework/lib/PyScripts:$PYTHONPATH" # Laptop

python3 runGrainBdry.py
