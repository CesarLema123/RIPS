#This script computes a bulk modulus


#Import what is needed
import os
import numpy as np
from utils import *
import pandas as pd

#---------------------------------------------------------

def getRunNum(loopFileName):
    """
    a function that caculates the correct run number for the data wanted
    """
    n = int( open(loopFileName).readline().split()[0] )
    runNum = n + 2#2#3
    return runNum

#-------------------------------------------------------

def equilPress(runNum,numBins,logFileName):
    """
    a function to calculate the equilibrium pressure. Inputted is the run number, which is the run number of the run after the LAMMPS simulation deems that equilibrium pressure has been met. The number of bins and the file name of the log file is also inputted. 
    """
    df = readLog(logFileName,runNum) #putting the log file into a data frame
    pressArray = df["Press"].to_numpy() #extracting the pressure vales
    length = pressArray.size
    binSize = length // numBins
    avePress = np.zeros(numBins)
    for i in range(numBins):
        start = i*binSize
        avePress[i] = np.sum(pressArray[start:(start + binSize)])/binSize #averaging the pressure in each of the bins
    press = np.average(avePress)
    return press

#------------------------------------------------------

def calcVolume(runNum,logFileName):
    """
    a function to calculate the volume for each simulation.
    """
    df = readLog(logFileName,runNum)
    volArray = df["Volume"].to_numpy()
    vol = volArray[4] #Volume is constant so can just choose any value!
    return vol
    
#---------------------------------------------------------

def bulkMod(numSims,temp = 2000):
    """
    a function to run many LAMMPS simulations at constant temperature and calculate a bulk modulus. inputted is the number of simulations and then temperature
    """
    pressure = np.zeros(numSims) #initialising
    volume = np.zeros(numSims)
    numDeriv = numSims - 1
    bM = np.zeros(numDeriv)
    dpdv = np.zeros(numDeriv) 
    xScale = 1
    yScale = 1
    zScale = 1
    numBins = 10
    for i in range(numSims):
        xScale += 0.001*i #the volume is changed for each simulation, but the relative dimensions of the box remain the same so x,y,z are scaled the same
        yScale += 0.001*i  
        zScale += 0.001*i
        os.system("lmp_daily -in in.bulkCuNi -var TEMP " + str(temp) + " -var xscale " + str(xScale) + " -var yscale " + str(yScale) + " -var zscale " + str(zScale) + " -var simNum " + str(i))
        runNum = getRunNum("loopNum"+str(i)+".txt")
        logFileName = "log.bulkMod"+str(i)
        pressure[i] = equilPress(runNum,numBins,logFileName)
        print("this is pressure = " + str(pressure[i]))
        volume[i] = calcVolume(runNum,logFileName)
    for j in range(numDeriv):
        dpdv[j] = (pressure[j+1]-pressure[j])/(volume[j+1]-volume[j])
        bM[j] = -volume[j]*dpdv[j]
    return bM
    

