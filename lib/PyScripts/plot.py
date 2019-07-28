import matplotlib.pyplot as plt
import numpy as np
from py_scripts.utils import *



def plot_from_log(fileName = "log.lammps",colName = "Temp",runNum = 1,waitSteps = 0):
    """
    fileName is the name of the log file to read from.
    colName is the name of the column given in the log file.
    runNum is the number of the run which corresponds to the run command in a lammps imput file.
    waitSteps is how many steps to ignore at the start of the run
    """
    df = readLog(fileName,runNum)
    x = np.array(df[colName])[waitSteps:]
    plt.plot(x)
    plt.show()
    return
