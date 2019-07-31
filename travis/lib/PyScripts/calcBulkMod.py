#This script computes a bulk modulus

import numpy as np
from utils import *
import pandas as pd

#---------------------------------------------------------

def equilPres(numBins,logFileName):
    """
    a function to calculate the equilibrium pressure. Inputted is the number of bins desired and the name of the log file where the data was stored.
    """
    df = readLogPD(logFileName) #putting the log file into a data frame
    pressArray = df["v_varAvePress"].to_numpy() #extracting the pressure vales
    length = pressArray.size
    binSize = length // numBins
    avePress = np.zeros(numBins)
    for i in range(numBins):
        start = i*binSize
        avePress[i] = np.sum(pressArray[start:(start + binSize)])/binSize #averaging the pressure in each of the bins
    press = np.average(avePress)
    return press

#---------------------------------------------------------

def calcVolume(logFileName = "log.data"):
    """
    a function to calculate the volume for each simulation.
    """
    df = readLogPD(logFileName)
    volArray = df["v_varAveVolume"].to_numpy()
    vol = sum(volArray)/len(volArray) #Taking the average of the volumes
    return vol

#----------------------------------------------------------

def bulkMod(numVols = 10,numSims = 13):
    """
    calculates the bulk modulus from data from simulations with different volumes at constant temperature. inputted is the number of simulations and then temperature
    """
    pressure = np.zeros([numSims,numVols]) #initialising
    volume = np.zeros([numSims,numVols])
    numDeriv = numVols - 1
    bM = np.zeros([numSims,numDeriv])
    dpdv = np.zeros([numSims,numDeriv])
    numBins = 10
    for i in range(numSims):
        for l in range(numVols):
            k = 1 + l*0.001
            logFileName = "log.data"
            pressure([i,l]) = equilPress(numBins,logFileName)
            print("this is pressure = " + str(pressure[i]))
            volume([i,l]) = calcVolume(logFileName)
        for j in range(numDeriv):
            dpdv([i,j]) = (pressure([i,j+1])-pressure([i,j]))/(volume([i,j+1])-volume([i,j]))
            bM([i,j]) = -volume([i,j])*dpdv([i,j])
    return bM

