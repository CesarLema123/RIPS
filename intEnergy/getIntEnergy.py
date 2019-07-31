from lammps import lammps,PyLammps
import numpy as np
import makeDataFile as MDF
import sys

latConst = 4.046
#---------Creating Atom Data---------------
atomDataMaker = MDF.AtomData(latConst,sysSize=1)


#-----------------------------------------


_lmp = lammps()
_lmp.file('in.intEnergy')

lmp = PyLammps(ptr=_lmp)
print('-------------test--------------')
# check for what the sim region looks like

print(lmp.system)


lmp.region('solBase block 0 4.046 0 4.046 0 4.046')
lmp.group('solAtoms region solBase')

#lmp.lattice("fcc", 4.046) # using create_atom arguement random
#lmp.change_box('all x scale 2')
lmp.change_box('all x final 0 8.092 y final 0 4.046 z final 0 4.046  remap')
#lmp.region('liquidBox block 4.047 8.092 0 4.045 0 4.045')
lmp.region('liquidBox block 4.045 8.092 0 4.046 0 4.046')

#lmp.create_atoms('2 random 100 ' + str(np.random.random(1)[0]) + ' liquidBox') #using changing random seed
lmp.create_atoms('2 random 100 10 liquidBox')
lmp.group('liquidAtoms region liquidBox')
lmp.delete_atoms('region liquidBox')


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

