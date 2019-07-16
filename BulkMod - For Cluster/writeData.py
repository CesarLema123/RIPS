#!/usr/bin/python3.6
from numpy.random import random,normal

# random([size]) -> numpy array 1 x size with elements in [0.0,1.0)
# normal( mu , sigma , size ) ->    np array 1 x size of elements from a gaussian distrobution
#                                   with mean mu and standard deviation sigma



FILE = "data.CuNi"
HEADER = "Nickle Copper Simulation"

STYLE = "atomic" 
LATTICETYPE = "fcc"
INITTEMP = 0 # kelvin (set via random inital velocities

NUMX = 10    # number of atoms in the x direction
NUMY = 10 
NUMZ = 10

AX,AY,AZ = 4.6,4.6,4.6  # The lattice constant in the 3 directions
CONCENTRATIONS = lambda a: 1 if a < -1.0 else 2 # A function which takes in a random value in [0,1) and outputs
                                                # an atom number
XLO, XHI = -0.02, (NUMX-1)*AX + 0.02
YLO, YHI = -0.02, (NUMY-1)*AY + 0.02
ZLO, ZHI = -0.02, (NUMZ-1)*AZ + 0.02




def getNumAtoms(latticeType = "fcc",numX,numY,numZ):
    if latticeType = "fcc":
        numAtoms = NUMX*NUMY*NUMZ + (NUMX-1)*(NUMY-1)*(NUMZ) + (NUMX-1)*(NUMY)*(NUMZ-1) + (NUMX)*(NUMY-1)*(NUMZ-1)
    elif latticeType = "bcc":
        numAtoms = 
    else:
        return
    return numAtoms





NUM_ATOMS = getNumAtoms(LATTICETYPE,NUMX,NUMY,NUMZ)
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




def writeatom(wfile,style = "atomic",num = 0,mol_tag = 0,atom_tag = 0,q = 0,x=0.0,y=0.0,z=0.0,nx=0.0,ny=0.0,nz=0.0, noise = 0.01):
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
    x,y,z = round(x - noise + 2*random(1)[0]*noise,4), round(y - noise + 2*random(1)[0]*noise,4), round(z - noise + 2*random(1)[0]*noise,4)
    if style == "atomic":
        s = T + str(num) + T + str(atom_tag) + T + str(x) + T + str(y) + T + str(z) + N
    elif style == " full":
        s = T + str(num) + T + str(mol_tag) + T + str(atom_tag) + T + str(q) + T + str(x) + T + str(y) + T + str(z) + T + str(nx) + T + str(ny) + T + str(nz) + N
    wfile.write(s)
    return


def writevelocity(wfile,style = "atomic",num = 0,vx = 0.0,vy = 0.0, vz = 0.0,noise = 0.01):
    vx += normal(0,noise,1)[0]
    vy += normal(0,noise,1)[0]
    vz += normal(0,noise,1)[0]
    if not style in ["electron","ellipsoid","sphere","hybrid"]:
        wfile.write(T + str(num) + T + str(vx) + T + str(vy) + T + str(vz) + N )
    else:
        pass
    return


def linebreak(wfile):
    wfile.write("\n")
    return


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

linebreak(w)





#Writing the atoms sections

w.write("Atoms" + N )

linebreak(w)

n = 1 #atom id will range from 1 to NUM_ATOMS and will also be used to for molecule tag
charge = 0


# Writing the atoms on the verticies of the fcc lattice
for x in range(NUMX):
    for y in range(NUMY):
        for z in range(NUMZ):
            writeatom(w,style = STYLE,num = n,atom_tag = CONCENTRATIONS(random()), x = AX*x, y = AY*y, z = AZ*z)
            n+=1



# Writing the atoms on the 3 faces of the fcc lattice

for x in range(NUMX-1):
    for y in range(NUMY-1):
        for z in range(NUMZ):
            writeatom(w,style = STYLE,num = n,atom_tag = CONCENTRATIONS(random()), x = AX*x + AX/2, y = AY*y + AY/2, z = AZ*z)
            n+=1


for x in range(NUMX-1):
    for y in range(NUMY):
        for z in range(NUMZ-1):
            writeatom(w,style = STYLE,num = n,atom_tag = CONCENTRATIONS(random()), x = AX*x + AX/2, y = AY*y, z = AZ*z + AZ/2)
            n+=1


for x in range(NUMX):
    for y in range (NUMY-1):
        for z in range(NUMZ-1):
            writeatom(w,style = STYLE,num = n,atom_tag = CONCENTRATIONS(random()), x = AX*x, y = AY*y + AY/2, z = AZ*z + AZ/2)
            n+=1


# Writing atom velocities

linebreak(w)
w.write("Velocities\n")
linebreak(w)


# keeping track of the first N-1 velocities to make sure there is no net velocity
svx,svy,svz = 0.0,0.0,0.0 


for i in range(1,NUM_ATOMS):
    vx,vy,vz = normal(0,SIGMA_VEL,3)
    writevelocity(w,style = STYLE,num = i,vx = vx,vy = vy,vz = vz,noise = 0.0)
    svx += vx
    svy += vy
    svz += vz

writevelocity(w,style = STYLE, num = NUM_ATOMS,vx = -svx,vy = -svy,vz = -svz,noise = 0.0)

del svx,svy,svz,vx,vy,vz
linebreak(w)

w.close()




            
print("All Done!")
