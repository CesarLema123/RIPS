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
    df = {}
    EOF = False
    while True:
        try:
            line = f.readline()
        except:
            break
        if search in line:
            if n == runNum:
                keys = line.split()
                for key in keys:
                    df[key] = []
                while True:
                    try:
                        line = f.readline()
                    except:
                        EOF = True
                        break
                    try:
                        values = list(float(x) for x in line.split())
                    except:
                        break
                    for i in range(len(keys)):
                        df[keys[i]].append(values[i])
            else:
                n += 1
        else:
            pass
        if len(df.keys()) > 0 or EOF:
            break
    df = pd.DataFrame(df)
    f.close()
    return df



def periodic_dist(x,y,l):
    d,l = np.abs(np.array(x) - np.array(y)),np.array(l)
    dist = np.array([d, l - d]).min(axis = 0)
    dist = dist ** 2
    return np.sqrt(dist.sum())

def dist(x,y):
    s = 0.0
    for i in range(len(x)):
        s += (x[i] - y[i])**2
    return np.sqrt(s)

def position_corrolation(config,lx,ly,lz,maxDist = 10.0,Plot = True):
    """
    config should be a data frame with columns x,y,z for each atom at one time step.
    lx,ly,lz are the dimensions of the simulation box; positive for periodic and negative for fixed boundary conditions.
    maxDist is the cut off distance at which two atoms are no longer considered neighbors.
    """
    distList = [] # list to hold all of the distances 
    x,y,z = 0,0,0
    for i,col in enumerate(config.columns):
        if col == "x":
            x = i
        elif col == "y":
            y = i
        elif col == "z":
            z = i
    n = len(config["x"]) # number of atoms 
    for i in range(n):
        a = np.array([config.iloc[i,x],config.iloc[i,y],config.iloc[i,z]])
        for j in range(n):
            if j <= i:
                continue
            b = np.array([config.iloc[j,x],config.iloc[j,y],config.iloc[j,z]])
            # computing the distances for atoms in the original box
            if dist(a,b) < maxDist:
                distList.append(dist(a,b))
    if lx < 0.0:
        lx = 99999999
    if ly < 0.0:
        ly = 99999999
    if lz < 0.0:
        lz = 99999999
    dx = 0
    for i in range(n):
        a = np.array([config.iloc[i,x],config.iloc[i,y],config.iloc[i,z]])
        for j in range(n):
            b = np.array([config.iloc[j,x],config.iloc[j,y],config.iloc[j,z]])
            while True:
                dy = 0
                while True:
                    dz = 0
                    while True:
                        break1,break2 = False,False
                        if dx == 0 and dy == 0 and dz == 0:
                            break
                        l = np.array([dx*lx,dy*ly,dz*lz])
                        if (not break1) and (dist(a + l,b) < maxDist):
                            distList.extend(dist(a + l,b)) # append twice for both dist(x+l,y) = dist(x,y-l)
                        else:
                            break1 = True
                        if (not break2) and (dist(a,b + l) < maxDist):
                            distList.extend(dist(a,b + l))
                        else:
                            break2 = True
                        if break1 and break2:
                            break
                        dz += 1
                    if dz == 0:
                        break
                    dy += 1
                if dy == 0 and dz == 0:
                    break
                dx += 1
    distList = np.array(distList,dtype = np.float64)
    n = len(distList)
    m = min(distList)
    hist,bins = np.histogram(distList,bins = 200, range=[0,maxDist],density=True)
    if Plot:
        plt.hist(distList,bins=200,range=[0,maxDist],density = True)
        plt.show()
    return hist,bins
