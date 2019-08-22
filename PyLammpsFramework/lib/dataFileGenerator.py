import numpy as np

"""
    This file contains classes for generating Atom positions data files to be input in a LAMMPS read_data command.
    
    This file can be imported as a module inorder to initialize instances of the AtomDataFileGenerator class.
"""

AlloyLatticeConsts = {'CuNi': 3.63,'custom': 'UserDefined'}  # MAKE THIS MORE UPDATABLE W/OUT HAVING TO MANUALLY CHNAGE


class FCC:
    """
        
    """
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
    def getLatticeType(self):
        return 'FCC'

""" CLASS FOR ANOTHER LATTICE TYPE
    class BCC:
        def __init__(self,alloy='CuNi'):
            <TODO>
"""


# better code would make a geometry base class w/ getBoxType, resize, and getXSize methods for CubicBox,ParallelogramBox
class CubicBox:
    """
        
    """
    
    def __init__(self,systemSize=1):
        self.systemSize = systemSize

    def getBoxType(self):
        return 'cubic'
    
    def resize(self,systemSize=None):
        if systemSize != None:
            self.systemSize = systemSize

class ParallelogramBox:
    """
        
    """
    
    def __init__(self, xSize = 1, ySize=1, zSize=1):
        self.xSize = xSize
        self.ySize = ySize
        self.zSize = zSize
    
    def getBoxType(self):
        return 'parallelogram'
    
    def resize(self, xSize=None, ySize=None, zSize=None):
        if xSize != None:
            self.xSize = xSize
        if ySize != None:
            self.ySize = ySize
        if xSize != None:
            self.zSize = zSize



