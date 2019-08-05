from lammps import lammps,PyLammps
import numpy as np
import dataFileGenerator as DFG
import sys
import os

import pandas as pd
import matplotlib.pyplot as plt
import outputAnalyzer as OA
import outputReader as OR

'''
class SimunlationConstants:
    def __init__(self):
        self.systemSize = 5


class InterfaceEnergySimulation:
    def __init__(self):
        <code>
'''

#---------Creating Atom Data---------------
alloyDG = DFG.AtomDataFileGenerator('atoms',systemSize=5,alloyCompPercent=.5)
#alloyDG = DFG.AtomDataFileGenerator('atoms',systemSize=10,alloy='custom',alloyCompPercent=.5,customLatticeConst=1.815)

alloyDG.createDataFile()             # method creates and add data file locally
print(" ************ created datafile sucessfully ************* ")

#alloyDG.setSystemSize(4) #update size of atom box [1*latticeConst => 4*latticeConst]
#alloyDG.createDataFile()

#-----------------------------------------


_lmp = lammps()
_lmp.file('in.intEnergy')

lmp = PyLammps(ptr=_lmp)
print('-------------test--------------')
# check for what the sim region looks like

print(lmp.system)


lmp.region('solBase block 0 3.63 0 3.63 0 3.63 side in') # solid Right interface is at systemSize*3.63 = 5*latConst
lmp.group('solAtoms region solBase')


latConst = 3.63
lmp.change_box('all','x','final',-2*latConst,20*latConst,'y','final',-0*latConst,5*latConst,'z','final',-0*latConst,5*latConst)


lmp.region('liquidBox','block', 7*latConst, 12*latConst, 0, 5*latConst, 0, 5*latConst,'side','in')

#lmp.create_atoms('2 random 500 ' + str(int(10*np.random.random(1)[0])) + ' liquidBox') # create atom using different seed each run
lmp.create_atoms('2 random 500 1 liquidBox')

lmp.group('liquidAtoms region liquidBox')
#lmp.delete_atoms('group liquidAtoms')


# --------------- Data Output -----------------------------
lmp.reset_timestep(0)
lmp.timestep(0.001)     #pico
lmp.thermo(10)
lmp.thermo_style('custom step atoms temp press etotal')

lmp.dump(2,'all','custom',10,'pos.XYZ','id','x','y','z')


# ------------------ Runs ----------------------
lmp.minimize('1e-7 1e-7 10000 10000')

print('\n',lmp.groups)

lmp.fix('solTemp solAtoms nvt temp 600 600 0.1')   # -------- use
lmp.fix('liqTemp liquidAtoms nvt temp 3000 3000 0.1')     # -------- use
lmp.run(400)


# MOVE LIQUID ATOMS CLOSE TO INTERFACE
for i in range(21):
    lmp.minimize('1e-4 1e-4 10000 10000')
    lmp.displace_atoms('liquidAtoms','move', -.1*latConst, 0, 0)
    lmp.run(20)

lmp.minimize('1e-2 1e-2 10000 10000')

For Fun/cool visualization
lmp.run(200)

for i in range(21):
    lmp.minimize('1e-4 1e-4 10000 10000')
    lmp.displace_atoms('liquidAtoms','move', -1*latConst, 0, 0)
    lmp.run(10)
    
#lmp.delete_atoms('region solBase')

# FIXEACH GROUP OF ATOMS TO A SPECIFIC TEMP
#lmp.fix('solTemp solAtoms nvt temp 1000 1000 0.01')   # -------- use
#lmp.fix('liqTemp liquidAtoms nvt temp 3000 3000 0.01')     # -------- use
#lmp.run(1000)          # -------- use

#lmp.compute('mobile all temp')
#lmp.velocity('all create 1.0 482748 temp mobile')
lmp.fix('1 all nve')       # -------- use
lmp.run(500)
#lmp.dump(2,'all','custom',10,'pos.XYZ','id','x','y','z')
lmp.run(10000)

print(lmp.system)
# COMPUTES



# RUNS



# FIXES

# DUMPS






# ----------- Post Processing -----------------

# import plotter and plot total enrgy vs time
thermo_labels = 'Step Atoms Temp Press TotEng'

df = OR.LogReader('log.intEnergy','Step Atoms Temp Press TotEng').getDataframe()
OA.DataFrameAnalyzer(df,100).plotColumnAgainstRT('TotEng')





# --------- VISIUALIZATION ---------------------
# OPEN OVITO AND VISUALIZE POS.XYZ DATA
appDirectory = '/Applications/Ovito.app/Contents/MacOS/ovitos'
os.system(appDirectory + ' -g ' + 'vis.py')






































# OLD CODE
'''
_lmp = lammps()
_lmp.file('in.intEnergy')

lmp = PyLammps(ptr=_lmp)
print('-------------test--------------')
# check for what the sim region looks like

print(lmp.system)


lmp.region('solBase block 0 3.63 0 3.63 0 3.63 side in') # solid Right interface is at systemSize*3.63 = 5*latConst
lmp.group('solAtoms region solBase')

#lmp.lattice("fcc", 4.046)
#lmp.change_box('all x scale 2')
#lmp.change_box('all x final 0 7.26 y final 0 3.63 z final 0 3.63  remap')
latConst = 3.63
lmp.change_box('all','x','final',-2*latConst,20*latConst,'y','final',-0*latConst,5*latConst,'z','final',-0*latConst,5*latConst)

#lmp.region('liquidBox block 4.047 8.092 0 4.045 0 4.045')
#lmp.region('liquidBox block 4.047 8.092 0 4.046 0 4.046')
lmp.region('liquidBox','block', 6*latConst, 11*latConst, 0, 5*latConst, 0, 5*latConst,'side','in')

#lmp.create_atoms('2 random 100 ' + str(np.random.random(1)[0]) + ' liquidBox') #using changing random seed
lmp.create_atoms('2 random 1000 1 liquidBox')
lmp.group('liquidAtoms region liquidBox')
#lmp.delete_atoms('group liquidAtoms')

lmp.dump(2,'all','custom',10,'pos.XYZ','id','x','y','z')

#lmp.minimize('1e-3 1e-3 10000 10000')
lmp.minimize('1e-6 1e-6 10000 10000')

print('\n',lmp.groups)

# MOVE LIQUID ATOMS CLOSE TO INTERFACE
for i in range(30):
    
    lmp.displace_atoms('liquidAtoms','move', -1*latConst, 0, 0)
    lmp.run(50)



# FIXEACH GROUP OF ATOMS TO A SPECIFIC TEMP
#lmp.fix('solTemp solAtoms nvt temp 1000 1000 0.01')   # -------- use
#lmp.fix('liqTemp liquidAtoms nvt temp 3000 3000 0.01')     # -------- use
#lmp.run(1000)          # -------- use

#lmp.compute('mobile all temp')
#lmp.velocity('all create 1.0 482748 temp mobile')
lmp.fix('1 all nve')
lmp.run(1000)
#lmp.dump(2,'all','custom',10,'pos.XYZ','id','x','y','z')
lmp.run(1000)

print(lmp.system)

'''
