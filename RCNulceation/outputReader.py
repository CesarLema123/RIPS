import pandas as pd

class LogReader:
    def __init__(self,filename,thermoLabels):
        self.filename = filename
        self.thermoLabels = thermoLabels.split()
    
    # get lines of thermo output data as list of lines
    def dataExtracter(self,includeLabelsForNewRun=False):
        self.includeLabelsForNewRun = includeLabelsForNewRun

        dataLines = []
        
        f = open(self.filename,'r')
        isDataLine = False
        for line in f.readlines():
            if isDataLine:
                if len(line.split())!= 0 and line.split()[0].isdigit():
                    dataLines.append(line.split())
                else:
                    isDataLine = False
            
            if line.split() == self.thermoLabels:
                isDataLine = True
                if includeLabelsForNewRun:     #used to seperate runs by thermoLabels
                    dataLines.append(line.split())

        f.close()
        return dataLines

    #User method to get dataframe from log data
    def getDataframe(self,seperateRunsByThermoLabels=False):
        return pd.DataFrame(self.dataExtracter(seperateRunsByThermoLabels),columns=self.thermoLabels)



# ---------------------------------------------------------
#USAGE EXAMPLE FOR GETTING DATA FRAME FROM FILENAME AND THERMO SPACE SEPERATED LIST OF THERMO COMMANDS
#USE FILE PATH IF FILE IS NOT LOCAL

#filename='log.Bulkmod',thermoLabels='Step Atoms Temp Press TotEng'
reader = LogReader('log.Bulkmod','Step Atoms Temp Press TotEng')
print(reader.getDataframe())
