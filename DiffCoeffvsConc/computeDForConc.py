#from utils import *
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def findDiff(fileName):
    """
    This function calculates a diffusion coefficient given a log file from lammps.
    """
    #import time and msd as vectors from specified log file
    #ldf = readLog(fileName, 1) #second argument specifies run number from sim
    #above line is deprecated - travis does preprocessing on log files now
    ldf = pd.read_csv(fileName, '\s+')
    t = ldf['Step'].values
    msd = ldf['c_MSD[4]'].values

    #compute Diffusion Coeff
    slope, intercept, r_value, p_value, std_err = stats.linregress(t, msd)
    DCoeff = slope/6 * 10**(-1)
    print('R-sq value: ', r_value, '\n', 'Diff Coeff (cmsq/s): ','{0:.15f}'.format(DCoeff))
    return DCoeff

#create an array to store concentration vs. Diffusion Coeffi
result = np.zeros((11,2))
temp = 2000 #specifies constant temperature to look at. change later to make dynamic/user input

for conc in range(11):
    logFile = "C" + str(conc) + "log.data"
    #store concentration as a percentage of Ni in first column
    result[conc,0] = conc*10 
    result[conc,1] = findDiff(logFile)

print(result)
plt.plot(result[:,0], result[:,1])
plt.xlabel('Concentration of Ni')
plt.ylabel('Diffusion Coefficient (cmsq/sec)')
plt.savefig('Conc(Ni).vs.Diff_' + 'Temp' + str(temp) + '.png')
