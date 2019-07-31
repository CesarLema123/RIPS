#this function calculates the elastic constants, as well as the bulk modulus,
#after a strain is applied in the x direction.


import numpy as np
from utils import *
import pandas as pd


#------------------------------------------------


def calcStress(logFileName):
    """
    a function that calculates the converged values of the stress tensor
    """
    numBins = 10 #can be modified
    df = readLog(logFileName) #putting the log file into a data frame
    stressArray = df["Stressxx","Stressyy","Stresszz","Stressxy"].to_numpy()
    length = df.shape[0]
    binSize = length // numBins
    aveStress = np.zeros(numBins,4)
    for j in range(4)
        for i in range(numBins)
            start = i*binSize
            aveStress[i,j] = np.average(stressArray[start:(start + binSize -1),j])
    stress = np.mean(aveStress, axis = 0)
    err = np.std(aveStress, axis = 0)
    return stress


#------------------------------------------------


def calcC11(strain,logFileName):
    """
    a function to calculate the first elastic constant
    """
    stressxx = calcStress(logFileName)[0]
    c11 = stressxx/strain
    return c11


#------------------------------------------------


def calcC12(strain,logFileName):
    """
    a function to calculate the second elastic consant
    """
    stressyy = calcStress(logFileName)[1]
    stresszz = calcStress(logFileName)[2]
    c12 = (stressyy + stresszz)/(2*strain)
    return c12


#------------------------------------------------


def calcC44(strain,logFileName):
    """
    a function to calculate an elastic constant
    """
    stressxy = calcStress(logFileName)[3]
    c44 = stressxy / strain
    return c44
       


#------------------------------------------------


def calcC(strain,logFileName):
    """
    a function which calculates all of the elastic constants
    """
    stress = calcStress(logFileName)
    stressxx = stress[0]
    stressyy = stress[1]
    stresszz = stress[2]
    stressxy = stress[3]
    c11 = stressxx/strain
    c12 = (stressyy + stresszz)/(2*strain)
    c44 = stressxy / strain
    return[c11,c12,c44]


#-----------------------------------------------


def calcBulkMod2(strain,logFileName)
    """
    an alternative way to calculate the bulk modulus
    """
    [c11,c12,c44] = calcC(strain,logFileName)
    B = (1/3)(c11 + 2*c22)
    return B


    


    
