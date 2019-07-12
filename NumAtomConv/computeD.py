from utils import *
from scipy import stats


#
#    fileName = "log.lammps"
#    runNum = 2

    #use terminal option after calling this file to specify what log file to use
#    if (len(sys.argv) > 2):
#        fileName = sys.argv[1]
#        runNum = int(sys.argv[2])
    #else:
    #    print("Invalid number of arguments")
    #    exit()
def findDiff(fileName):

    #import time and msd as vectors from specified log file
    ldf = readLog(fileName, 2) #second argument specifies run number from sim
    t = ldf['Step'].values
    msd = ldf['c_MSD[4]'].values

    #truncate t, msd to only look at second half of data
    length = len(t)
    tD = t[length//2:]
    msdD = msd[length//2:]

    #compute Diffusion Coeff
    slope, intercept, r_value, p_value, std_err = stats.linregress(tD, msdD)
    DCoeff = slope * 10**(-1)
    print('R-sq value: ', r_value, '\n', 'Diff Coeff (cmsq/s): ','{0:.15f}'.format(DCoeff))
    return DCoeff

