#This script computes a (volumetric) coefficient of thermal expansion

import numpy as np
from utils import *
import pandas as pd

#-------------------------------------------------------------------------

def equilVol(numBins,logFileName):
    """
    a function to calculate the equilibrium volume Inputted is the number of bins desired and the name of the log file where the data was stored.
    """
    df = readLog(logFileName) #putting the log file into a data frame
    volArray = df["Volume"].to_numpy() #extracting the pressure vales
    length = volArray.size
    binSize = length // numBins
    aveVol = np.zeros(numBins)
    for i in range(numBins):
        start = i*binSize
        aveVol[i] = np.sum(volArray[start:(start + binSize)])/binSize #averaging the pressure in each of the bins
    vol = np.average(aveVol)
    return press

#-------------------------------------------------------------------------

def calcTemp(logFileName)
    """
    a function to calculate the temperature for each simulation
    """
    df = readLog(logFileName)
    tempArray = df["Temp"].to_numpy()
    temp = tempArray[4] #temperature is constant so can just choose any value

#-------------------------------------------------------------------------

def thermExp(numTemp)
    """
    this function calculates the coefficient of (volumetric) thermal expansion. Inputted is the number of different temperatures the simulation will run at.
    """
    volume = np.zeros([numTemp]) #initialising 
    temperature = np.zeros([numTemp])
    numDeriv = numTemp - 1 #there is one less derivative calculated because you need two values to approx dV/dT
    CTE = np.zeros(numDeriv)
    dvdt = np.zeros(numDeriv)
    numBins = 10
    for i in range(numTemp)
        logFileName = #??
        volume[i] = equilVol(numBins,logFileName)
        temperature[i] = calcTemp(logFileName)
    for j in range(numDeriv)
        dvdt[i] = (volume[i+1]-volume[i])/(temperature[i+1]-temperature[i])
        CTE[i] = dvdt[i]/volume[i]
    return CTE


