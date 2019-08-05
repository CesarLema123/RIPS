import numpy as np

AlloyLatticeConsts = {'CuNi': 3.63,'custom': 'UserDefined'}  # MAKE THIS MORE UPDATABLE W/OUT HAVING TO MANUALLY CHNAGE

''' CLASS FOR ANOTHER LATTICE TYPE
class BCC:
    def __init__(self,alloy='CuNi'):
        < TO DO >
'''

class FCC:
    def __init__(self,alloy='CuNi',customLatticeConst=1):
        if alloy == 'custom':
            self.latticeParameter = customLatticeConst
        else:
            self.latticeParameter = AlloyLatticeConsts[alloy]   # should check if alloy is in alloylattice const list first, before setting
        self.basis = np.array([[1.0, 0.0, 0.0],
                               [0.0, 1.0, 0.0],
                               [0.0, 0.0, 1.0]])*self.latticeParameter
        self.baseAtoms = np.array([[0.0, 0.0, 0.0],
                                   [0.5, 0.5, 0.0],
                                   [0.5, 0.0, 0.5],
                                   [0.0, 0.5, 0.5]])*self.latticeParameter

class AtomDataFileGenerator:
    def __init__(self, filename='atom2', latticeType='FCC', alloy='CuNi', systemSize=1, atomTypes=2, alloyCompPercent = 0, customLatticeConst=None):
        # FILE SETUP
        self.filename = 'data.'+filename
        self.systemSize = systemSize        # SYSTEMSIZE CREATES (basis*systemSize)^3 box of atoms
        self.atomTypes = atomTypes
        self.alloy = alloy
        self.fileCreated = False

        # BOX INFO
        self.latticeType = latticeType          # CAN MAKE THIS INTO A INPUT PARAMETER, WHITH DIFFERENT CLASSSES FOR EACH LATTICETYPE
        if self.latticeType == 'FCC':           # THIS MAKES MORE SENSE IF WE HAVE MULTIPLE LATTICE TYPES
            if customLatticeConst is None:         # Specify a custom alloy with any lattice parameter
                self.lattice = FCC(alloy)
            else:
                self.lattice = FCC('custom',customLatticeConst)
        else:                                   # conditional for more lattice types options
            self.lattice = FCC(alloy)
        
        #PERCENT COMPOSITION FOR BINARY ATOMDATA PRODUCTION
        self.compPercent = alloyCompPercent         # compPercent affects number of 2 atoms created, up to user which elem is 1 or 2
        self.compCounter = 0
        
    
    # METHODS FOR UPDATING FILE AND ATOM VARIABLES
    def getActualCompPercent(self):
        if self.fileCreated:
            return float(self.compCounter/self.getNumAtoms())
        else:
            # edit code to raise an error instead of print
            print('*********** ERROR: DATAFILE NOT CREATED YET, CALL METHOD createDataFile() **********')

    def getNumAtoms(self):
        return 4*self.systemSize**3
    
    def setFilename(self,newFilename):
        self.filename = 'data.'+newFilename
    
    def setSystemSize(self,newSize):
        self.systemSize = newSize

    def setCompPercent(self,newPercent):
        self.compPercent = newPercent

    #def setLatticeType

    #def setAlloyType

    # RETURN LIST OF ATOMS POSITION AT LATTICE (latticeType) POINTS
    def generatePositionList(self):
        basis = self.lattice.basis
        
        positions = []
        for i in range(self.systemSize):
            for j in range(self.systemSize):
                for k in range(self.systemSize):
                    basePosition = np.array([i,j,k])
                    cartPosition = np.inner(basis.T, basePosition) #basically resizes basis vectors to point to poistion on 3D lattice grid
                    for atom in self.lattice.baseAtoms:
                        positions.append(cartPosition + atom)
        return positions
    
    # RETURN ATOM TYPE BASED ON DESIRED COMPOSITION, 1 = Ni, 2 = Cu
    def generateAtomType(self):
        compRand = np.random.random(1)[0]
        if compRand < self.compPercent:
            self.compCounter+=1
            return(2)
        else:
            return(1)
        
        ''' Original Implementation
        compMax = 4*(self.systemSize**3)*self.compPercent
        compBias = .70       # FIX THIS, NO HARD CODED NUMBERS
        
        compRand = np.random.random(1)[0]
        if compRand > compBias and self.compCounter <= compMax:
            self.compCounter+=1
            return(2)
        else:
            return(1)
        '''

    # WRITE LAMMPS DATAFILE
    def createDataFile(self):
        positions = self.generatePositionList()
        
        with open(self.filename,'w') as fdata:
            fdata.write(str(self.alloy)+' atom datafile for lammps scripts \n\n') # comment on in file
            
            #----------- Header --------------#
            # Specify number of atoms and atom types
            fdata.write('{} atoms\n'.format(len(positions)))
            fdata.write('{} atom types\n'.format(self.atomTypes))
            # -------- Box dimensions -------------#
            fdata.write('{} {} xlo xhi\n'.format(0.0, self.systemSize*self.lattice.latticeParameter))
            fdata.write('{} {} ylo yhi\n'.format(0.0, self.systemSize*self.lattice.latticeParameter))
            fdata.write('{} {} zlo zhi\n'.format(0.0, self.systemSize*self.lattice.latticeParameter))
            fdata.write('0.0 0.0 0.0 xy xz yz\n') # allows simulation box to tilt
            fdata.write('\n')
            # -------- Atom Positions -----------#
            fdata.write('Atoms\n\n')
 
            for i,pos in enumerate(positions):
                fdata.write('{} {} {} {} {}\n'.format(i+1,str(self.generateAtomType()),*pos))

            self.fileCreated = True
                 

























# ORIGINAL CODE
'''
# Lattice parameter for aluminum
#a = AtomData()
lattice_parameter = 4.046     # without object oriented class (AtomData)
#lattice_parameter = a.latConst

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
                       
#----simple cubic base atoms--------
#base_atoms = np.array([[0.0, 0.0, 0.0],
#                       [1, 1, 0.0],
#                       [1, 0.0, 1],
#                       [0.0, 1, 1]])*lattice_parameter
#-----------------------------------

# Size of the system cell in lattice units
#    assuming an cubic cell starting at the origin
system_size = 2
#system_size = a.sysSize


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
with open('atom.data','w') as fdata:
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

'''
