import utils
import pandas as pd
from random import randint
import dataFileGenerator as dataF
import inFiles as inF
import numpy as np
import os
import csv
sh = os.system # I am running this on a bash terminal. If running in windows, you will have to rewrite any sh() calls to the correct strings.

   
class simulation():
    """
    The simulation class is meant to hold all of the parameters one would vary across a lammps md simulation in the npt or nvt ensemble.
    It is also capable to running the simulations.
    """
    def __init__(self,lib = "$HOME/RIPS/lib/",lammps = "lmp_daily -in",runTimes = [100,],alloy = "CuNi",latticeConst = 3.63,latticeType = "FCC",numAtomTypes = 2,systemSizes = [6,],temperatures = [300,],pressures = [0,],lengths = [6*3.63,],concPercents = [30,],timeStep = 0.0001,simType = "npt",fileName = "CuNi",potentialFile = "CuNi.eam.alloy",inTemplate = "in.Template"):
        self.lib = lib 
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

    def setSimParams(self,lib = "",lammps = "",alloy = "",latticeConst = 0.0,latticeType = "",numAtomTypes = 0,runTimes = [],systemSizes = [],temperatures = [],pressures = [],lengths = [],concPercents = [],timeStep = 0.0,simType = "",fileName = "", potentialFile = "",inTemplate = ""):
        """
        Change any of the initial parameters. Any unspecifies paramters are automatically unchanged.
        """
        if lib:
            self.lib = lib
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
        """
        This function writes the name of the directory in which the simulation will be run and output. 
        The naming is preference and can be changed.
        """
        if self.simType == "npt":
            return "Out/RunTime"+str(time)+"Size"+str(size)+"Conc"+str(concPercent)+"Temp"+str(temp)+"Press"+str(round(pv,2))
        elif self.simType == "nvt":
            return "Out/RunTime"+str(time)+"Size"+str(size)+"Conc"+str(concPercent)+"Temp"+str(temp)+"Length"+str(round(pv,2))
        else:
            print("Unknown sim type.")
            return 
    
    def cpTemplate(self,wd):
        """
        This function copies the inFile and potential file to the directory in which the simulation wil be run.
        """
        sh("cp " + self.inTemplate + " " + wd)
        sh("cp " + self.potentialFile + " " + wd)
        return 
    
   
    def inFile(self):
        """
        Returns the name of the lammps in file to be created and used in the simulations.
        """
        return "in." + self.fileName

    def dataFile(self):
        """
        Returns the name of the atom data file to be created and used in the simulations.
        """
        return "data." + self.fileName

    def pythonLib(self):
        """
        Returns the path to python library.
        """
        return self.lib+"/PyScripts"

    def awkLib(self): 
        """
        awk is a linux function for quick file reading and editing. It is used to make lammps output more easily readable. 
        See cleanOutput for more about specific awk files used.
        """
        return self.lib+"/AwkFiles"

    def runLammps(self):
        """
        Command line call to run lammps.
        """
        sh(self.lammps + " " + self.inFile())
        return 

    def getVolOrPress(self):
        """
        Returns either the list of lengths or pressures depending on the simulation type.
        """
        if self.simType == "npt":
            return self.pressures,"PRESSURE"
        elif self.simType == "nvt":
            return self.lengths,"LENGTH"
        else:
            print("Unknown simulation type")
            return

    def runSims(self):
        """
        This method runs the lammps simulations over the range of parameters specified in the object.
        """
        volOrPress,varString = self.getVolOrPress()
        cwd = os.getcwd()
        sh("mkdir Out") # Where the simulation directories will be stored for organizational purposes.
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for var in volOrPress:
                        for concPercent in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,var,concPercent)
                            sh("mkdir " + wd) 
                            self.cpTemplate(wd)
                            os.chdir(wd)
                            # write the input file and the data file
                            inFile = inF.inFile(fileName = self.fileName, readFile = self.inTemplate,runTime = time,timeStep = self.timeStep)
                            inFile.writeInFile(options = ["TEMPERATURE equal " + str(temp),varString + " equal " +str(var),"RANDOM equal " + str(randint(1000000,9999999))])
                            dataFile = dataF.AtomDataFileGenerator(filename = self.fileName,latticeType = self.latticeType,alloy = self.alloy,customLatticeConst = self.latticeConst,systemSize = size, atomTypes = self.numAtomTypes, alloyCompPercent = concPercent)
                            dataFile.createDataFile()
                            self.runLammps()
                            os.chdir(cwd)
        return 
    
    def cleanOutput(self):
        """
        This function cleans up lammps output files so that they can be read by a read csv function and jmol.
        """
        volOrPress = self.getVolOrPress()[0]
        cwd = os.getcwd()
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for var in volOrPress:
                        for concPercent in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,var,concPercent)
                            os.chdir(wd)
                            sh("awk -f " + self.awkLib() + "/awkReadLog log.run > log.data") #Removes everything except for header and data from simulation log files
                            try:
                                sh("awk -f " + self.awkLib() + "/awkReadLog log.loop > log.temp") #Removes everything except for header and data from simulation log files
                                sh("awk -f " + self.awkLib() + "/awkCombineLog log.temp > log.loop") # Removes the extra headers loop files
                            except:
                                pass
                            sh("awk -f " + self.awkLib() + "/awkFixElementId dump.xyz > dump.pos") # Changes the names of the atoms in the dump files to Cu and Ni
                            sh("rm -f log.run log.temp dump.xyz" + " " + self.potentialFile + " " + self.inTemplate) # delete extraneous files.
                            os.chdir(cwd)
        return 
    


    def recordData(self,thermoDataFile = "thermoData"):
        """
        Record the averanges, standard deviations, and standard deviations of the mean for the energy, temperature, pressure, and volume of each simualtion
        in the current directory in a file specified in the input. Defualt is thermoDataFile = \"thermoData\"
        """
        w = open(thermoDataFile,mode = "w")
        writer = csv.writer(w,delimiter = " ")
        volOrPress = self.getVolOrPress()[0]
        header = ""
        cwd = os.getcwd()
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for var in volOrPress:
                        for concPercent in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,var,concPercent)
                            os.chdir(wd)
                            try:
                                if not header:
                                    data,header = utils.getThermoStats("log.data") # automatically uses log.data as this is the data file after cleanOutput is run
                                    writer.writerow(header)
                                    writer.writerow(data)
                                else:
                                    data = utils.getThermoStats("log.data")[0]
                                    writer.writerow(data)
                            except:
                                pass
                            os.chdir(cwd)
        w.close()
        return 
    
     
    def getData(self):
        """
        Makes a pandas dataframeof the the averanges, standard deviations, and standard deviations of the mean for the
        energy, temperature, pressure, and volume of each simualtion.
        """
        volOrPress = self.getVolOrPress()[0]
        df = []
        header = ""
        cwd = os.getcwd()
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for var in volOrPress:
                        for concPercent in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,var,concPercent)
                            os.chdir(wd)
                            try:
                                if not header:
                                    data,header = utils.getThermoStats("log.data")
                                    df.append(data)
                                else:
                                    data = utils.getThermoStats("log.data")[0]
                                    df.append(data)
                            except:
                                pass
                            os.chdir(cwd)
        return pd.DataFrame(df,columns = header)

    def getForwDif(self,A,B):
        """
        This function computes the derivative of thermo variable Y with respect to X
        using the forward difference method. X and Y shoud be strings any of Volume Energy Press or Temp.
        The output are generated using utils.getThermoStats and utils.dForwDif and are:
        X - list of averages of independent variable in sims
        dX - the uncertainties in X
        Y - list of averages of dependent variable in sims
        dY - the uncertainties in Y
        dYdX - the derivative approximated by forward difference
        ddYdX - the uncertainty in ddYdX
        midX - the midpoint between the values in the X variable
        """
        #varDict = {"Energy": ["Energy Ave","Energy Std"],"Volume": ["Volume Ave","Volume Std"],"Press": ["Press Ave","Press Std"],"Temp":["Temp Ave","Temp Std"],"Enthalpy":["Enthalpy Ave","Enthalpy Std"]}
        thermoDF = self.getData()
        thermoDf = thermoDF.sort_values(A + " Ave")
        X = list(a for a in thermoDF[A + " Ave"])
        dX = list(a for a in thermoDF[A + " Std"])
        Y = list(a for a in thermoDF[B + " Ave"])
        dY = list(a for a in thermoDF[B + " Std"])
        dYdX,ddYdX,midX = utils.dForwDif(X,dX,Y,dY)
        return X,dX,Y,dY,dYdX,ddYdX,midX

    def calcBulkModT(self):
        """
        This code takes a dataframe generated by utils.getThermoStats and computes the bulk modulus of the values.
        """
        V,dV,P,dP,dPdV,ddPdV,midV = self.getForwDif("Volume","Press")
        N = len(midV)
        bM = np.zeros(N) #Initializing Bulk Modulus
        dbM = np.zeros(N)# Uncertainty in bM
        dmidV = np.zeros(N) # Uncertainty in midV
        for i in range(len(dPdV)):
            bM[i] = -midV[i]*dPdV[i]
            dmidV[i] = (1/2)*np.sqrt(dV[i+1]**2 + dV[i]**2)
            dbM[i] = abs(bM[i])*np.sqrt((ddPdV[i]/dPdV[i])**2 + (dmidV[i]/midV[i])**2)
        return bM,dbM,midV,dmidV

    def calcThermExp(self):
        """
        This code takes a dataframe generated by utils.getThermoStats and computes the thermal expansion coeff of the values.
        """
        T,dT,V,dV,dVdT,ddVdT,midT = self.getForwDif("Temp","Volume")
        N = len(midT)
        tE = np.zeros(N)
        dtE = np.zeros(N)
        dmidT = np.zeros(N)
        for i in range(len(midT)): # Note that here you need to make a choice for the volume at each point in nT (the midpoints between temperature values. I went with the left hand side volume.
            tE[i] = dVdT[i]/V[i]
            dmidT[i] = (1/2)*np.sqrt(dT[i+1]**2 + dT[i]**2)
            dtE[i] = abs(dVdT[i])*np.sqrt((ddVdT[i]/dVdT[i])**2 + (dV[i]/V[i])**2)
        return tE,dtE,midT,dmidT

    def calcHeatCapV(self):
        """
        This code takes a dataframe generated by utils.getThermoStats and computes the heat capacity of the values for constant volume.
        """
        T,dT,E,dE,dEdT,ddEdT,midT = self.getForwDif("Temp","Energy")
        dmidT = np.array((1/2)*sqrt(dT[i+1]**2 + dT[i]**2) for i in range(len(dT) - 1))
        return dEdT,ddEdT,midT,dmidT
    
    def simQPlot(self,logFile = "log.data"):
        """
        This function is meant for plotting lammps outputs from the log file over the range of simulations.
        """
        volOrPress = self.getVolOrPress()[0]
        cwd = os.getcwd()
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for var in volOrPress:
                        for concPercent in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,var,concPercent)
                            os.chdir(wd)
                            print("Time: %d, N: %d, T: %0.2f, %s: %0.4f, C: %d" %(time,size,temp,"P" if self.simType == "npt" else "V",var,concPercent*10))
                            qplot(logFile) # A function from utils which gives a 
                            os.chdir(cwd)
        return 
