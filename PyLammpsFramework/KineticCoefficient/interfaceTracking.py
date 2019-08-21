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
    This script calculates the velocity of a solid-liquid interface
    
    
    
'''


#------------------------------- Simulating Parameters ----------------------------------

###########################################################################################
### Currently DFG class does not work with float systemsizes, maybe fix if have time ######
###########################################################################################

# Sim = simulation(...)
geometry = 'parallelogram'
xSize, ySize, zSize =  15 , 9 , 9
#xSize, ySize, zSize =  9 , 6 , 6

latConst = 3.63
atomPositionFilename = 'pos.XYZ'
FCCAtomDataFilename = 'atomParameters.data'
logFilename = 'log.interfaceTracking'
thermoArgs = 'step atoms temp press etotal enthalpy' #since log file labels arent same as arguements, might have to make a dictionary with arguements as keys and log labels as value {etotal:}
FCCAtomDumpArgs = 'id type x c_ptm[1] c_centro' # id first so it works with reader class, time step has to begin at 0; not sure if this is still true


#--------------------- Creating Datafile with Initial Atom positons ----------------------

###########################################################################################
### Uses DataFileGenerator class to create CuNi body with specified %composition ######
###########################################################################################

DFGenerator = DFG.AtomDataFileGenerator(filename='CuNi_50%', latticeType='FCC', alloy='CuNi', atomTypes=2, alloyCompPercent = .5, geometry = geometry, xSize = xSize, ySize = ySize, zSize = zSize)
# consider adding DFG method write read_data filename in lammps input file

DFGenerator.createDataFile()                                          # creates CuNi (50% compositon) Datafile with atoms in lattice points
print('Copper comp value: ', DFGenerator.getActualCompPercent())      # prints actual percentage of copper atoms

#--------------------------- Initializing LAMMPS Simulation ---------------------------------

###########################################################################################################
### Uses PyLammps module to create a simulation file and run a lammps setup input file                 ####
### consider having simulation class use PyLammps to run setup commands instead of running input file  ####
###########################################################################################################

lmp = PyLammps()
lmp.file('in.AlloySimulationSetup')
lmp.log('log.interfaceTracking')

# ---------------------------- Simulation Output Settings -----------------------------------
lmp.compute('ptm all ptm/atom default 0.1')                 # compute commands for PTM
lmp.compute('centro all centro/atom 12')                    # compute commands for centro-symmetry paramter

lmp.reset_timestep(0)
lmp.thermo(10)
lmp.thermo_style('custom',thermoArgs)
lmp.dump('positionOutput','all','custom',10,atomPositionFilename,'type id x y z')      # output file with data to visualize movement of atoms
lmp.dump('PTMOutput','all','custom',10,FCCAtomDataFilename,FCCAtomDumpArgs)            # output file with data to find interface atoms

# ------------------------------- Simulation Setup ---------------------------------------

lmp.change_box('all','x','final',-2*latConst,2.5*xSize*latConst,'y','final',0,ySize*latConst,'z','final',0,zSize*latConst)    #resize simulation box to fit solid and liquid regions

liqBox_xLow = (xSize)*latConst
liqBox_xUpp = (2*xSize)*latConst

lmp.region('liqRegion','block', liqBox_xLow, liqBox_xUpp,0,ySize*latConst,0,zSize*latConst)

lmp.create_atoms('2','random', DFGenerator.getNumAtoms(),1,'liqRegion')
lmp.group('liqAtoms region liqRegion')
#lmp.fix('liquify liqAtoms nvt temp 2000 2000 0.1')


# DIVIDING EACH SOL/LIQ REGION INTO 3 SUB-REGIONS
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

#lmp.fix('solConstT1 solRegion2Atoms langevin 2100.0 2100.0 0.01 3746823')
solTemp = 3000

lmp.fix('liqNullForce liqAtoms setforce 0 0 0')
lmp.fix('solConstT1 solRegion3Atoms nvt temp',solTemp,solTemp,.1)
lmp.fix('solConstT2 solRegion2Atoms nvt temp',solTemp,solTemp,.1)

lmp.run(500)

lmp.unfix('liqNullForce')
lmp.unfix('solConstT1')
lmp.unfix('solConstT2')
lmp.fix('liquify liqAtoms nvt temp 2000 2000 0.1')

lmp.run(10)

lmp.fix('solConstE solRegion3Atoms nve')
lmp.fix('liqConstE liqRegion1Atoms nve')
lmp.fix('solConstT solRegion2Atoms langevin',solTemp,solTemp,0.01,3746823)
lmp.fix('liqConstT liqRegion2Atoms langevin 2000.0 2000.0 0.01 37496823')
lmp.fix('solNullForce solRegion1Atoms setforce 0 0 0')
#lmp.fix('liqBath liqRegion3Atoms nve')
lmp.fix('liqNullForce liqRegion3Atoms setforce 0 0 0')                # should create a particle bath instead removing all forces from atoms

# ------------------------------ Execute Simulation -----------------------------------------------

##########################################################################################################
### Run simulation multiple times, dump to respective file for post processing                         ###
### edit simulation parameters to find dependence relations ships                                      ###
### consider makig this script a class (interface velocity tracker for 1 set of simulation parameters) ###
### then use another python script to run multiple interfaceTracking simulations                       ###
##########################################################################################################

lmp.run(1000)

# -------------------------------- Post Processing ---------------------------------------------

###########################################################################################
### Uses OutputReader class to get atoms data as ndarray for analaysis                  ###
### Uses interfaceTrackingFunctions to find get interface velocity using atom data      ###
###########################################################################################

thermo_labels = 'Step Atoms Temp Press TotEng Enthalpy'                      # data header labels from log file, not the same syntax as the thermo arguments

thermoReader = OR.OutputReader(logFilename,'log',thermo_labels)
dumpReader = OR.OutputReader(FCCAtomDataFilename,'dump',FCCAtomDumpArgs)     # need id as first FCCAtomDumpArgs
atomSimData =dumpReader.getNDArray()
ptmData = atomSimData[:,:,4].astype(float)                                   # matrix of PTM data for each atom, row is atom number and col is data values
centroData = atomSimData[:,:,5].astype(float)                                # matrix of centro data for each atom
xPositionData = atomSimData[:,:,3].astype(float)                             # matrix of xposition data for each atom

interfaceVelocity = ITF.getInterfaceVelocity(ptmData,centroData,xPositionData,CentroLimit = 3, groupAtomsMaxError = .7) # uses PTM and centro-symmetry fata to find mean Xposition vector of FCC atom groups that interaxt with the S-L interface
print(interfaceVelocity)



'''
# --------- VISIUALIZATION ---------------------
# OPEN OVITO AND VISUALIZE POS.XYZ DATA
appDirectory = '/Applications/Ovito.app/Contents/MacOS/ovitos'
os.system(appDirectory + ' -g ' + 'vis.py')
'''












