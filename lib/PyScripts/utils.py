import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt



def readDump(fileName):
    """
    This function reads in a dump.atom file with all of the per atom values and returns a 2d pandas dataframe 
    """
    search_time = "ITEM: TIMESTEP"
    search_atom = "ITEM: ATOMS"
    f = open(fileName,mode = "r")
    d = {"Time Step": []} # dictionary to be made into a data frame initialized so Time Step is the first value
    ts = 0 #number of the time step
    nostep = False # an indicator if we should read a new line at the beginning
    while True:
        try:
            if not nostep:
                line = next(f)
            else:
                nostep = False
            if search_time in line:
                ts = float(next(f)[:-1]) # go to next line, remove \n char and make it the time step
            elif search_atom in line:
                if len(d.keys()) == 1: # if the dictionary headers haven't been added yet do...
                    keys = line[len(search_atom):].split() # remove "Item: ATOM" and make a list of the words remaining in the line for the header
                    for key in keys:
                        d[key] = [] # initializing the dictionary
                while True:
                    try:
                        line = next(f)
                        values = [ts,] + list(round(float(x),4) for x in line.split())
                        keys = list(d.keys())
                        for i in range(len(keys)):
                            d[keys[i]].append(values[i])
                    except: # Break if we hit a line which isn't numeric data
                        nostep = True  # Don't read a new line since we already read one in the try section
                        break 
        except:
            break # Break if we hit the EOF
    df = pd.DataFrame(d)
    return df


def readLog(fileName,runNum = 1):
    """
    fileName is the name of the log file to be read.
    runNum is the run number which corresponds to the run command in the input file.
    """
    search = "Step"
    n = 1
    f = open(fileName)
    data = []
    header = ""
    for line in f:
        if header:
            try:
                d = list(float(x) for x in line.split())
                data.append(d)
            except:
                break
        elif search in line:
            if n == runNum:
                header = line
            else:
                n+=1
    df = pd.DataFrame(data,columns = [x for x in header.split()])
    f.close()
    return df


def fixAtomIdCuNi(readFile,writeFile):
    r = open(readFile)
    w = open(writeFile,mode = "w")
    for line in r:
        if line[0] == "1":
            line = "Cu" + line[1:]
        elif line[0] == "2":
            line = "Ni" + line[1:]
        w.write(line)
    r.close()
    w.close()

def readLogPD(fileName):
    df = pd.read_csv(fileName,sep = "\s+")
    return df

def prepForMatLab(readFile,writeFile):
    """
    This function takes in the lammps atom data output for grain tracking and makes
    new files containing only the data for each timestep. These can then be inputted into
    the matlab grain tracking code.
    """
    r = open(readFile)
    f = open(readFile)
    timestep = ""
    getTime = False
    search = "ITEM: TIMESTEP"
    for line in r:
        if getTime:
            timestep = line.split()[0]
            getTime = False
            f.close()
            f = open(writeFile + "_" + timestep + ".cfg",mode = "w")
            f.write(search + "\n")
            f.write(line)
        elif search in line:
            getTime = True
        else:
            f.write(line)
    return
        


def getFinalStats(fileName):
    """
    This function gets the thermodynamic values from a simulation where the output is time averaged data.
    """
    df = readLog(fileName)
    header = ("Energy Ave","Energy Std","Energy Stdm","Temp Ave","Temp Std","Temp Stdm","Volume Ave","Volume Std","Volume Stdm","Press Ave","Press Std","Press Stdm","Enthalpy Ave","Enthalpy Std","Enthalpy Stdm")
    thermoVars = ("Energy","Temp","Volume","Press","Enthalpy")
    thermoVarDict = {"Energy":["TotEng","v_varAveEnergy","v_energySTD"],"Temp":["Temp","v_varAveTemp","v_tempSTD"],"Volume":["Volume","v_varAveVolume","v_volumeSTD"],"Press":["Press","v_varAvePress","v_pressSTD"],"Enthalpy":["Enthalpy","v_varAveEnthalpy","v_enthalpySTD"]}
    data = []
    for var in thermoVars:
        try:
            colNames = thermoVarDict[var]
            N = len(list(df[colNames[1]]))
            ave,std = list(df[colNames[1]])[-1],list(df[colNames[2]])[-1]
            stdm = std/np.sqrt(N)
            data.extend([ave,std,stdm])
        except:
            print("Column %s not found. Entering zeros for all values." %(var))
            data.extend([0.0,0.0,0.0])
    return data,header 







