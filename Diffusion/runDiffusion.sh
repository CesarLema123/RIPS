#!/bin/bash


# Add the location of the python scripts to PYTHONPATH (path/to/RIPS/lib/PyScripts)
export PYTHONPATH="$HOME/Research/git-RIPS/RIPS/lib/PyScripts:$PTHONPATH"

# Run the diffusion python script
python3 runDiffusion.py
