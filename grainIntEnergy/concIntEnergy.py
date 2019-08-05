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
alloy1 = DFG.AtomDataFileGenerator('conc9',systemSize=6,alloyCompPercent=.9)
alloy1.createDataFile()
print('alloy1 concentration is: ', alloy1.getActualCompPercent())
alloy2 = DFG.AtomDataFileGenerator('conc1', systemSize = 6, alloyCompPercent=.1)
alloy2.createDataFile()
print('alloy2 concentration is: ', alloy2.getActualCompPercent())
#alloyDG = DFG.AtomDataFileGenerator('atoms',systemSize=10,alloy='custom',alloyCompPercent=.5,customLatticeConst=1.815)


#-----------------------------------------


_lmp = lammps()
_lmp.file('in.concIntEnergy')

lmp = PyLammps(ptr=_lmp)
print('-------------test--------------')
# check for what the sim region looks like

print(lmp.system)

latConst = 3.63
systemSize = 6
lmp.read_data('data.conc9', 'add', 'append', 'shift', latConst*systemSize, 0, 0, 'group', 'conc9Atoms')

#lmp.region('solBase block 0 3.63 0 3.63 0 3.63 side in') # solid Right interface is at systemSize*3.63 = 5*latConst
#lmp.group('solAtoms region solBase')


#lmp.change_box('all','x','final',-2*latConst,20*latConst,'y','final',-0*latConst,5*latConst,'z','final',-0*latConst,5*latConst)


# --------------- Data Output -----------------------------
lmp.reset_timestep(0)
lmp.timestep(0.001)     #pico
lmp.thermo(100)
lmp.thermo_style('custom step atoms temp press etotal')

lmp.dump(2,'all','custom',10,'pos.XYZ','id','type','x','y','z')

# ------------------ Runs ----------------------
#lmp.minimize('1e-7 1e-7 10000 10000')

print('\n',lmp.groups)

lmp.fix(0, 'all', 'nve')
lmp.fix(1, 'all', 'langevin', 2000, 2000, 0.1, 761, 'zero', 'yes')
lmp.run(10000)

print(lmp.system)
# COMPUTES



# RUNS



# FIXES

# DUMPS






# ----------- Post Processing -----------------

# import plotter and plot total enrgy vs time
thermo_labels = 'Step Atoms Temp Press TotEng'

df = OR.LogReader('log.concIntEnergy','Step Atoms Temp Press TotEng').getDataframe()
OA.DataFrameAnalyzer(df,100).plotColumnAgainstRT('TotEng')


# --------- VISIUALIZATION ---------------------
# OPEN OVITO AND VISUALIZE POS.XYZ DATA
appDirectory = '~/Downloads/ovito-2.9.0-x86_64/bin/ovitos'
os.system(appDirectory + ' -g ' + 'vis.py')


