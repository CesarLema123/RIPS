#-------------------------------------------------------#
# Generate LAMMPS data file using crystalline metal     #
#     atom positions                                         #
#                                                         #
#     - Bradley Huddleston, April 15, 2018                #
#-------------------------------------------------------#

import numpy as np

'''
def nucleation:
    ...
'''
# Lattice parameter for aluminum
lattice_parameter = 4.046

# Number of atom types
atomTypes = 2

# Cubic FCC basis
basis = np.array([[1.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0],
                  [0.0, 0.0, 1.0]])*lattice_parameter

base_atoms = np.array([[0.0, 0.0, 0.0],
                       [0.5, 0.5, 0.0],
                       [0.5, 0.0, 0.5],
                       [0.0, 0.5, 0.5]])*lattice_parameter

''' simple cubic base atoms
base_atoms = np.array([[0.0, 0.0, 0.0],
                       [1, 1, 0.0],
                       [1, 0.0, 1],
                       [0.0, 1, 1]])*lattice_parameter '''

# Size of the system cell in lattice units
#    assuming an cubic cell starting at the origin
system_size = 5

#PERCENT COMPOSITION of Ni [2]
cPercent = .4
cMax = 4*(system_size**3)*cPercent  # max num of Ni atoms
cCounter  = 0                         # number of current Ni atoms
cbias = .70      # percent random number has to be above to become Ni [2]



#NUCLEATIONCOUNTER
nPercent = .0
nMax = 4*(system_size**3)*nPercent
nCounter = 0
#nRand
nbias = .80


# Generate atom positions
positions = []
for i in range(system_size):
    for j in range(system_size):
        for k in range(system_size):
            base_position = np.array([i,j,k])
            cart_position = np.inner(basis.T, base_position) #basically resizes basis vectors to point to poistion on 3D lattice grid
            nRand = np.random.random(1)[0]
            for atom in base_atoms:
                randUnitDirection = np.random.random((3))
                if nRand > nbias and nCounter <= nMax:
                    positions.append(cart_position + atom*.3)
                    nCounter+=1
                else:
                    positions.append(cart_position + atom)  #sets up atoms so they follow fcc laticce instead of cartesian points
#print("-----------atom vect: ",atom,' directional vect: ',randUnitDirection,' new: ',atom*randUnitDirection)
print("nMax: ",nMax,"  nCounter: ",nCounter,"  #UnitLattices: ",system_size**3,"  #Clummpedlattices: ",(system_size**3)*nPercent)

# Write LAMMPS data file
with open('crystalline.data','w') as fdata:
    # First line is a comment line
    fdata.write('Crystalline Al atoms - written for EnCodeVentor tutorial\n\n')
    
    #--- Header ---#
    # Specify number of atoms and atom types
    fdata.write('{} atoms\n'.format(len(positions)))
    fdata.write('{} atom types\n'.format(atomTypes))
    # Specify box dimensions
    fdata.write('{} {} xlo xhi\n'.format(0.0, system_size*lattice_parameter))
    fdata.write('{} {} ylo yhi\n'.format(0.0, system_size*lattice_parameter))
    fdata.write('{} {} zlo zhi\n'.format(0.0, system_size*lattice_parameter))
    fdata.write('\n')
    
    # Atoms section
    fdata.write('Atoms\n\n')
    
    # Write each position
    for i,pos in enumerate(positions):
        cRand = np.random.random(1)[0]
        if cRand > cbias and cCounter <= cMax:
            fdata.write('{} {} {} {} {}\n'.format(i+1,2,*pos))
            cCounter+=1
        else:
            fdata.write('{} {} {} {} {}\n'.format(i+1,1,*pos))
    print("cMax: ",cMax,"  cCounter: ",cCounter,"  #Atoms ",4*system_size**3, " Target%Composition: ", cPercent, "  %CompositionCu: ",cCounter/(4*system_size**3))

# If you have bonds and angles, further sections below

