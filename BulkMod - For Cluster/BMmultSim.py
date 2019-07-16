#!/usr/bin/python3.6
"""
This file creates sequential data files and in files to run BM simulations for differing numbers of atoms
"""

import subprocess
#import bulkModulus as bm
import numpy as np
#import matplotlib.pyplot as mpl



tempInFile = 'in.bulkCuNi'
lmpsCMD = 'lmp_daily -in' #change this depending if running on cluster or locally

#create necessary data files
for i in range(2, 7):
    #i is an argument representing "num" in the writeData file - number of atoms along each axis
    datCMD = 'python writeData.py ' + str(i)
    subprocess.run(datCMD, shell = True)

#create necessary "in" files for LAMMPS
#BOTTOMFILE is constant - only change in "in" file is SIMNUM variable
BOTTOMFILE = "bottomBMin"

for simnum in range(2,7):

    NEWFILENAME = "in.bulkCuNi" + str(simnum)

    reader = open(BOTTOMFILE,mode = "r")
    writer = open(NEWFILENAME,mode = "w")
    writer.write("# ---------------- Define Variables ---------------\n")
    writer.write("variable\t\tSIMNUM string \"" + str(simnum) + "\"\n")
    for line in reader:
        writer.write(line)


#run multiple LAMMPS simulations in sequence
for i in range(2, 7): 
    #run the appropriate lammps input file
    inFile = tempInFile + str(i)
    simCMD = lmpsCMD + ' ' + inFile
    subprocess.run(simCMD, shell=True)
    print('Log file #', i, ' created.')


#print(result)
#mpl.plot(result[:,0], result[:,1])
#mpl.show()
