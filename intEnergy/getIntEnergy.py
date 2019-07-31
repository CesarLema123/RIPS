from lammps import lammps,PyLammps
import numpy as np
import dataFileGenerator as DFG
import sys

#---------Creating Atom Data---------------
alloyDG = DFG.AtomDataFileGenerator('atom',systemSize=1,alloyCompPercent=.5)
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


lmp.region('solBase block 0 4.046 0 4.046 0 4.046')
lmp.group('solAtoms region solBase')

#lmp.lattice("fcc", 4.046)
#lmp.change_box('all x scale 2')
lmp.change_box('all x final 0 8.092 y final 0 4.046 z final 0 4.046  remap')
#lmp.region('liquidBox block 4.047 8.092 0 4.045 0 4.045')
#lmp.region('liquidBox block 4.047 8.092 0 4.046 0 4.046')
lmp.region('liquidBox block 5 6 3 4 3 4')

#lmp.create_atoms('2 random 100 ' + str(np.random.random(1)[0]) + ' liquidBox') #using changing random seed
lmp.create_atoms('2 random 6 10 liquidBox')
lmp.group('liquidAtoms region liquidBox')
#lmp.delete_atoms('region liquidBox')
lmp.delete_atoms('group solAtoms')


print('\n',lmp.groups)
#lmp.compute('mobile all temp')
#lmp.velocity('all create 1.0 482748 temp mobile')
lmp.fix('1 all nve')
lmp.run(400)
lmp.dump(2,'all','custom',10,'pos.XYZ','id','x','y','z')
lmp.run(400)
#lmp.minimize('1 1 1000 1000')
print(lmp.system)
# COMPUTES



# RUNS



# FIXES

# DUMPS

