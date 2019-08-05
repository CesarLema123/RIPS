import numpy as np
import dataFileGenerator as DFG

'''
    Class:
        AtomDataFileGenerator [Generate data file for atom positions of alloy with varaibel lattice type and composition]
    
    constructor:
        AtomDataFileGenerator(filename='atom2.data', latticeType='FCC', alloy='CuNi', systemSize=1, atomTypes=2, alloyCompPercent = 0)
    
    instance vars:
        filename
        systemSize
        atomTypes
        alloy
        
        latticeType
        lattice (object)
        
        compPercent
        compCounter
        
    methods:
        getActualCompPercent(self) [Actual percent of type 2 atoms created]****
        getNumAtoms(self)  ****
        setFilename(newFilename) [Change filename where data is output]  ****
        setSystemSize(newSize) [Change side length of atom box size]  ****
        setCompPercent(newPercent) [Change percent of type 2 atoms in data]  ****
        generatePositionList() [Make list of atoms position at lattice points]
        generateAtomType() [Return value for atom type depending on compPercent]
        createDataFile() [create a new data file locally with atom postion data]  ****
        
'''


generator = DFG.AtomDataFileGenerator('testDataFile',systemSize=10,alloyCompPercent=.4)
generator.createDataFile()
print(generator.getNumAtoms())
print(generator.getActualCompPercent())

