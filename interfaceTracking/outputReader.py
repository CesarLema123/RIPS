import pandas as pd
import numpy as np

'''
    log files output global quantities
    dump files output peratom quatities
    
    assumes run start at 0 timestep,
    assumes first line is not a dataline
    #can edit class to take in only filename and assume all log filenames begin with log.<filename>, so seperate filename by '.' and if first string is log then set output type as 'log'
    
    for dump:
    assumes id is first row  # can fix this by looping through labels list and finding index and checking that index for atom ids
    assumes ids are in same row order for in each timestep
    assumes no clear way in datafile to differentiate run commans, in log data is grouped by run commands
    
'''

class OutputReader:
    def __init__(self,filename,outputType,dataLabels,sepUniqueRun=False):
        self.filename = filename
        self.outputType = outputType
        self.dataLabels = dataLabels.split()
        self.sepUniqueRun = sepUniqueRun
        self.datafile = None                # single or collection of datafiles
        self.ndArray = None                 # single or collection ndArrays
    
    def getDataFrame(self):
        if self.datafile is None:
            if self.outputType == 'log':
                if self.sepUniqueRun == True:
                    runKeys, runDF = [], []             # collection of datafiles and keys
                    for ind in range(self.getNDArray().shape[0]):           # initialize a dataframe for each element in the array
                        runDF.append(pd.DataFrame(self.getNDArray()[ind],columns=self.dataLabels))
                        runKeys.append(ind)
                    self.datafile = pd.concat(runDF,keys=runKeys,names=['Run Number','Row Number'])       #concatenate collection to a single dataframe
                else:
                    self.datafile = pd.DataFrame(self.getNDArray(),columns=self.dataLabels)
            elif self.outputType == 'dump':
                runKeys, runDF = [], []                 # collection of datafiles and keys
                for ind in range(self.getNDArray().shape[0]):               # initialize a dataframe for each element (data for a single atom) in the array
                    runDF.append(pd.DataFrame(self.getNDArray()[ind],columns=['step']+self.dataLabels))
                    runKeys.append(ind+1)
                self.datafile = pd.concat(runDF,keys=runKeys,names=['Atom Number','Row Number'])          #concatenate collection to a single dataframe
        return self.datafile

    def getNDArray(self):
        if self.ndArray is None:
            if self.outputType == 'log':
                self.ndArray = np.array(self.extractLogData())
            elif self.outputType == 'dump':
                self.ndArray = np.array(self.extractDumpData())
            else:
                print('Error: cannot read output type '+str(self.outputType)) # should raise an error
                return
        return self.ndArray

    def getDataLabels(self):
        return self.dataLabels
    
    def editReader(self,newFile=None,newType=None,newDataLabels=None,sepUniqueRun=None):  # relies on reader to set correct parameters
        parameterChanged = False
        
        if newFile is not None:
            self.filename = newFile
            parameterChanged = True
        if newType is not None:
            self.outputType = newType
            parameterChanged = True
        if newDataLabels is not None:
            self.dataLabels = newDataLabels
            parameterChanged = True
        if sepUniqueRun is not None:
            self.sepUniqueRun = sepUniqueRun
            parameterChanged = True
                
        if parameterChanged:        # If any class parameter changed then have to re-ExtractData
            self.datafile = None
            self.ndArray = None
        return
    
    def extractLogData(self):
        didNotfindDataLabels = True
        if self.sepUniqueRun:
            dataCollection = []
        
        f = open(self.filename,'r')
        runData = []
        isDataLine = False
        
        for line in f.readlines():          # assumes first line will not be a data line
            if isDataLine:
                if len(line.split()) != 0 and line.split()[0].isdigit():     # assumes data line starts an numeric value
                    runData.append(line.split())                             # adds dataline to collection
                else:                                                        # Line is no longer a dataline
                    isDataLine = False
        
            if line.split() == self.dataLabels:         # find the header preceding the rows of data for each unique run
                didNotfindDataLabels = False
                isDataLine = True                       # identifies the following line as a dataline
                if self.sepUniqueRun:
                    dataCollection.append(np.array(runData))      # saves array of data for previous run
                    runData = []                                  # resets array for new run data
        f.close()

        if didNotfindDataLabels:                            # check if dataLabels were found atleast once
            print('ERROR: did not find data with current datalabels')
            return []                                       # should raise an error instead of returning empty list
        else:
            if self.sepUniqueRun:
                dataCollection.append(np.array(runData))    # add array of data for last run
                return dataCollection[1:]                   # first item is an empty list
            else:
                return runData

    def extractDumpData(self):
        dataHeader = 'ITEM: ATOMS'.split() + self.dataLabels     # header in output files of data lines
        
        f = open(self.filename,'r')
        datalines = [line.strip().split() for line in f.readlines()]                            # collection of lines in output file
        numAtoms = int(datalines[datalines.index('ITEM: NUMBER OF ATOMS'.split())+1][0])        # get number of atoms from output file
        widthOfHeader = datalines.index('ITEM: ATOMS'.split()+self.dataLabels)+1                # get number of lines before first set of dataline, assumes the width is the same for each timestep
        totData = []
        numTimesUniqueAtomDataAppears = int(len(datalines)/(numAtoms+widthOfHeader))            # number of times data lines for an atom with id x appears
        linesBeforeAtomRepeat = numAtoms+widthOfHeader                                          # number of lines for dataline
        timestepArray = [datalines[datalines.index('ITEM: TIMESTEP'.split())+1+(ind*linesBeforeAtomRepeat)] for ind in range(numTimesUniqueAtomDataAppears)]        # creates collection of timestep values for each set of timeste
        
        for i in range(numAtoms):                                                               # create a collection of datalines for each atom
            atomDataLineInd = widthOfHeader+i                                                   # index of dataline for atom with id x=i, assumes data is printed for each atom in order of 1,...,N
            totData.append(np.array([timestepArray[ind]+datalines[atomDataLineInd+(ind*linesBeforeAtomRepeat)] for ind in range(numTimesUniqueAtomDataAppears)]))   # creats collection of data from each timestep for a unique atom
        f.close()
        
        return totData