class AtomDataFileGenerator:
    """ A class for generating simulation datafiles for atom related parameters and positions to be read by the LAMMPS read_data command
        
    This class is meant to be importated and used as a object that generates LAMMPS simulation datafiles respective to the values of an instances attributes. Instance methods can be called to update the attribute values and generate new datafiles.
    currently the class was implemented to work best for binary alloys.
    
    Attributes:
        filename = A string representing the desired filename (without file extension) for the data file created.
        latticeType = a string indicating the desired lattice type for the atoms in the data file created.
        alloy = a string indicating the alloy in the data file created.
        atomTypes = an int representing the number of elements in the alloy used in data file created.
        alloyCompPercent = a float from 0 to 1 indicating the desired precentage of type 2 atoms in the data file created.
        geometry = a string indicating the shape of the region the atom positions fill in the data file created.
        systemSize = an int indicating the multiplication factor of the lattice constant along one side of a cubic region of atoms.
        customLatticeConst = a float of lattice constant for a custom style alloy
        xSize = an int indicating the multiplication factor of the lattice constant along the unit x vector of a paralleliped region the atom positions are created in for the data file created.
        ySize = an int indicating the multiplication factor of the lattice constant along the unit y vector of a paralleliped region the atom positions are created in for the data file created.
        zSize = an int indicating the multiplication factor of the lattice constant along the unit z vector of a paralleliped region the atom positions are created in for the data file created.
    
    Methods:
        getActualCompPercent(): returns a calculated percentage of type 2 atoms in the data file created.
        getNumAtoms(): return the number of atoms in the data file created.
        setFilename(newFilename): change the desired filename for the data file created
        setSystemSize(newSize=1, newX=1, newY=1 ,newZ=1 ): change the lengths of the respective regions the atoms positions created should fit in.
        setCompPercent(newPercent): change the desired precentage of type 2 atoms in the data file created.
        setGeometry(geometry,systemSize=1,xSize=1,ySize=1,zSize=1): change the shape of the region the atom positions are creatd in the data file.
        generatePositionList(): implementation method for generation atom position with respects to the the value of an instances attributes.
        generateAtomType(): implementation for generating the type of an atom to satisfy the alloyCompPercent attribute.
        createDataFile(): method to create a LAMMPS data file.
    """
    
    def __init__(self, filename='atom', latticeType='FCC', alloy='CuNi', atomTypes=2 ,alloyCompPercent = 0, geometry='cubic', systemSize=1, customLatticeConst=None, xSize=1, ySize=1, zSize=1):
        # FILE SETUP
        self.filename = 'data.'+filename
        self.atomTypes = atomTypes
        self.alloy = alloy
        self.fileCreated = False
        
        # BOX INITIALIZATION
        if geometry == 'cubic':           # THIS MAKES MORE SENSE IF WE HAVE MULTIPLE systemBox TYPES
            self.systemBox = CubicBox(systemSize)
        else:
            self.systemBox = ParallelogramBox(xSize,ySize,zSize)
        
        # LATTICE INITIALIZATION
        if latticeType == 'FCC':           # THIS MAKES MORE SENSE IF WE HAVE MULTIPLE LATTICE TYPES
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
        if self.lattice.getLatticeType() == 'FCC':
            if self.systemBox.getBoxType() == 'cubic':
                return 4*self.systemBox.systemSize**3
            if self.systemBox.getBoxType() == 'parallelogram':
                return 4*self.systemBox.xSize*self.systemBox.ySize*self.systemBox.zSize
    
    def setFilename(self,newFilename):
        self.fileCreated = False
        self.filename = 'data.'+newFilename
    
    def setSystemSize(self,newSize=1, newX=1, newY=1 ,newZ=1 ):
        self.fileCreated = False
        self.compCounter = 0
        if self.systemBox.getBoxType == 'cubic':
            self.systemBox.resize(newSize)
        if self.systemBox.getBoxType == 'parallelogram':
            self.systemBox.resize(newX,newY,newZ)

    def setCompPercent(self,newPercent):
        self.fileCreated = False
        self.compCounter = 0
        self.compPercent = newPercent

    def setGeometry(self,geometry,systemSize=1,xSize=1,ySize=1,zSize=1):
        self.fileCreated = False
        self.compCounter = 0
        if geometry == 'cubic':
            self.systemBox = CubicBox(systemSize)
        if geometry == 'parallelogram':
            self.systemBox = ParallelogramBox(xSize,ySize,zSize)

    #def setLatticeType

    #def setAlloyType

    # RETURN LIST OF ATOMS POSITION AT LATTICE (latticeType) POINTS IN SYSTEMBOX
    def generatePositionList(self):
        basis = self.lattice.basis
        if self.systemBox.getBoxType() == 'cubic':
            xSize = self.systemBox.systemSize
            ySize = self.systemBox.systemSize
            zSize = self.systemBox.systemSize
        elif self.systemBox.getBoxType() == 'parallelogram':
            xSize = self.systemBox.xSize
            ySize = self.systemBox.ySize
            zSize = self.systemBox.zSize

        positions = []
        for i in range(xSize):
            for j in range(ySize):
                for k in range(zSize):
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

    # WRITE LAMMPS DATAFILE
    def createDataFile(self):
     
        positions = self.generatePositionList()
        
        if self.systemBox.getBoxType() == 'cubic':
            xSize = self.systemBox.systemSize
            ySize = self.systemBox.systemSize
            zSize = self.systemBox.systemSize
        elif self.systemBox.getBoxType() == 'parallelogram':
            xSize = self.systemBox.xSize
            ySize = self.systemBox.ySize
            zSize = self.systemBox.zSize
        
        with open(self.filename,'w') as fdata:
            fdata.write(str(self.alloy)+' atom datafile for lammps scripts \n\n') # comment on in file
            
            #----------- Header --------------#
            # Specify number of atoms and atom types
            fdata.write('{} atoms\n'.format(len(positions)))
            fdata.write('{} atom types\n'.format(self.atomTypes))
            # -------- Box dimensions -------------#
            fdata.write('{} {} xlo xhi\n'.format(0.0, xSize*self.lattice.latticeParameter))
            fdata.write('{} {} ylo yhi\n'.format(0.0, ySize*self.lattice.latticeParameter))
            fdata.write('{} {} zlo zhi\n'.format(0.0, zSize*self.lattice.latticeParameter))
            fdata.write('0.0 0.0 0.0 xy xz yz\n') # allows simulation box to tilt
            fdata.write('\n')
            # -------- Atom Positions -----------#
            fdata.write('Atoms\n\n')
 
            for i,pos in enumerate(positions):
                fdata.write('{} {} {} {} {}\n'.format(i+1,str(self.generateAtomType()),*pos))

            self.fileCreated = True

