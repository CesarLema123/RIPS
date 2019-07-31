#!/usr/bin/python3.6

# This script runs both with python2 and python3

#from numpy.random import random,normal
import sys
from random import random,gauss,randint
#from math import sqrt

S,T,N = " ","\t","\n"

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


def writeVelocity(wfile,style = "atomic",num = 0,vx = 0.0,vy = 0.0, vz = 0.0):
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
        writeAtom(writer,style,startIdNum,0,concFunc(random()),0,x,y,z)
        writeAtom(writer,style,startIdNum+1,0,concFunc(random()),0,x+ ax/2,y+ay/2,z)
        writeAtom(writer,style,startIdNum+2,0,concFunc(random()),0,x,y+ay/2,z+az/2)
        writeAtom(writer,style,startIdNum+3,0,concFunc(random()),0,x+ax/2,y,z+az/2)
    elif latticeType == "bcc":
        writeAtom(writer,style,startIdNum,0,concFunc(random()),0,x,y,z)
        writeAtom(writer,style,startIdNum+1,0,concFunc(random()),0,x + ax/2,y + ay/2,z + az/2)
    return 


def writeGroup(writer,origin = (0,0,0), latticeType = "fcc",startIdNum = 1,style = "atomic",concFunc = lambda p: 1, numX = 10, numY = 10, numZ = 10,ax = 3.4,ay = 3.4,az = 3.4):
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

# Writing atom velocities
def writeVelocities(writer,nAtoms,temp,style):
    linebreak(writer)
    writer.write("Velocities\n")
    linebreak(writer)


    # keeping track of the first N-1 velocities to make sure there is no net velocity
    svx,svy,svz = 0.0,0.0,0.0 

    kB = 8.617333262e-5
    sigmaVel =  (30 * temp * kB)**(2/3)

    for i in range(1,nAtoms):
        vx,vy,vz = round(gauss(0.0,sigmaVel),4),round(gauss(0.0,sigmaVel),4),round(gauss(0.0,sigmaVel),4)
        writeVelocity(writer,style = style,num = i,vx = vx,vy = vy,vz =vz)
        svx += vx
        svy += vy
        svz += vz
    writeVelocity(writer,style = style, num = nAtoms,vx = round(-svx,4),vy = round(-svy,4),vz = round(-svz,4))
    del svx,svy,svz,vx,vy,vz
    linebreak(writer)
    return





def writeHeader(writer,header,totNAtoms,nBonds = 0,nAngles = 0,nDihedrals = 0,nImpropers = 0,nAtomTypes = 1,nBondTypes = 0,nAngleTypes = 0,nDihedralTypes = 0,nImproperTypes = 0):
    # Writing the first line of the file
    writer.write(header + N)
    
    linebreak(writer)

    # Writing the number of atoms
    writer.write(str(totNAtoms) + S + T + "atoms" + N )
    writer.write(str(nBonds) + S + T + "bonds" + N )
    writer.write(str(nAngles) + S + T + "angles" + N )
    writer.write(str(nDihedrals) + S + T + "dihedrals" + N )
    writer.write(str(nImpropers) + S + T + "impropers" + N )

    linebreak(writer)

    # Writing the number of atom types
    writer.write(str(nAtomTypes) + T + "atom" + S + "types" + N )
    writer.write(str(nBondTypes) + T + "bond" + S + "types" + N )
    writer.write(str(nAngleTypes) + T + "angle" + S + "types" + N )
    writer.write(str(nDihedralTypes)  + T + "dihedral" + S + "types" + N )
    writer.write(str(nImproperTypes)  + T + "improper" + S + "types" + N )

    linebreak(writer)
    return


def writeBounds(writer,bdryList):
    bdryStr = (("xlo","xhi"),("ylo","yhi"),("zlo","zhi"))
    #writing x,y,z low and high
    for i in range(len(bdryList)):
        if bdryList[i][0] < 0:
            writer.write(str(bdryList[i][0]) + T + str(bdryList[i][1]) + T + bdryStr[i][0] + S + bdryStr[i][1] + N) 
        else:
            writer.write(str(bdryList[i][0]) + T + str(bdryList[i][1]) +  T + bdryStr[i][0] + S + bdryStr[i][1] + N) 
    return



def writeDataFile(dataFile = "data.CuNi",style = "atomic", latticeType = "fcc", initTemp = 300,nAtoms = [6,6,6],latticeParams = [3.6,3.6,3.6],concFunc = lambda a: 1 if a < 0.3 else 2,header = "Lammps Data File for CuNi",nBonds = 0,nAngles = 0,nDihedrals = 0,nImpropers = 0,nAtomTypes = 2,nBondTypes = 0,nAngleTypes = 0,nDihedralTypes = 0,nImproperTypes = 0):

    xLo, xHi = 0.0, nAtoms[0]*latticeParams[0] 
    yLo, yHi = 0.0, nAtoms[1]*latticeParams[1]
    zLo, zHi = 0.0, nAtoms[2]*latticeParams[2]
    bdryList = ((xLo,xHi),(yLo,yHi),(zLo,zHi))

    totNAtoms = getNumAtoms(latticeType,nAtoms[0],nAtoms[1],nAtoms[2])

    w = open(dataFile,mode = "w")
    writeHeader(w,header,totNAtoms, nBonds, nAngles, nDihedrals,nImpropers,nAtomTypes,nBondTypes,nAngleTypes,nDihedralTypes,nImproperTypes)
    writeBounds(w,bdryList)
    writeGroup(w,(0,0,0),latticeType,1,style,concFunc,nAtoms[0],nAtoms[1],nAtoms[2],latticeParams[0],latticeParams[1],latticeParams[2]) 
    writeVelocities(w,totNAtoms,initTemp,style)
    w.close()
    return


def writeInNPT(inFile = "in.CuNi",dataFile = "data.CuNi",runTime = 1000,timeStep = 0.0001,temp = 300,press = 0,readFile = "in.Template",):
    reader = open(readFile)
    writer = open(inFile,mode="w")
    simSteps = str(int(runTime/timeStep))
    writer.write("# --------------- Define Variables --------------\n")
    writer.write("variable INFILE string " + inFile + "\n")
    writer.write("variable DATAFILE string " + dataFile + "\n")
    writer.write("variable RUNTIME equal " + simSteps + "\n")
    writer.write("variable TEMPERATURE equal " + str(temp) + "\n")
    writer.write("variable PRESSURE equal " + str(press) + "\n")
    writer.write("variable RANDOM equal " + str(randint(1000000,9999999)) + "\n\n")
    for line in reader:
        writer.write(line)	
    reader.close()
    writer.close()
    return
		

def writeInNVT(inFile = "in.CuNi",dataFile = "data.CuNi", runTime = 1000,timeStep = 0.0001,temp = 300,length = 21.0,readFile = "in.Template"):
    reader = open(readFile)
    writer = open(inFile,mode="w")
    simSteps = str(int(runTime/timeStep))
    writer.write("# --------------- Define Variables --------------\n")
    writer.write("variable INFILE string " + inFile + "\n")
    writer.write("variable DATAFILE string " + dataFile + "\n")
    writer.write("variable RUNTIME equal " + simSteps + "\n")
    writer.write("variable TEMPERATURE equal " + str(temp) + "\n")
    writer.write("variable LENGTH equal " + str(length) + "\n")
    writer.write("variable RANDOM equal " + str(randint(1000000,9999999)) + "\n\n")
    for line in reader:
        writer.write(line)	
    reader.close()
    writer.close()
    return

