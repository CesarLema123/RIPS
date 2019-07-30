#This script computes a bulk modulus

import numpy as np
from utils import *
import pandas as pd

#---------------------------------------------------------

def equilPres(numBins,logFileName):
    """
    a function to calculate the equilibrium pressure. Inputted is the number of bins desired and the name of the log file where the data was stored.
    """
    df = readLog(logFileName) #putting the log file into a data frame
    pressArray = df["Press"].to_numpy() #extracting the pressure vales
    length = pressArray.size
    binSize = length // numBins
    avePress = np.zeros(numBins)
    for i in range(numBins):
        start = i*binSize
        avePress[i] = np.sum(pressArray[start:(start + binSize-1)])/binSize #averaging the pressure in each of the bins
    press = np.average(avePress)
    err = np.std(avePress)
    return [press,err]

#---------------------------------------------------------

def calcVolume(logFileName):
    """
    a function to calculate the volume for each simulation.
    """
    df = readLog(logFileName)
    volArray = df["Volume"].to_numpy()
    vol = volArray[4] #Volume is constant so can just choose any value!
    return vol

#----------------------------------------------------------

def bulkMod(numSims = 13):
    """
    calculates the bulk modulus from data from simulations with different volumes at constant temperature. inputted is the number of simulations and then temperature
    """
    pressure = np.zeros(numSims) #initialising
    volume = np.zeros(numSims)
    numDeriv = numSims - 1
    bM = np.zeros(numDeriv)
    dpdv = np.zeros(numDeriv)
    numBins = 10
    for i in range(numSims):
        logFileName = "log.data"
        [pressure[i],pressErr[i]] = equilPress(numBins,logFileName)
        volume[i] = calcVolume(logFileName)
    for j in range(numDeriv):
        dpdv[j] = (pressure[j+1]-pressure[j])/(volume[j+1]-volume[,j])
        bM[j] = -volume[j]*dpdv[j]
    return [bM,pressErr]

