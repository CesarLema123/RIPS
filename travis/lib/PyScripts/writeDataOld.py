#!/usr/bin/python3.6

# This script runs both with python2 and python3

#from numpy.random import random,normal
from random import random,gauss
import sys



# random([size]) -> numpy array 1 x size with elements in [0.0,1.0)
# normal( mu , sigma , size ) ->    np array 1 x size of elements from a gaussian distrobution
#                                   with mean mu and standard deviation sigma

def getNumAtoms(latticeType = "fcc",numX = 10 ,numY = 10,numZ = 10):
    """
    Specify a lattice type and a number of atoms in the three directions.
    The function outputs the number of atoms that will be created
    """
    if latticeType == "fcc":
        numAtoms = numX*numY*numZ + (numX-1)*(numY-1)*(numZ) + (numX-1)*(numY)*(numZ-1) + (numX)*(numY-1)*(numZ-1)
    elif latticeType == "bcc":
        numAtoms = numX*numY*numZ + (numX - 1)*(numY - 1)*(numZ - 1)
    else:
        return
    return numAtoms

def writeatom(wfile,style = "atomic",num = 0,mol_tag = 0,atom_tag = 0,q = 0,x=0.0,y=0.0,z=0.0,nx=0.0,ny=0.0,nz=0.0, noise = 0.0):
    '''wfile is a "_io.TextIOWrapper" for open(FILE),
    style corresponds to a lammps atom_style which only write the entries which the given atom_style is expecting. 
    If you spcify a value which is not used by the given style, it will simply be ignored.
    n is the number of the atom
    mol_tag is the molecule tag
    atom_tag is the number of the atom type
    q is the charge
    x,y,z are the spacial coordinates
    nx,ny,nz are optional
    noise adds a random factor of magnitude noise to each of the positions'''
    x,y,z = round(x - noise + 2*random()*noise,4), round(y - noise + 2*random()*noise,4), round(z - noise + 2*random()*noise,4)
    if style == "atomic":
        s = T + str(num) + T + str(atom_tag) + T + str(x) + T + str(y) + T + str(z) + N
    elif style == " full":
        s = T + str(num) + T + str(mol_tag) + T + str(atom_tag) + T + str(q) + T + str(x) + T + str(y) + T + str(z) + T + str(nx) + T + str(ny) + T + str(nz) + N
    wfile.write(s)
    return


def writevelocity(wfile,style = "atomic",num = 0,vx = 0.0,vy = 0.0, vz = 0.0,noise = 0.01):
    vx += gauss(0,noise) #normal(0,noise,1)[0]
    vy += gauss(0,noise) #normal(0,noise,1)[0]
    vz += gauss(0,noise) #normal(0,noise,1)[0]
    if not style in ["electron","ellipsoid","sphere","hybrid"]:
        wfile.write(T + str(num) + T + str(vx) + T + str(vy) + T + str(vz) + N )
    else:
        pass
    return


def linebreak(wfile):
    wfile.write("\n")
    return

def writeGroup(writer,origin = (0,0,0), latticeType = "fcc",startIdNum = 1,style = "atomic",concFunc = lambda p: 1, numX = 10, numY = 10, numZ = 10,ax = 3.4,ay = 3.4,az = 3.4):
    S,T,N = " ","\t","\n"
    linebreak(writer)
    writer.write("Atoms" + N )
    linebreak(writer)

    n = startIdNum #atom id will range from 1 to NUM_ATOMS and will also be used to for molecule tag
    if latticeType == "fcc":
        # Writing the atoms on the verticies of the fcc lattice
        for x in range(numX):
            for y in range(numY):
                for z in range(numZ):
                    writeatom(writer,style = style,num = n,atom_tag = concFunc(random()), x = ax*x, y = ay*y, z = az*z)
                    n+=1



        # Writing the atoms on the 3 faces of the fcc lattice

        for x in range(numX-1):
            for y in range(numY-1):
                for z in range(numZ):
                    writeatom(writer,style = style,num = n,atom_tag = concFunc(random()), x = ax*x + ax/2, y = ay*y + ay/2, z = az*z)
                    n+=1


        for x in range(numX-1):
            for y in range(numY):
                for z in range(numZ-1):
                    writeatom(writer,style = style,num = n,atom_tag = concFunc(random()), x = ax*x + ax/2, y = ay*y, z = az*z + az/2)
                    n+=1


        for x in range(numX):
            for y in range (numY-1):
                for z in range(numZ-1):
                    writeatom(writer,style = style,num = n,atom_tag = concFunc(random()), x = ax*x, y = ay*y + ay/2, z = az*z + az/2)
                    n+=1

    elif latticeType == "bcc":
        # Writing the atoms on the verticies of the fcc lattice
        for x in range(numX):
            for y in range(numY):
                for z in range(numZ):
                    writeatom(writer,style = style,num = n,atom_tag = concFunc(random()), x = ax*x, y = ay*y, z = az*z)
                    n+=1

        for x in range(numX - 1):
            for y in range(numY - 1):
                for z in range(numZ - 1):
                    writeatom(writer,style = style,num = n,atom_tag = concFunc(random()),x = ax*x + ax/2, y = ay*y + ay/2,z =  az*z + az/2)
                    n+=1

    else:
        print("Unknown lattice type.")
        return 1
    return 0










# ------------ COMMAND LINE INPUTS ----------------







if len(sys.argv) > 1:
    _numSide,_conc,_dataFile = list(sys.argv[a + 1] for a in range(3))
else:
    _numSide,_conc,_dataFile = 4,5,"data.CuNi"
_numSide = int(_numSide)
_conc = float(_conc)/10










# --------------- SPECIFY PARAMETERS FOR WRITE FILE ---------------



FILE = _dataFile
HEADER = "Nickle Copper Simulation"

STYLE = "atomic" 
LATTICE_TYPE = "fcc"
INITTEMP = 0 # kelvin (set via random inital velocities

NUMX = _numSide    # number of atoms in the x direction
NUMY = _numSide
NUMZ = _numSide



CuNi_LATTICE_CONSTANT = 3.63


AX,AY,AZ = [CuNi_LATTICE_CONSTANT]*3  # The lattice constant in the 3 directions
CONCENTRATIONS = lambda a: 1 if a < _conc else 2 # A function which takes in a random value in [0,1) and outputs
                                                # an atom number
XLO, XHI = 0.0, (NUMX-1/2)*AX 
YLO, YHI = 0.0, (NUMY-1/2)*AY
ZLO, ZHI = 0.0, (NUMZ-1/2)*AZ







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
    vx,vy,vz = 0.0,0.0,0.0 #normal(0,SIGMA_VEL,3)
    writevelocity(w,style = STYLE,num = i,vx = vx,vy = vy,vz = vz,noise = 0.0)
    svx += vx
    svy += vy
    svz += vz

writevelocity(w,style = STYLE, num = NUM_ATOMS,vx = -svx,vy = -svy,vz = -svz,noise = 0.0)

del svx,svy,svz,vx,vy,vz
linebreak(w)

w.close()


