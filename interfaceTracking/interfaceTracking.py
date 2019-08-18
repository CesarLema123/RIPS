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
import interfaceTrackingFunctions as ITF



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
#systemSize = 6
geometry = 'parallelogram'
#xSize, ySize, zSize =  9, 3, 3      # 2.__
#xSize, ySize, zSize =  12, 6 ,6      # 1.624
#xSize, ySize, zSize =  18, 6 ,6      # 1.901
#xSize, ySize, zSize =  15, 9, 9      # 1.966,1.815
#xSize, ySize, zSize =  21 , 9 , 9      # 1.901, 1.980
xSize, ySize, zSize =  6 , 3 , 3      # 1.901, 1.980

latConst = 3.63
dumpFilename = 'pos.XYZ'
logFilename = 'log.interfaceTracking'
thermoArgs = 'step atoms temp press etotal enthalpy' #since log file labels arent same as arguements, might have to make a dictionary with arguements as keys and log labels as value {etotal:}


#---------Creating Atom position Datafiles ---------------  # Currently DFG class does not work with float systemsizes, maybe fix if have time

DFGenerator = DFG.AtomDataFileGenerator(filename='CuNi_50%', latticeType='FCC', alloy='CuNi', atomTypes=2, alloyCompPercent = .5, geometry = geometry, xSize = xSize, ySize = ySize, zSize = zSize)

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
lmp.thermo_style('custom',thermoArgs)

#lmp.log('log.interfaceTracking')

lmp.compute('ptm all ptm/atom default 0.1') #*********
lmp.compute('cna all cna/atom',2.15) #********* seems to not be working properly
lmp.compute('centro all centro/atom 12') #*********
#lmp.dump(2,'all','custom',10,dumpFilename,'type','id','x','y','z','c_ptm[1]','c_centro','c_cna') dont use cna, to many errors
lmp.dump(2,'all','custom',10,dumpFilename,'type','id','x','y','z','c_ptm[1]','c_centro')

dumpLabel = 'id type x c_ptm[1] c_ptm[2] c_ptm[3] c_centro' # id first so it works with reader class, time step has to be at 0
dumpFN = 'atomParameters.data'
lmp.dump('PTMOutput','all','custom',10,dumpFN,dumpLabel)

lmp.log('log.interfaceTracking')
# ---------------------- Simulation Execution ----------------------------------

lmp.change_box('all','x','final',-2*latConst,2.5*xSize*latConst,'y','final',0,ySize*latConst,'z','final',0,zSize*latConst)

liqBox_xLow = (xSize)*latConst
liqBox_xUpp = (2*xSize)*latConst

lmp.region('liqRegion','block', liqBox_xLow, liqBox_xUpp,0,ySize*latConst,0,zSize*latConst)

lmp.create_atoms('2','random', DFGenerator.getNumAtoms(),1,'liqRegion')
lmp.group('liqAtoms region liqRegion')
#lmp.velocity('liqAtoms create 2000.0 321')
lmp.fix('liquify liqAtoms nvt temp 2000 2000 0.1')
#lmp.fix('1 liqAtoms nve/limit 0.05')



#DIVIDING EACH SOL/LIQ REGION INTO 3 SUB-REGIONS'
solBox_xLow = 0
solBox_xUpp = xSize*latConst
region1Fract = .05
region2Fract = .15
region3Fract = .8


lmp.region('liqRegion1','block',liqBox_xLow,liqBox_xLow+(xSize*latConst)*(region3Fract),0,ySize*latConst,0,zSize*latConst)
lmp.group('liqRegion1Atoms region liqRegion1')
lmp.region('liqRegion2','block',liqBox_xLow+(xSize*latConst)*(region3Fract),liqBox_xLow+(xSize*latConst)*(region3Fract+region2Fract),0,ySize*latConst,0,zSize*latConst)
lmp.group('liqRegion2Atoms region liqRegion2')
lmp.region('liqRegion3','block',liqBox_xLow+(xSize*latConst)*(region2Fract),liqBox_xUpp,0,ySize*latConst,0,zSize*latConst)
lmp.group('liqRegion3Atoms region liqRegion3')

lmp.region('solRegion1','block',solBox_xLow,solBox_xUpp*(region1Fract),0,ySize*latConst,0,zSize*latConst)
lmp.group('solRegion1Atoms region solRegion1')
lmp.region('solRegion2','block',solBox_xUpp*(region1Fract),solBox_xUpp*(region1Fract+region2Fract),0,ySize*latConst,0,zSize*latConst)
lmp.group('solRegion2Atoms region solRegion2')
lmp.region('solRegion3','block',solBox_xUpp*(region2Fract),solBox_xUpp,0,ySize*latConst,0,zSize*latConst)
lmp.group('solRegion3Atoms region solRegion3')

lmp.run(10)

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

#print(lmp.runs[0]._asdict().value)
lmp.run(1000)

# getting atom data






# ----------- Post Processing -----------------

# import plotter and plot total enrgy vs time
thermo_labels = 'Step Atoms Temp Press TotEng Enthalpy'

ThermoDF = OR.OutputReader(logFilename,'log',thermo_labels).getDataFrame()
dumpDF = OR.OutputReader(dumpFN,'dump',dumpLabel)    # need id as first dumplabel
simData =dumpDF.getNDArray()
#print(simData[0])

#OA.DataFrameAnalyzer(dumpDF.getDataFrame().xs(200),10).plotColumnAgainstRT('c_ptm[1]')
#OA.DataFrameAnalyzer(ThermoDF,10).plotColumnAgainstRT('TotEng')
#OA.DataFrameAnalyzer(ThermoDF,10).plotColumnAgainstRT('Enthalpy')


# use c_ptmp[1] and c_entro to find interface
#ptmData = np.array([simData[])




ptmData = simData[:,:,4].astype(float)
centroData = simData[:,:,7].astype(float)
xPositionData = simData[:,:,3].astype(float)



print(ITF.getInterfaceVelocity(ptmData,centroData,xPositionData,CentroLimit = 3, groupAtomsMaxError = .7))





'''

# --------- VISIUALIZATION ---------------------
# OPEN OVITO AND VISUALIZE POS.XYZ DATA
appDirectory = '/Applications/Ovito.app/Contents/MacOS/ovitos'
os.system(appDirectory + ' -g ' + 'vis.py')

'''









































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
