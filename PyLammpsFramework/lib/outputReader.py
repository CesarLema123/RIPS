import pandas as pd
import numpy as np

"""
    This file contains a class that can be used to extract simulation data from log and dump type LAMMPS output files.
    
    This file can be imported as a module.
"""


class OutputReader:
    """ A class for extracting data from LAMMPS dump and log type output files.
    
    The class is meant to be used as an object that extracts data from an associated (specificed as string representing the filename) LAMMPS output file. Class instances are meant to be initialized with a default existing LAMMPS dump or log type
    output file, file type, label(s) of the data outputted, and (specific) for log type files: a boolean for whether the extracted data collection should be compartmentalized by unique LAMMPS run commands. Once initialized, the class methods are
    meant to get data from the associated files as a Pandas datafile or Numpy ndarray and to update/change the LAMMPS output file associated with the class instance.
    LAMMPS log type output files contain global simulation quatities and dump type output files contain per atom simulation quantities. Therefore methods for extracting data and format of the resulting data collectoins are different for each
    output type. Some simulation assumtions are made including: simulation data outputted in files start a 0 timestep and is not reset to 0, output files follow specific formats, dataLables/data headers always come before simulation data, etc.
    
    Attributes:
        filename = A string representing the filename (with file extension) of a LAMMPS type output file.
        outputType = A string, "log" or "dump", indicating the file type outputted by LAMMPS.
        dataLabels = A space seperated string inidicating the data labels/arguements in the LAMMPS output file. The input should match the entire data header in the output file.
        sepUniqueRun = For log type output files, a boolean representing whether the data collection object returned from the class methods ia compartmentalized by unique LAMMPS run commands. The default value is False, indicating that the data collection object returned from the class methods should be returned as one collection for the entire simulation.
        datafile = A Pandas DataFrame instance with the extracted data from the associated LAMMPS output file. This should not be directly accessed, instead the respective method should be called to get the DataFrame as the object may be set or reset to None through out the life of the class instace.
        ndArray = A Numpy ndarray instance with the extracted data from the associated LAMMPS output file. This should not be directly accessed, instead the respective method should be called to get the ndarray a the object may be set or reset to None through out the life of the class instance.
        
    Methods:
        getDataFrame(): returns data specified by data labels attribute as a Pandas Dataframe from the associated LAMMPS output file.
        getNDArray(): returns data specified by set data labels attribute as a Numpy ndarray from the associated LAMMPS output file.
        getDataLabels(): returns data labels a class instance is associated with.
        editReader(newFile=None,newType=None,newDataLabels=None,sepUniqueRun=None): modify associated output file reader parameter(s) or change the file and respective parameters associated with the class instance.
        extractLogData(): implementation method called by the getNDArray method to read and extract data from log type output files.
        extractDumpData(): implementation method called by the getNDArray method to read and extract data from dump type output files
    """
    def __init__(self,filename,outputType,dataLabels,sepUniqueRun=False):
        """ Initializes OutputReader object with a default LAMMPS style dump and Log file.
            
        Class methods are implemented to extract collections data objects with data from the file the object is associated with.
            
        Args:
            filename: A string representing the filename (with file extension) of a LAMMPS type output file.
            outputType: A string, "log" or "dump", indicating the file type outputted by LAMMPS.
            dataLabels: A space seperated string inidicating the data labels/arguements in the LAMMPS output file. The input should match the entire data header in the output file.
            sepUniqueRun: For log type output files, a boolean representing whether the data collection object returned from the class methods ia compartmentalized by unique LAMMPS run commands. The default value is False, indicating that the data collection object returned from the class methods should be returned as one collection for the entire simulation.
            
        TODO:
        
        """
        
        self.filename = filename
        self.outputType = outputType
        self.dataLabels = dataLabels.split()
        self.sepUniqueRun = sepUniqueRun
        self.datafile = None                # single or collection of datafiles
        self.ndArray = None                 # single or collection ndArrays
    
    def getDataFrame(self):
        """  Returns data from LAMMPS output file as a Pandas DataFrame.
    
        Converts ndarray attribute or calls getNDArray method if ndarray attribute is None and initializes a Pandas DataFrame to return with ndarray attribute.
 
        Return:
            A Pandas dataframe with each column representing a arguemnt/term in the dataLabels attribute and containing respective data values. Row data and dataframe structure depends on attributes values.
        
        TODO:
        
        """
        
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
        """ Returns data from LAMMPS output file as Numpy ndarray.
            
        Calls respective file type method to extract/read data from LAMMPS output file and sets ndarray attribute if the attribute is none. Returns ndarray attribute
        
        Return:
            A Numpy ndarray with each column representing a arguemnt/term in the dataLabels attribute and containing respective data values. Row data and ndarray dimensions depends on attributes values.
        
        TODO:
        
        """
        
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
        """ set instance attributes
        
        Args:
            newFile = A string representing the new filename (with file extension) of a LAMMPS type output file to associate the instance with.
            newType =
            newDataLabels =
            sepUniqueRun =
        
        Return:
            None

        TODO:
            Return a boolean indicating whether the new/changed parameters were set and logically go together.
        """
        
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
        """ Extract data under the specified outputLabels in the associated log output file.
            
        An implementation method used by the class to read data from the associated file. Extracts data using the dataLabels and sepUniqueRun attributes. Data is extrscted by searching for the header line in the output file matching the dataLabels
        attribute. The lines below the header containing alphanumeric values are collected. This method should not be called by the user.
        
        Return:
            Python list instance with each element as the exact space seperated data values lines from the associated file. If sepUniqueRun attribute is true then the elements are Numpy ndarrays containing the exact space seperated data values
            lines from the output file for each unique LAMMPS run commmand.
            
        TODO:
            Make this method private
        """
        
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
        """ Extract data under the specified outputLabels in the associated dump output file.
        
        An implementation method used by the class to read data from the associated dump file. Extracts data using the dataLabels and sepUniqueRun attributes. Data is extracted by indexing all of the space seperated data values lines in the dump
        file associated with each atom id. This method should not be called by the user. Assumptions made about the dump file are: tom ID's are in the same increasing order (starting from 1) for the data under each timestep.
        
        Return:
            Python list instance with each element as a Numpy ndarray with the data lines corresponding to one specific atoom ID.
        
        TODO:
            Make this method private
        """
        
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

