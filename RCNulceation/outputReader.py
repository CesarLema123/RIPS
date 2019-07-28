import pandas as pd


'''
class dumpReader:
    def __init__(self,filename):
        self.holder = 'holding variable'
'''


class LogReader:
    def __init__(self,filename,thermoLabels = ''):
        self.filename = filename
        self.thermoLabels = thermoLabels.split()
    
    # func to get lines of log files with the thermo output data as a collection of lines/rows
    def dataExtracter(self,includeLabelsForNewRun=False):
        dataLines = []               # list to collect rows/line of dump file with thermo data
        
        f = open(self.filename,'r')
        isDataLine = False                 # variable to identify a row/line of dump file as data line

        for line in f.readlines():          # for first iteration, assumes first line will not be a data line
            if isDataLine:                  #true when found a data line and adds it to data collection
                if len(line.split())!= 0 and line.split()[0].isdigit():     # assumes data line starts an numeric value
                    dataLines.append(line.split())
                else:
                    isDataLine = False
            
            if line.split() == self.thermoLabels:        #find the thermo labels line preceding the rows of data
                isDataLine = True                       # labels line is not a data line but next iteration will be
                if includeLabelsForNewRun:             #easily identify seperate runs in list by thermoLabels lines
                    dataLines.append(line.split())
        f.close()
        return dataLines

    #User method to get dataframe from log data
    def getDataframe(self,seperateRunsByThermoLabels=False):
        return pd.DataFrame(self.dataExtracter(seperateRunsByThermoLabels),columns=self.thermoLabels)

    '''
    #method to find thermolabels from log file by searching line by line unti thermo command is found then extract
    thermo output arguements
    def findThermoLabels(self):
    code
    #would make 'includeLabelsForNewRun' from data extracter obsolete as we can also extract eat run as its own data file and append them to a datafile list, each element would be a dataframe for an individual run
    '''




# ---------------------------------------------------------
#USAGE EXAMPLE FOR GETTING DATA FRAME FROM FILENAME AND THERMO SPACE SEPERATED LIST OF THERMO COMMANDS
#USE FILE PATH IF FILE IS NOT LOCAL

#filename='log.Bulkmod',thermoLabels='Step Atoms Temp Press TotEng'
reader = LogReader('log.Bulkmod','Step Atoms Temp Press TotEng')
print(reader.getDataframe())
