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


def readLogPD(fileName):
    df = pd.read_csv(fileName,sep = "\s+")
    return df
