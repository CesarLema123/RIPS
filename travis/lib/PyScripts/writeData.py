#!/usr/bin/python3.6

# This script runs both with python2 and python3

#from numpy.random import random,normal
import sys
from random import random,gauss
#from math import sqrt


# random([size]) -> numpy array 1 x size with elements in [0.0,1.0)
# normal( mu , sigma , size ) ->    np array 1 x size of elements from a gaussian distrobution
#                                   with mean mu and standard deviation sigma

def getNumAtoms(latticeType = "fcc",numX = 10 ,numY = 10,numZ = 10):
    """
    Specify a lattice type and a number of atoms in the three directions.
    The function outputs the number of atoms that will be created
    """
    if latticeType == "fcc":
        numAtoms = 4*numX*numY*numZ 
    elif latticeType == "bcc":
        numAtoms = 2*numX*numY*numZ 
    else:
        return
    return numAtoms

def writeAtom(wfile,style = "atomic",num = 0,mol_tag = 0,atom_tag = 0,q = 0,x=0.0,y=0.0,z=0.0,nx=0.0,ny=0.0,nz=0.0):
    S,T,N = " ","\t","\n"
    x,y,z = round(x,4),round(y,4),round(z,4)
    '''wfile is a "_io.TextIOWrapper" for open(FILE),
    style corresponds to a lammps atom_style which only write the entries which the given atom_style is expecting. 
    If you spcify a value which is not used by the given style, it will simply be ignored.
    n is the number of the atom
    mol_tag is the molecule tag
    atom_tag is the number of the atom type
    q is the charge
    x,y,z are the spacial coordinates
    nx,ny,nz are optional
    '''  
    if style == "atomic":
        s = T + str(num) + T + str(atom_tag) + T + str(x) + T + str(y) + T + str(z) + N
    elif style == " full":
        s = T + str(num) + T + str(mol_tag) + T + str(atom_tag) + T + str(q) + T + str(x) + T + str(y) + T + str(z) + T + str(nx) + T + str(ny) + T + str(nz) + N
    wfile.write(s)
    return


def writevelocity(wfile,style = "atomic",num = 0,vx = 0.0,vy = 0.0, vz = 0.0):
    if not style in ["electron","ellipsoid","sphere","hybrid"]:
        wfile.write(T + str(num) + T + str(vx) + T + str(vy) + T + str(vz) + N )
    else:
        pass
    return


def linebreak(wfile):
    wfile.write("\n")
    return


def writeUnitCell(writer,origin = (0,0,0),latticeType = "fcc",startIdNum = 1,style = "atomic",concFunc = lambda p: 1, ax = 3.52, ay = 3.52, az = 3.52):
    x,y,z = origin
    if latticeType == "fcc":
        writeAtom(writer,style = style,num = startIdNum,atom_tag = concFunc(random()),x = x, y = y, z = z)
        writeAtom(writer,style = style,num = startIdNum+1,atom_tag = concFunc(random()),x = x+ ax/2, y = y+ay/2, z = z)
        writeAtom(writer,style = style,num = startIdNum+2,atom_tag = concFunc(random()),x = x, y = y+ay/2, z = z+az/2)
        writeAtom(writer,style = style,num = startIdNum+3,atom_tag = concFunc(random()),x = x+ax/2, y = y, z = z+az/2)
    elif latticeType == "bcc":
        writeAtom(writer,style = style,num = startIdNum,atom_tag = concFunc(random()),x = x, y = y, z = z)
        writeAtom(writer,style = style,num = startIdNum+1,atom_tag = concFunc(random()),x = x + ax/sqrt(2), y = y + ay/sqrt(2), z = z + az/sqrt(2))
    return 


def writeGroup(writer,origin = (0,0,0), latticeType = "fcc",startIdNum = 1,style = "atomic",concFunc = lambda p: 1, numX = 10, numY = 10, numZ = 10,ax = 3.4,ay = 3.4,az = 3.4):
    S,T,N = " ","\t","\n"
    linebreak(writer)
    writer.write("Atoms" + N )
    linebreak(writer)
    x0,y0,z0 = origin
    n = startIdNum #atom id will range from 1 to NUM_ATOMS and will also be used to for molecule tag
    # Writing the atoms on the verticies of the fcc lattice
    for x in range(numX):
        for y in range(numY):
            for z in range(numZ):
                writeUnitCell(writer,origin = (x0 + x*ax,y0 + y*ay,z0 + z*az) ,latticeType = latticeType, startIdNum = n,style = style,concFunc = concFunc, ax = ax, ay = ay, az = az)
                if latticeType == "fcc":
                    n+=4
                elif latticeType == "bcc":
                    n+=2
    return









# ------------ COMMAND LINE INPUTS ----------------







if len(sys.argv) > 1:
    _numSide,_conc= list(sys.argv[a + 1] for a in range(2))
    _dataFile = "data.CuNi"
else:
    _numSide,_conc,_dataFile = 6,3,"data.CuNi" 
