from utils import *
import dataFileGenerator as dataF
import inFiles as inF
import numpy as np
import os
import csv
sh = os.system # I am running this on a bash terminal

   
class simulation:
    def __init__(self):
        self.pythonLib = "$HOME\"RIPS/lib/PyScripts\""
        self.awkLib = "$HOME\"/RIPS/lib/AwkFiles\""
        self.lammps = "lmp_daily -in"
        self.runTimes = [100,]
        self.alloy = "CuNi"
        self.latticeConst = 3.63
        self.numAtomTypes = 2
        self.numAtoms = [6,]
        self.temperatures = [300,]
        self.pressures = [0,]
        self.lengths = [21,]
        self.concInts = [[30,70],]
        self.timeStep = 0.0001
        self.simType = "npt"
        self.fileName = "CuNi"
        self.potentialFile = "CuNi.eam.alloy"
        self.inTemplate = "in.Template"
        return 

    def setSimParams(self,_pythonLib = "",_awkLib = "",_lammps = "",_alloy = "",_latticeConst = 0.0,_numAtomTypes = 0,_runTimes = [],_numAtoms = [],_temperatures = [],_pressures = [],_lengths = [],_concInts = [],_timeStep = 0.0,_simType = "",_fileName = "", _potentialFile = "",_inTemplate = ""):
        if _pythonLib:
            self.pythonLib = _pythonLib
        if _awkLib:
            self.awkLib = _awkLib
        if _lammps:
            self.lammps = _lammps
        if _alloy:
            self.alloy = _alloy
        if _latticeConst:
            self.latticeConst = _latticeConst
        if _numAtomTypes:
            self.numAtomTypes = _numAtomTypes
        if any(_runTimes):
            self.runTimes = _runTimes
        if any(_numAtoms):
            self.numAtoms = _numAtoms
        if any(_temperatures):
            self.temperatures = _temperatures
        if any(_pressures):
            self.pressures = _pressures
        if any(_lengths):
            self.lengths = _lengths
        if any(_concInts):
            self.concInts = _concInts
        if _timeStep:
            self.timeStep = _timeStep
        if _simType:
            self.simType = _simType
        if _inTemplate:
            self.inTemplate = _inTemplate
        if _fileName:
            self.fileName = _fileName
        if _potentialFile:
            self.potentialFile = _potentialFile
        return 0

    def getWorkDir(self,time,nAtoms,temp,pv,concInt):
        if self.simType == "npt":
            return "Out/RunTime"+str(time)+"NumAtoms"+str(nAtoms)+"ConcInt"+str(concInt)+"Temp"+str(temp)+"Press"+str(round(pv,2))
        elif self.simType == "nvt":
            return "Out/RunTime"+str(time)+"NumAtoms"+str(nAtoms)+"ConcInt"+str(concInt)+"Temp"+str(temp)+"Length"+str(round(pv,2))
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

    def writeData
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
            for nAtoms in self.numAtoms:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concInt in self.concInts:
                            wd = self.getWorkDir(time,nAtoms,temp,var,concInt)
                            sh("mkdir " + wd) 
                            self.cpTmp(wd)
                            os.chdir(wd)
                            # write the input file and the data file
                            inFile = inF.inFile(fileName = self.fileName, readFile = self.inTemplate,runTime = self.runTime,timeStep = self.timeStep)
                            inFile.writeInFile(options = ["TEMPERATURE equal " + str(temp),varString + " equal " +str(var),"RANDOM equal " + str(randint(1000000,9999999))])
                            dataFile = dataF.AtomDataFileGenerator(filename = self.fileName,latticeType = self.latticeType,alloy = self.alloy,latticeCosnt = self.latticeConst,systemSize = self.numAtoms, atomTypes = self.numAtomTypes, alloyCompPercent = concInt)
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
            for nAtoms in self.numAtoms:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concInt in self.concInts:
                            wd = self.getWorkDir(time,nAtoms,temp,var,concInt)
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
        return 0
    
    
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
        i = 0
        cwd = os.getcwd()
        for time in self.runTimes:
            for nAtoms in self.numAtoms:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concInt in self.concInts:
                            wd = self.getWorkDir(time,nAtoms,temp,var,concInt)
                            os.chdir(wd)
                            try:
                                if i == 0:
                                    data,header = getThermoStats("log.data")
                                    writer.writerow(header)
                                    writer.writerow(data)
                                    i = 1
                                else:
                                    data = getThermoStats("log.data")[0]
                                    writer.writerow(data)
                            except:
                                pass
                            os.chdir(cwd)
        w.close()
        return 0
    
     
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
        w = open(self.thermoDataFile,mode = "w")
        df = []
        i = 0
        cwd = os.getcwd()
        for time in self.runTimes:
            for nAtoms in self.numAtoms:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concInt in self.concInts:
                            wd = self.getWorkDir(time,nAtoms,temp,var,concInt)
                            os.chdir(wd)
                            try:
                                if i == 0:
                                    data,header = getThermoStats("log.data")
                                    df.append(data)
                                    i = 1
                                else:
                                    data = getThermoStats("log.data")[0]
                                    df.append(data)
                            except:
                                pass
                            os.chdir(cwd)
        w.close()
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
            thermoDF = self.getData(simType)
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
            for nAtoms in self.numAtoms:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concInt in self.concInts:
                            wd = self.getWorkDir(time,nAtoms,temp,var,concInt)
                            os.chdir(wd)
                            print("Time: %d, N: %d, T: %0.2f, %s: %0.4f, C: %d" %(time,nAtoms,temp,"P" if self.simType == "npt" else "V",var,concInt*10))
                            qplot(logFile) # A function from utils which gives a 
                            os.chdir(cwd)
        return 0
