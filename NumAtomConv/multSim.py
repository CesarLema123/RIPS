#!/usr/bin/env
"""
This file runs sequential in files from LAMMPS and process each in sequence to produce an array of number of atoms vs. diffusion coefficients. It requires that numerically labelled in files and data files already exist in cd.
"""
import subprocess
import computeD as cD
import numpy as np
import matplotlib.pyplot as mpl

tempInFile = 'in.Cu'
lmpsCMD = 'lammps.q'
result = np.zeros((10,2))
for i in range(2, 12): 
    #run the appropriate lammps input file
    inFile = tempInFile + str(i)
    logFile = 'log' + str(i) + '.lammps'
    simCMD = lmpsCMD + ' ' + inFile
    print(simCMD)
    subprocess.run(simCMD, shell=True)
    print('Log file #', i, ' created.')
#    compCMD = 'python computeD.py ' + logFile + str(2) 
#    subprocess.run(compCMD)
    #store the 'num' parameter used in writedata.py next to the compute Diffusion coefficient
    result[i-2, 0] = i
    result[i-2, 1] = cD.findDiff(logFile)

print(result)
mpl.plot(result[:,0], result[:,1])
mpl.savefig('img.png')
