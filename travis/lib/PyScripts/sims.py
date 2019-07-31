from utils import *
from lammpsWriteFiles import *
import os
import csv
sh = os.system # I am running this on a bash terminal
    
    
class simulation:
    def __init__(self):
    self.MY_PYTHON_LIB = ""
    self.MY_AWK_LIB = ""
    self.lammps = ""
    self.runTimes = []
    self.numAtoms = []
    self.temperatures = []
    self.pressures = []
    self.lengths = []
    self.concInts = []
    self.timeStep = 0.0
    self.inFile = ""
    self.dataFile = ""
    self.writeFile = ""
    self.themoDataFile = ""
    self.potentialFile = ""
    return 0

    def setSimParams(self,_pythonLib = "",_awkLib = "",_lammps = "",_runTimes = [],_numAtoms = [],_temperatures = [],_pressures = [],_lengths = [],_timeStep = 0.0,_inFile = "",_dataFile = "",_writeFile = "" , _potentialFile = "",_thermoDataFile = ""):
        if _pythonLib:
            self.MY_PYTHON_LIB = _pythonLib
        if _awkLib:
            self.MY_AWK_LIB = _awkLib
        if _lammps:
            self.lammps = _lammps
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
        if _timeStep:
            self.timeStep = _timeStep
        if _inFile:
            self.inFile = _inFile
        if _dataFile:
            self.dataFile = _dataFile
        if _writeFile:
            self.writeFile = _writeFile
        if _potentialFile:
            self.potentialFile = _potentialFile
        if _thermoDataFile:
            self.thermoDataFile = _thermoDataFile
        return 0

    def getWorkDir(simType,time,nAtoms,temp,pv,concInt):
        if simType = "npt":
            return "/Out/RunTime"+str(time)+"NumAtoms"+str(nAtoms)+"ConcInt"+str(concInt)+"Temp"+str(temp)+"Press"+str(pv)
        elif simType = "nvt":
            return "/Out/RunTime"+str(time)+"NumAtoms"+str(nAtoms)+"ConcInt"+str(concInt)+"Temp"+str(temp)+"Length"+str(pv)
        else:
            print("Unknown sim type.")
            return 1
    
    def cpTmp(self,wd):
        sh("cp " + self.inFile + " " + wd)
        sh("cp " + self.potentialFile + " " + wd)
        return 0
    
    def runLammps(self):
        sh(self.lammps + " " + self.inFile)
        return 0
    
    def runSims(self,simType):
        cwd = os.getcwd()
        for time in self.runTimes:
            for nAtoms in self.numAtoms:
                for temp in self.temperatures:
                    if simType == "npt":
                        for press in self.pressures:
                            for concInt in concInts:
                                wd = getWorkDir("npt",time,nAtoms,temp,press,concInt)
                                sh("mkdir ." + wd) 
                                self.cpTmp(wd)
                                os.chdir(wd)
                                # write the input file and the data file
                                writeInNPT(runTime = time,timeStep = timeStep,temp = temp,press = press)
                                writeDataFile(initTemp = 0,nAtoms = [nAtoms,nAtoms,nAtoms],concFunc = lambda a: 1 if a < concInt/100 else 2) 
                                self.runLammps()
                                os.chdir(cwd)
                    elif simType == "nvt":
                        for length in self.lengths:
                            for concInt in concInts:
                                wd = getWorkDir("nvt",time,nAtoms,temp,length,concInt)
                                sh("mkdir ." + wd) 
                                self.cpTmp(wd)
                                os.chdir(wd)
                                # write the input file and the data file
                                writeInNVT(runTime = time,timeStep = timeStep,temp = temp,length = length)
                                writeDataFile(initTemp = 0,nAtoms = [nAtoms,nAtoms,nAtoms],concFunc = lambda a: 1 if a < concInt/100 else 2) 
                                self.runLammps()
                                os.chdir(cwd)
                    else:
                        print("Unknown simulation type.")
                        return 1
        return 0
    
    def cleanOutput(self,simType):
        if simType == "npt":
            vOrp = self.pressures
        elif simType == "nvt":
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
                            wd = getWorkDir(simType,time,nAtoms,temp,var,concInt)
                            os.chdir(wd)
                            sh("awk -f " + self.MY_AWK_LIB + "/awkReadLog log.run > log.data")
                            sh("awk -f " + self.MY_AWK_LIB + "/awkReadLog log.loop > log.temp")
                            sh("awk -f " + self.MY_AWK_LIB + "/awkCombineLog log.temp > log.loop")
                            sh("awk -f " + self.MY_AWK_LIB + "/awkFixElementId dump.xyz > dump.pos")
                            sh("rm -f log.run log.temp dump.xyz in.Template CuNi.eam.alloy")
                            os.chdir(cwd)
        return 0
    
    
    def recordData(self,simType):
        if simType == "npt":
            vOrP = self.pressures
        elif simType == "nvt":
            vOrP = self.lengths
        else:
            print("Unknown simulation type.")
            return 1
        w = open(self.thermoDataFile,mode = "w")
        writer = csv.writer(w,delimeter = " ")
        i = 0
        cwd = os.getcwd()
        for time in self.runTimes:
            for nAtoms in self.numAtoms:
                for temp in self.temperatures:
                    for var in vOrP:
                        for concInt in self.concInts:
                            wp = getWorkDir(simType,time,nAtoms,temp,var,concInt)
                            os.chdir(wd)
                            if i == 0:
                                data,header = getThermoStats("log.data")
                                writer.writerow(header)
                                writer.writerow(data)
                                i = 1
                            else:
                                data = getThermoStats("log.data")[0]
                                writer.writerow(data)
                            os.chdir(cwd)
        w.close()
        return 0