_numSide = int(_numSide)
_conc = float(_conc)/10 # This is the concentration of Ni










# --------------- SPECIFY PARAMETERS FOR WRITE FILE ---------------



FILE = _dataFile
HEADER = "Nickle Copper Simulation"

STYLE = "atomic" 
LATTICE_TYPE = "fcc"
INITTEMP = 0 # kelvin (set via random inital velocities

NUMX = _numSide    # number of atoms in the x direction
NUMY = _numSide
NUMZ = _numSide



CuNi_LATTICE_CONSTANT = 3.6


AX,AY,AZ = [CuNi_LATTICE_CONSTANT]*3  # The lattice constant in the 3 directions
CONCENTRATIONS = lambda a: 1 if a < _conc else 2 # A function which takes in a random value in [0,1) and outputs
                                                # an atom number
XLO, XHI = 0.0, (NUMX)*AX 
YLO, YHI = 0.0, (NUMY)*AY
ZLO, ZHI = 0.0, (NUMZ)*AZ







NUM_ATOMS = getNumAtoms(LATTICE_TYPE,NUMX,NUMY,NUMZ)
NUM_BONDS = 0 # Not used
NUM_ANGLES = 0 # Not used
NUM_DIHEDRALS = 0 # Not used
NUM_IMPROPERS = 0 # Not used


NUM_ATOM_TYPES = 2 # Specify the number of atoms types
NUM_BOND_TYPES = 0 # Not used
NUM_ANGLE_TYPES = 0 # Not used
NUM_DIHEDRAL_TYPES = 0 # Not used
NUM_IMPROPER_TYPES = 0 # Not used






KB = 8.617333262e-5
SIGMA_VEL =  (30 * INITTEMP * KB)**(2/3)


BDRY_LIST = ((XLO,XHI),(YLO,YHI),(ZLO,ZHI))
BDRY_STR = (("xlo","xhi"),("ylo","yhi"),("zlo","zhi"))
S = " "
T = "\t"
N = "\n"





# This is the write file
w = open(FILE,mode = "w")

# Writing the first line of the file
w.write(HEADER + N)

linebreak(w)

# Writing the number of atoms
w.write(str(NUM_ATOMS) + S + T + "atoms" + N )
w.write(str(NUM_BONDS) + S + T + "bonds" + N )
w.write(str(NUM_ANGLES) + S + T + "angles" + N )
w.write(str(NUM_DIHEDRALS) + S + T + "dihedrals" + N )
w.write(str(NUM_IMPROPERS) + S + T + "impropers" + N )

linebreak(w)

# Writing the number of atom types
w.write(str(NUM_ATOM_TYPES) + T + "atom" + S + "types" + N )
w.write(str(NUM_BOND_TYPES) + T + "bond" + S + "types" + N )
w.write(str(NUM_ANGLE_TYPES) + T + "angle" + S + "types" + N )
w.write(str(NUM_DIHEDRAL_TYPES)  + T + "dihedral" + S + "types" + N )
w.write(str(NUM_IMPROPER_TYPES)  + T + "improper" + S + "types" + N )

linebreak(w)




#writing x,y,z low and high
for i in range(len(BDRY_LIST)):
    if BDRY_LIST[i][0] < 0:
        w.write(str(BDRY_LIST[i][0]) + T + str(BDRY_LIST[i][1]) + T + BDRY_STR[i][0] + S + BDRY_STR[i][1] + N) 
    else:
        w.write(str(BDRY_LIST[i][0]) + T + str(BDRY_LIST[i][1]) +  T + BDRY_STR[i][0] + S + BDRY_STR[i][1] + N) 



# def writeGroup(writer,origin = (0,0,0), latticeType = "fcc",startIdNum = 1,style = "atomic",concFunc = lambda p: 0, numX = 10, numY = 10, numZ = 10,ax = 3.4,ay = 3.4,az = 3.4)
writeGroup(w,numX = NUMX, numY = NUMZ, numZ = NUMZ, ax = AX, ay = AY, az = AZ,style = STYLE,latticeType = LATTICE_TYPE, concFunc = CONCENTRATIONS) 


# Writing atom velocities
linebreak(w)

w.write("Velocities\n")
linebreak(w)


    # keeping track of the first N-1 velocities to make sure there is no net velocity
svx,svy,svz = 0.0,0.0,0.0 


for i in range(1,NUM_ATOMS):
    vx,vy,vz = round(gauss(0.0,SIGMA_VEL),4),round(gauss(0.0,SIGMA_VEL),4),round(gauss(0.0,SIGMA_VEL),4)
    writevelocity(w,style = STYLE,num = i,vx = vx,vy = vy,vz = vz)
    svx += vx
    svy += vy
    svz += vz

writevelocity(w,style = STYLE, num = NUM_ATOMS,vx = -svx,vy = -svy,vz = -svz)

del svx,svy,svz,vx,vy,vz
linebreak(w)

w.close()


