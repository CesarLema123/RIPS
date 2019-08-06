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
This file runs three simulations: two at the given pure alloy concentrations, and one with two regions
at the given concentrations, and an interface between them. This is used for calculating solid-solid
interfacial energy for a compositional interface.
'''
#---------Set Parameters----------------
CONC1 = 0.8
CONC2 = 0.1
TEMP = 400
SYS_SIZE = 4
LAT_CONST = 3.63


#---------Creating Atom Data---------------
alloy1 = DFG.AtomDataFileGenerator('conc1',systemSize=SYS_SIZE,alloyCompPercent=CONC1)
alloy1.createDataFile()
print('alloy1 concentration is: ', alloy1.getActualCompPercent())
alloy2 = DFG.AtomDataFileGenerator('conc2', systemSize = SYS_SIZE, alloyCompPercent=CONC2)
alloy2.createDataFile()
print('alloy2 concentration is: ', alloy2.getActualCompPercent())

_lmp = lammps()
_lmp.file('in.concIntEnergy')

lmp = PyLammps(ptr=_lmp)

#---------Run Pure Conc1 Simulation---------------
print('-------------pure conc1--------------')
# check for what the sim region looks like

print(lmp.system)
lmp.log('log.Conc1') 
lmp.read_data('data.conc1', 'add', 'append', 'shift', LAT_CONST*SYS_SIZE, 0, 0)


#Data Output Pure Conc1
lmp.reset_timestep(0)
lmp.timestep(0.001)     
lmp.thermo(100)
lmp.thermo_style('custom step atoms temp vol press pe etotal')

lmp.dump(1,'all','custom',10,'conc1.XYZ','id','type','x','y','z')

#Run Pure Conc1
print('\n',lmp.groups)

lmp.fix(0, 'all', 'nve')
lmp.fix(1, 'all', 'langevin', TEMP, TEMP, 0.1, 761, 'zero', 'yes')
lmp.run(10000)

print(lmp.system)


# Post Processing Pure Conc1
thermo_labels = 'Step Atoms Temp Volume Press PotEng TotEng'

dfConc1 = OR.LogReader('log.Conc1',thermo_labels).getDataframe()
OA.DataFrameAnalyzer(dfConc1,100).plotColumnAgainstRT('TotEng', fileName = 'pureConc1') 


#---------Run Pure Conc2 Simulation---------------
lmp.delete_atoms('group', 'all')
print('-------------pure conc2--------------')
# check for what the sim region looks like
print(lmp.system)

lmp.log('log.Conc2')
lmp.read_data('data.conc2','add', 'append')
lmp.read_data('data.conc2', 'add', 'append', 'shift', LAT_CONST*SYS_SIZE, 0, 0, 'group', 'conc2Atoms')


# Data Output Pure Conc2
lmp.reset_timestep(0)
lmp.timestep(0.001)
lmp.thermo(100)
lmp.thermo_style('custom step atoms temp vol press pe etotal')

lmp.dump(2,'all','custom',10,'conc2.XYZ','id','type','x','y','z')

# Run Pure Conc2
print('\n',lmp.groups)

lmp.fix(0, 'all', 'nve')
lmp.fix(1, 'all', 'langevin', TEMP, TEMP, 0.1, 761, 'zero', 'yes')
lmp.run(10000)

print(lmp.system)


# Post Processing Pure Conc2
thermo_labels = 'Step Atoms Temp Volume Press PotEng TotEng'

dfConc2 = OR.LogReader('log.Conc2',thermo_labels).getDataframe()
OA.DataFrameAnalyzer(dfConc2,100).plotColumnAgainstRT('TotEng', fileName = 'pureConc2')



#---------Run Mixed Concentrations Simulation---------------
lmp.delete_atoms('group', 'all')
print('-------------mixed--------------')
# check for what the sim region looks like
print(lmp.system)

lmp.log('log.mixedConc') #CHANGE THIS FOR OTHER SIMS
lmp.read_data('data.conc1','add', 'append', 'group', 'conc1Atoms')
lmp.read_data('data.conc2', 'add', 'append', 'shift', LAT_CONST*SYS_SIZE, 0, 0, 'group', 'conc2Atoms')


# Data Output Mixed
lmp.reset_timestep(0)
lmp.timestep(0.001)
lmp.thermo(100)
lmp.thermo_style('custom step atoms temp vol press pe etotal')

lmp.dump(3,'all','custom',10,'mixed.XYZ','id','type','x','y','z')

# Run Mixed
print('\n',lmp.groups)

lmp.fix(0, 'all', 'nve')
lmp.fix(1, 'all', 'langevin', TEMP, TEMP, 0.1, 761, 'zero', 'yes')
lmp.run(10000)

print(lmp.system)


# Post Processing Mixed 
thermo_labels = 'Step Atoms Temp Volume Press PotEng TotEng'

dfMixed = OR.LogReader('log.mixedConc',thermo_labels).getDataframe()
OA.DataFrameAnalyzer(dfMixed,100).plotColumnAgainstRT('TotEng', fileName = 'mixedConc') 

#----------Post Processing for concInterfaceEng-------------
raw_data = {
        'Step': dfMixed['Step'].values,
        'TotEng1': dfConc1['TotEng'].values,
        'TotEng2': dfConc2['TotEng'].values,
        'TotEngMix': dfMixed['TotEng'].values}
combineDF = pd.DataFrame(raw_data, columns = ['Step', 'TotEng1', 'TotEng2', 'TotEngMix'])
print(combineDF.head())
OA.DataFrameAnalyzer(combineDF,100).concInterfaceEng()


# --------- VISIUALIZATION ---------------------
# OPEN OVITO AND VISUALIZE POS.XYZ DATA
appDirectory = '~/Downloads/ovito-2.9.0-x86_64/bin/ovitos'
os.system(appDirectory + ' -g ' + 'vis.py')


