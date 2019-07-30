# This script computes the heat capacity at constant volume and then at constant pressure. 

import numpy as np
from utils import *
import pandas as pd

#------------------------------------------------------

def equilEng(numBins,logFileName):
    """
    a function wchich calculates the equilbirium total energy. inputted is the number of bins desired and the name of the log file where the data was stores
    """
    df = readLog(logFileName) #putting the log file into a data frame
    engArray = df["TotEng"].to_numpy()
    length = engArray.size
    binSize = length // numBins
    aveEng = np.zeros(numBins)
    for i in range(numBins)
        start = i*binSize
        aveEng[i] = np.sum(engArray[start:(start + binSize-1)])/binSize #averaging the energy in each of the bins
    eng = np.average(aveEng)
    err = np.std(aveEng)
    return eng 

#------------------------------------------------------

def equilEnth(numBins,logFileName):
    """ 
    a function which calculates the equilibrium enthalpy.
    """
    df = readLog(logFileName) 
    enthArray = df["Enthalpy"].to_numpy()
    length = enthArray.size
    binSize = length // numBins
    aveEnth = np.zeros(numBins)
    for i in range(numBins)
        start = i*binSize
        aveEng[i] = np.sum(enthArray[start:(start + binSize-1)])/binSize
    enth = np.average(aveEnth)
    err = np.std(aveEnth)
    return enth

#-------------------------------------------------------

def calcTemp(logFileName):
    """
    a function which calculates the tempertaure
    """
    df = readLog(logFileName)
    tempArray = df["Temp"].to_numpy()
    temp = tempArray[4] 
    return temp

#--------------------------------------------------------

def calcCV(numTemps = 10):
    """
    This function calculates the heat capacity at constant volume.
    """
    energy = np.zeros(numTemps)
    temperature = np.zeros(numTemps)
    numDeriv = numTemps - 1
    CV = np.zeros(numDeriv)
    numBins = 10 
    for i in range(numTemps):
        logFileName = "log.data"
        [energy[i],errEng[i]] = equilEng(numBins,logFileName)
        temperature[i] = calcTemp(logFileName)
    for j in range(numDeriv):
        CV[j] = (energy[j+1]-energy[j])/(temperature[j+1]-temperature[j])
    return [CV,errEng]

#--------------------------------------------------------

def calcCP(numTemps = 10):
    """
    This function calculates the heat capacity at constant pressure. 
    """
    enthalpy = np.zeros(numTemps)
    temperature = np.zeros(numTemps)
    numDeriv = numTemps - 1
    CV = np.zeros(numDeriv)
    numBins = 10
    for i in range(numTemps):
        logFileName = "log.data"
        [enthalpy[i],errEnth[i]] = equilEnth(numBins,logFileName)
        temperature[i] = calcTemp(logFileName)
    for j in range(numDeriv):
        CP[j] = (enthalpy[j+1]-enthalpy[j])/(temperature[j+1]-temperature[j])
    return [CP,errEnth]








