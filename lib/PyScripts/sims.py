from utils import *
from random import randint
import dataFileGenerator as dataF
import inFiles as inF
import numpy as np
import os
import csv
sh = os.system # I am running this on a bash terminal

   
class simulation():
    def __init__(self,pythonLib = "$HOME/RIPS/lib/PyScripts",awkLib = "$HOME/RIPS/lib/AwkFiles",lammps = "lmp_daily -in",runTimes = [100,],alloy = "CuNi",latticeConst = 3.63,latticeType = "FCC",numAtomTypes = 2,systemSizes = [6,],temperatures = [300,],pressures = [0,],lengths = [6*3.63,],concPercents = [30,],timeStep = 0.0001,simType = "npt",fileName = "CuNi",potentialFile = "CuNi.eam.alloy",inTemplate = "in.Template"):
        self.pythonLib = pythonLib
        self.awkLib = awkLib
        self.lammps = lammps
        self.runTimes = runTimes
        self.alloy = alloy
        self.latticeConst = latticeConst
        self.latticeType = latticeType
        self.numAtomTypes = numAtomTypes
        self.systemSizes = systemSizes
        self.temperatures = temperatures
        self.pressures = pressures
        self.lengths = lengths
        self.concPercents = concPercents
        self.timeStep = timeStep
        self.simType = simType
        self.fileName = fileName
        self.potentialFile = potentialFile
        self.inTemplate = inTemplate
        return 

    def setSimParams(self,pythonLib = "",awkLib = "",lammps = "",alloy = "",latticeConst = 0.0,latticeType = "",numAtomTypes = 0,runTimes = [],systemSizes = [],temperatures = [],pressures = [],lengths = [],concPercents = [],timeStep = 0.0,simType = "",fileName = "", potentialFile = "",inTemplate = ""):
        if pythonLib:
            self.pythonLib = pythonLib
        if awkLib:
            self.awkLib = awkLib
        if lammps:
            self.lammps = lammps
        if alloy:
            self.alloy = alloy
        if latticeConst:
            self.latticeConst = latticeConst
        if latticeType:
            self.latticeType = latticeType
        if numAtomTypes:
            self.numAtomTypes = numAtomTypes
        if any(runTimes):
            self.runTimes = runTimes
        if any(systemSizes):
            self.systemSizes = systemSizes
        if any(temperatures):
            self.temperatures = temperatures
        if any(pressures):
            self.pressures = pressures
        if any(lengths):
            self.lengths = lengths
        if any(concPercents):
            self.concPercents = concPercents
        if timeStep:
            self.timeStep = timeStep
        if simType:
            self.simType = simType
        if inTemplate:
            self.inTemplate = inTemplate
        if fileName:
            self.fileName = fileName
        if potentialFile:
            self.potentialFile = potentialFile
        return 

    def getWorkDir(self,time,size,temp,pv,concPercent):
        if self.simType == "npt":
            return "Out/RunTime"+str(time)+"Size"+str(size)+"Conc"+str(concPercent)+"Temp"+str(temp)+"Press"+str(round(pv,2))
        elif self.simType == "nvt":
            return "Out/RunTime"+str(time)+"Size"+str(size)+"Conc"+str(concPercent)+"Temp"+str(temp)+"Length"+str(round(pv,2))
        else:
            print("Unknown sim type.")
            return 1
    
    def cpTmp(self,wd):
        sh("cp " + self.inTemplate + " " + wd)
        sh("cp " + self.potentialFile + " " + wd)
        return 0
    
   
    def inFile(self):
        return "in." + self.fileName

    def dataFile(self):
        return "data." + self.fileName


    def runLammps(self):
        sh(self.lammps + " " + self.inFile())
        return 0

    def runSims(self):
        if self.simType == "npt":
            vOrP = self.pressures
            varString = "PRESSURE"
        elif self.simType == "nvt":
            vOrP = self.lengths
            varString = "LENGTH"
        else:
            print("Unknown Simulation Type")
            return 1
        cwd = os.getcwd()
        sh("mkdir Out")
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concPercent in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,var,concPercent)
                            sh("mkdir " + wd) 
                            self.cpTmp(wd)
                            os.chdir(wd)
                            # write the input file and the data file
                            inFile = inF.inFile(fileName = self.fileName, readFile = self.inTemplate,runTime = time,timeStep = self.timeStep)
                            inFile.writeInFile(options = ["TEMPERATURE equal " + str(temp),varString + " equal " +str(var),"RANDOM equal " + str(randint(1000000,9999999))])
                            dataFile = dataF.AtomDataFileGenerator(filename = self.fileName,latticeType = self.latticeType,alloy = self.alloy,customLatticeConst = self.latticeConst,systemSize = size, atomTypes = self.numAtomTypes, alloyCompPercent = concPercent)
                            dataFile.createDataFile()
                            self.runLammps()
                            os.chdir(cwd)
        return 0
    
    def cleanOutput(self):
        if self.simType == "npt":
            vOrp = self.pressures
        elif self.simType == "nvt":
            vOrP = self.lengths
        else:
            print("Unknown simulation type.")
            return 1
        cwd = os.getcwd()
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concPercent in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,var,concPercent)
                            os.chdir(wd)
                            sh("awk -f " + self.awkLib + "/awkReadLog log.run > log.data")
                            try:
                                sh("awk -f " + self.awkLib + "/awkReadLog log.loop > log.temp")
                                sh("awk -f " + self.awkLib + "/awkCombineLog log.temp > log.loop")
                            except:
                                pass
                            sh("awk -f " + self.awkLib + "/awkFixElementId dump.xyz > dump.pos")
                            sh("rm -f log.run log.temp dump.xyz" + " " + self.potentialFile + " " + self.inTemplate)
                            os.chdir(cwd)
        return 
    
    
    def recordData(self):
        thermoDataFile = input("Please give a name for the file to write to: ")
        w = open(thermoDataFile,mode = "w")
        writer = csv.writer(w,delimiter = " ")
        if self.simType == "npt":
            vOrP = self.pressures
        elif self.simType == "nvt":
            vOrP = self.lengths
        else:
            print("Unknown simulation type.")
            return 1
        header = ""
        cwd = os.getcwd()
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concPercent in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,var,concPercent)
                            os.chdir(wd)
                            try:
                                if not header:
                                    data,header = getThermoStats("log.data")
                                    writer.writerow(header)
                                    writer.writerow(data)
                                else:
                                    data = getThermoStats("log.data")[0]
                                    writer.writerow(data)
                            except:
                                pass
                            os.chdir(cwd)
        w.close()
        return 
    
     
    def getData(self):
        """
        This script collects all of the thermodynamic data from simulation runs and puts them into a data frame.
        """
        if self.simType == "npt":
            vOrP = self.pressures
        elif self.simType == "nvt":
            vOrP = self.lengths
        else:
            print("Unknown simulation type.")
            return 1
        df = []
        header = ""
        cwd = os.getcwd()
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concPercent in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,var,concPercent)
                            os.chdir(wd)
                            try:
                                if not header:
                                    data,header = getThermoStats("log.data")
                                    df.append(data)
                                else:
                                    data = getThermoStats("log.data")[0]
                                    df.append(data)
                            except:
                                pass
                            os.chdir(cwd)
        return pd.DataFrame(df,columns = header)

    def calcBulkModT(self,thermoDF = None):
        """
        This code takes a dataframe generated by getThermoStats and computes the bulk modulus of the values.
        """
        if type(thermoDF) == type(None):
            thermoDF = self.getData()
        thermoDf = thermoDF.sort_values("Volume Ave")
        P = list(thermoDF["Press Ave"])
        V = list(thermoDF["Volume Ave"])
        dP = list(thermoDF["Press Stdm"])
        dV = list(thermoDF["Volume Stdm"])
        dPdV,ddPdV ,nV = dForwDif(V,dV,P,dP)
        bM = [0.0]*len(nV)
        dbM = [0.0]*len(nV)
        dnV = [0.0]*len(nV)
        for i in range(len(dPdV)):
            bM[i] = -nV[i]*dPdV[i]
            dnV[i] = (1/2)*sqrt(dV[i+1]**2 + dV[i]**2)
            dbM[i] = abs(bM[i])*sqrt((ddPdV[i]/dPdV[i])**2 + (dnV[i]/nV[i])**2)
        return bM,dbM,nV,dnV

    def calcThermExp(self,thermoDF = None):
        if type(thermoDF) == type(None):
            thermoDF = self.getData()
        thermoDF = thermoDF.sort_values("Temp Ave")
        V = list(thermoDF["Volume Ave"])
        dV = list(thermoDF["Volume Stdm"])
        T = list(thermoDF["Temp Ave"])
        dT = list(thermoDF["Temp Stdm"])
        dVdT,ddVdT,nT = dForwDif(T,dT,V,dV)
        tE = [0.0]*len(nT)
        dtE = [0.0]*len(nT)
        dnT = [0.0]*len(nT)
        for i in range(len(nT)): # Note that here you need to make a choice for the volume at each point in nT (the midpoints between temperature values. I went with the left hand side volume.
            tE[i] = dVdT[i]/V[i]
            dnT[i] = (1/2)*sqrt(dT[i+1]**2 + dT[i]**2)
            dtE[i] = abs(dVdT[i])*sqrt((ddVdT[i]/dVdT[i])**2 + (dV[i]/V[i])**2)
        return tE,dtE,nT,dnT

    def calcHeatCapV(self,thermoDF = None):
        if type(thermoDF) == type(None):
            thermoDF = self.getData()
        thermoDf.sort_values("Temp Ave")
        T = list(thermoDF["Temp Ave"])
        dT = list(thermoDF["Temp Stdm"])
        E = list(thermoDF["Energy Ave"])
        dE = list(thermoDF["Energy Stdm"])
        dEdT,ddEdT,nT = dForwDif(T,dT,E,dE)
        dnT = list((1/2)*sqrt(dT[i+1]**2 + dT[i]**2) for i in range(len(dT) - 1))
        return dEdT,ddEdT,nT,dnT
    
    def simQPlot(self,logFile = "log.data"):
        if self.simType == "npt":
            vOrP = self.pressures
        elif self.simType == "nvt":
            vOrP = self.volumes
        else:
            print("Unknown simulation type.")
            return 1
        cwd = os.getcwd()
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concPercent in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,var,concPercent)
                            os.chdir(wd)
                            print("Time: %d, N: %d, T: %0.2f, %s: %0.4f, C: %d" %(time,size,temp,"P" if self.simType == "npt" else "V",var,concPercent*10))
                            qplot(logFile) # A function from utils which gives a 
                            os.chdir(cwd)
        return 