def getThermoStats(fileName):
    """
    This Function reads a cut log file and outputs the average, standard deviation and standard deviaton of the mean for each thermodynamic variable
    """
    df = readLog(fileName)

    N = len(df["Step"])
    nBins = 20
    while N//nBins < 100:
        nBins -= 1
    lBins = N//nBins

    header = ("Energy Ave","Energy Std","Energy Stdm","Temp Ave","Temp Std","Temp Stdm","Volume Ave","Volume Std","Volume Stdm","Press Ave","Press Std","Press Stdm","Enthalpy Ave","Enthalpy Std","Enthalpy Stdm")
    thermoVars = ("Energy","Temp","Volume","Press","Enthalpy")
    thermoVarDict = {"Energy":["TotEng","v_varAveEnergy","v_energySTD"],"Temp":["Temp","v_varAveTemp","v_tempSTD"],"Volume":["Volume","v_varAveVolume","v_volumeSTD"],"Press":["Press","v_varAvePress","v_pressSTD"],"Enthalpy":["Enthalpy","v_varAveEnthalpy","v_enthalpySTD"]}
    data = []
    for var in thermoVars:
        try:
            colNames = thermoVarDict[var]
            inst,ave,std = list(df[colNames[0]]),list(df[colNames[1]]),list(df[colNames[2]])
            aveStd = sum(std)/N
            aveBins = [0.0]*nBins
            for b in range(nBins):
                A = sum(ave[b*lBins:(b+1)*lBins])/lBins
                aveBins[b] = A
            A = sum(aveBins)/nBins
            S = np.sqrt(sum((x - A)**2 for x in aveBins)/nBins)
            data.extend([A,aveStd,S])
        except:
            print("Column %s not found. Entering zeros for all values." %(var))
            data.extend([0.0,0.0,0.0])
    return data,header 


def qplot(fileName,stepSize = 0.0001):
    try:
        df = readLogPD(fileName)
    except:
        print("Error in qplot. File being read may not exist.")
        return 1
    step = list(df["Step"])
    time = list(stepSize*(s - step[0]) for s in step)
    colDir = {}
    i = 1
    for col in list(df.columns)[1:]:
        print(str(i) + 20*"-" +" " +  col)
        colDir[i] = col
        i += 1
    rep = int(input("Please choose a number from above: "))
    y = list(df[colDir[rep]])
    plt.scatter(time,y,c = "r",s = 8)
    plt.xlabel("Time (ns)")
    plt.ylabel(colDir[rep])
    plt.show()
    return



def forwDif(X,Y):
    """
    This script computes and approximate derivative using a forward difference method.
    If X,Y are lists of length N then the output is two lists of N-1 corresponding t
    the approximate derivative and their corresponding X coordinates which are taken to be
    the mid points between each adjacent pair.
    """
    N = len(X)
    dYdX,nX = [0.0]*(N-1),[0.0]*(N-1)
    for i in range(N-1):
        dYdX[i] = (Y[i+1] - Y[i])/(X[i+1] - X[i])
        nX[i] = (X[i+1] + X[i])/2
    return dYdX,nX

def dForwDif(X,dX,Y,dY):
    """
    This script computes and approximate derivative using a forward difference method.
    If X,Y are lists of length N to be used in for computing the derivate and dX and dY are their uncertainties.
    The output is three lists of N-1 corresponding to
    the approximate derivative, the uncertainty associated with the forward difference given the errors,
    and their corresponding X coordinates which are taken to be
    the mid points between each adjacent pair.
    """
    N = len(X)
    dYdX,ddYdX,nX = [0.0]*(N-1),[0.0]*(N-1),[0.0]*(N-1) # confusing labels but ddYdX is the error in the derivative
    for i in range(N-1):
        dYdX[i] = (Y[i+1] - Y[i])/(X[i+1] - X[i])
        ddYdX[i] = np.sqrt((dY[i+1]/(X[i+1] - X[i]))**2 + (dY[i]/(X[i+1] - X[i]))**2 + (dX[i+1]*(Y[i+1] - Y[i])/(X[i+1] - X[i])**2)**2 + (dX[i]*(Y[i+1] - Y[i])/(X[i+1] - X[i])**2)**2) 
        nX[i] = (X[i+1] + X[i])/2
    return dYdX,ddYdX,nX
    
