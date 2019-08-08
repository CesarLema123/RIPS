from lammps import lammps,PyLammps
import numpy as np
import dataFileGenerator as DFG
import sys
import os

import pandas as pd
import matplotlib.pyplot as plt
import outputAnalyzer as OA
import outputReader as OR
import matplotlib.pyplot as plt

'''
class SimunlationConstants:
    def __init__(self):
        self.systemSize = 5


class InterfaceEnergySimulation:
    def __init__(self):
        <code>
'''

#--------- Setting Simulating Parameters ---------------  # Currently DFG class does not work with float systemsizes, maybe fix if have time


# Sim = simulation(...)
systemSize = 6
latConst = 3.63
dumpFilename = 'pos.XYZ'
logFilename = 'log.interfaceTracking'
thermoArgs = 'custom step atoms temp press etotal enthalpy' #since log file labels arent same as arguements, might have to make a dictionary with arguements as keys and log labels as value {etotal:}


#---------Creating Atom position Datafiles ---------------  # Currently DFG class does not work with float systemsizes, maybe fix if have time

DFGenerator = DFG.AtomDataFileGenerator(filename='CuNi_50%', latticeType='FCC', alloy='CuNi', atomTypes=2, alloyCompPercent = .5, systemSize = systemSize)

#add some method that can go into lammps in file and sets readdata finename in input file

# DATAFILE FOR RECTANGULAR BOX OF ATOMS W/ 0% Cu
DFGenerator.createDataFile()
print('Copper comp value: ',DFGenerator.getActualCompPercent())

#--------------- Initializing LAMMPS Simulation --------------------------
_lmp = lammps()
_lmp.file('in.AlloySimulationSetup')

lmp = PyLammps(ptr=_lmp)

# ----------------------- Output settings ---------------------------
lmp.reset_timestep(0)
lmp.thermo(10)
lmp.thermo_style(thermoArgs)

lmp.compute('ptm all ptm/atom default 0.1') #*********
lmp.dump(2,'all','custom',10,dumpFilename,'type','id','x','y','z','c_ptm[1]')
lmp.log('log.interfaceTracking')
# ---------------------- Simulation Execution ----------------------------------

lmp.change_box('all','x','final',-2*latConst,2.5*systemSize*latConst,'y','final',0,systemSize*latConst,'z','final',0,systemSize*latConst)

liqBox_xLow = (systemSize)*latConst
liqBox_xUpp = (2*systemSize)*latConst

lmp.region('liqRegion','block', liqBox_xLow, liqBox_xUpp,0,systemSize*latConst,0,systemSize*latConst)

lmp.create_atoms('2','random', DFGenerator.getNumAtoms(),1,'liqRegion')
lmp.group('liqAtoms region liqRegion')
#lmp.velocity('liqAtoms create 2000.0 321')
lmp.fix('liquify liqAtoms nvt temp 2000 2000 0.1')
#lmp.fix('1 liqAtoms nve/limit 0.05')

lmp.run(10)

#DIVIDING EACH SOL/LIQ REGION INTO 3 SUB-REGIONS'
solBox_xLow = 0
solBox_xUpp = systemSize*latConst

lmp.region('liqRegion1','block',liqBox_xLow,liqBox_xLow+(systemSize*latConst)*(1/3),0,systemSize*latConst,0,systemSize*latConst)
lmp.group('liqRegion1Atoms region liqRegion1')
lmp.region('liqRegion2','block',liqBox_xLow+(systemSize*latConst)*(1/3),liqBox_xLow+(systemSize*latConst)*(2/3),0,systemSize*latConst,0,systemSize*latConst)
lmp.group('liqRegion2Atoms region liqRegion2')
lmp.region('liqRegion3','block',liqBox_xLow+(systemSize*latConst)*(2/3),liqBox_xUpp,0,systemSize*latConst,0,systemSize*latConst)
lmp.group('liqRegion3Atoms region liqRegion3')

lmp.region('solRegion1','block',solBox_xLow,solBox_xUpp*(1/3),0,systemSize*latConst,0,systemSize*latConst)
lmp.group('solRegion1Atoms region solRegion1')
lmp.region('solRegion2','block',solBox_xUpp*(1/3),solBox_xUpp*(2/3),0,systemSize*latConst,0,systemSize*latConst)
lmp.group('solRegion2Atoms region solRegion2')
lmp.region('solRegion3','block',solBox_xUpp*(2/3),solBox_xUpp,0,systemSize*latConst,0,systemSize*latConst)
lmp.group('solRegion3Atoms region solRegion3')

lmp.fix('solConstE solRegion3Atoms nve')
lmp.fix('liqConstE liqRegion1Atoms nve')
lmp.fix('solConstT solRegion2Atoms langevin 1600.0 1600.0 0.01 3746823')
lmp.fix('liqConstT liqRegion2Atoms langevin 2000.0 2000.0 0.01 37496823')
lmp.fix('solNullForce solRegion1Atoms setforce 0 0 0')
#lmp.fix('liqBath liqRegion3Atoms nve')
lmp.fix('liqNullForce liqRegion3Atoms setforce 0 0 0') # should create a particle bath instead of this


''' delete specified region 
lmp.run(10)
lmp.delete_atoms('group solRegion1Atoms')
lmp.run(10)
lmp.delete_atoms('group solRegion2Atoms')
lmp.run(10)
lmp.delete_atoms('group solRegion3Atoms')
lmp.run(10)
lmp.delete_atoms('group liqRegion1Atoms')
lmp.run(10)
lmp.delete_atoms('group liqRegion2Atoms')
lmp.run(10)
lmp.delete_atoms('group liqRegion3Atoms')
'''

#lmp.compute('ptm all ptm/atom default 0.1')
lmp.dump('PTMOutput','all','custom',10,'PTMData.data','type','id','c_ptm[1] c_ptm[2] c_ptm[3] ')
#print(lmp.runs[0]._asdict().value)

lmp.run(1000)





'''


# ----------- Post Processing -----------------

# import plotter and plot total enrgy vs time
thermo_labels = 'Step Atoms Temp Press TotEng Enthalpy'

df = OR.LogReader(logFilename,thermo_labels).getDataframe()
OA.DataFrameAnalyzer(df,100).plotColumnAgainstRT('TotEng')
OA.DataFrameAnalyzer(df,100).plotColumnAgainstRT('Enthalpy')
'''

# --------- VISIUALIZATION ---------------------
# OPEN OVITO AND VISUALIZE POS.XYZ DATA
appDirectory = '/Applications/Ovito.app/Contents/MacOS/ovitos'
os.system(appDirectory + ' -g ' + 'vis.py')


















''' code for Data Analysis/extracting data using pylammps
    
print(lmp.computes)
lmp.run(1000)

print('*********************************************\n')
labels = []

print(lmp.runs[0].thermo.__dict__.keys())
for key in lmp.runs[0].thermo.__dict__:
    labels.append(key)

print(labels)

#print(lmp.runs[0].thermo.__dict__)
print(lmp.runs[0].thermo.Atoms)
print('\nlmp.runs[0].thermo.__dict__: \n',dir(lmp.runs[0].thermo.__dict__))
print('\nlmp.runs[0].thermo: \n',dir(lmp.runs[0].thermo))
print('\nlmp.runs[0]: \n',dir(lmp.runs[0]))
print('\nlmp.runs: \n',dir(lmp.runs))

steps = lmp.runs[0].thermo.Step
temp = lmp.runs[0].thermo.Temp

plt.plot(steps, temp)
plt.grid()
plt.show


'''



















# Testing code
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
