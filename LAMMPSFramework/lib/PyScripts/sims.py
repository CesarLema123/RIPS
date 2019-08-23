import utils
from random import randint
import dataFileGenerator as dataF
import inFiles as inF
import pandas as pd
from scipy.stats import linregress
import numpy as np
import os
import csv
sh = os.system # I am running this on a bash terminal. If running in windows, you will have to rewrite any sh() calls to the correct strings.

   
class simulation():
    """
    The simulation class is meant to hold all of the parameters one would vary across a lammps md simulation in the npt or nvt ensemble.
    It is also capable to running the simulations.
    lib: string - absolute path the the lib directory
    lammps: string - a string containing the system command to run lammps
    runTimes: list[int] - a list of runTimes to use in the simulations
    alloy: string - name of alloy to use preset lattice constants. Set to \"custom\" to specify your own lattice constant
    latticeConst: float
    numAtomTypes: int - number of atoms types in the simulation (only works with 1 or 2 right now)
    systemSizes: list[int] - a list of ints giving the number of unit lattice cells to use on each side (10 -> 4000 atoms in fcc)
    temperatures: list[float]
    pressures: list[float]
    lengths: list[float] - this is a list of lengths which correspond to the side of the cubic simulation cell (latConst*systemSize)
    concPercents: int - the percentage of atom 1 (Cu for all but GB and Ni for GB)
    timeStep: float
    simType: "nvt" or "npt" for Bulk and Diffusion, "" for rest
    fileName: string - The name of the data and in files to be written
    potentialFile: string - name of the potentialFile to be used.
    inTemplate: string -name of the in.*** lammps file to be copied during simulations
    copyDir: string - name of the directory containing the files to be copied to run a simulation (see one of the main directories for examples)
    logFile: string - name of the log file to read for data analysis
    """
    def __init__(self,lib = "$HOME/RIPS/lib/",lammps = "lmp_daily -in",runTimes = [100,],alloy = "CuNi",latticeConst = 3.6,latticeType = "FCC",numAtomTypes = 2,systemSizes = [6,],temperatures = [300,],pressures = [0,],lengths = [6*3.63,],concPercents = [30,],timeStep = 0.0001,simType = "npt",fileName = "CuNi",potentialFile = "CuNi.eam.alloy",inTemplate = "in.Template",copyDir = "./In",logFile = "log.run"):
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
        self.copyDir = copyDir
        self.logFile = logFile
        return 

    def setSimParams(self,lib = "",lammps = "",alloy = "",latticeConst = 0.0,latticeType = "",numAtomTypes = 0,runTimes = [],systemSizes = [],temperatures = [],pressures = [],lengths = [],concPercents = [],timeStep = 0.0,simType = "",fileName = "", potentialFile = "",inTemplate = "",copyDir = "",logFile = ""):
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
        if copyDir:
            self.copyDir = copyDir
        if logFile:
            self.logFile = logFile
        return 





    def cpTemplate(self,wd):
        """
        This function copies all of the files in copyDir to the working directory.
        """
        sh("cp " + self.copyDir + "/* " + wd)
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






class GrainBdry(simulation):
    """
    This class is meant to run simulations to get the energy due to an interface between two misaligned crystal structures for a range of temperatures and concentrations of CuNi
    See the simulation object for list of initialization vaiables.
   	"""
    def __init__(self,lib = "$HOME/RIPS/lib/",lammps = "lmp_daily -in",runTimes = [10,],alloy = "custom",latticeConst = 3.6,latticeType = "FCC",numAtomTypes = 2,systemSizes = [14,],temperatures = [1,]+[x for x in range(100,2501,100)],pressures = [0,],lengths = [],concPercents = [x for x in range(0,101,10)],orientations = [[1,0,0,0,1,0,0,0,1],],timeStep = 0.0005,simType = "",fileName = "grainBdry",potentialFile = "CuNi.eam.alloy",inTemplate = "in.grainBdryTemplate",copyDir = "./In"):
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
        self.orientations = orientations
        self.timeStep = timeStep
        self.simType = simType
        self.fileName = fileName
        self.potentialFile = potentialFile
        self.inTemplate = inTemplate
        self.copyDir = copyDir
        return 

    def setOrientations(self,orientations):
        """
        Change any of the lattice orientations in the simulations
        input- list(list(int*9)) [[x1,x2,x3,y1,y2,y3,z1,z2,z3],...] directions to point the lattice vectors (must be orthogonal)
        """
        self.orientations = orientations
        return

    

    def getWorkDir(self,time,size,temp,press,concPercent,orientation):
        """
        This function returns the path to the directory in which a simulation will be run.
        """
        o = orientation
        orientStr = "%d%d%d-%d%d%d-%d%d%d" %(o[0],o[1],o[2],o[3],o[4],o[5],o[6],o[7],o[8])
        return "Out/RunTime" + str(int(time)) + "Size" + str(int(size)) + "Temp" + str(int(temp)) + "Conc" + str(int(concPercent)) + "Press" + str(int(press)) + "Orient" + orientStr

    def runGBSims(self):
        """
        Run simulations to get the interfacial energy due to a misorientation between grains
        """
        cwd = os.getcwd()
        sh("mkdir Out")
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for press in self.pressures:
                        for conc in self.concPercents:
                            for orient in self.orientations:
                                wd = self.getWorkDir(time,size,temp,press,conc,orient)
                                sh("mkdir " + wd)
                                self.cpTemplate(wd)
                                os.chdir(wd)
                                nums = [3,1,2]
                                lets = ["x","y","z"]
                                o = ["%s%d equal %d" %(lets[i//3],nums[(i+1)%3],orient[i]) for i in range(9)]
                                inFile = inF.inFile(fileName = self.fileName,readFile = self.inTemplate,runTime=time,timeStep = self.timeStep)
                                inFile.writeInFile(options = ["TEMPERATURE equal " + str(temp),"PRESSURE equal " + str(press),"RANDOM equal " + str(randint(1000000,99999999)),"CONC equal " + str(conc),"A equal " + str(self.latticeConst),"SYSTEMSIZE equal " + str(size)] + o)
                                self.runLammps()
                                os.chdir(cwd)
        return

    def dataFile(self): # This override the simulation method becasue the grainbdry sim does not use a data file
        return




class elastic(simulation):
    """
    This class is meant to run simulations to get the elastic constants over a range of temperatures and 
    concentrations. See simulation object for initialization parameters
    """
    def __init__(self,lib = "$HOME/RIPS/lib/",lammps = "lmp_daily -in",runTimes = [1,],alloy = "CuNi",latticeConst = 3.6,latticeType = "FCC",numAtomTypes = 2,systemSizes = [14,],temperatures = [1,]+[x for x in range(100,2501,100)],pressures = [],lengths = [],concPercents = [x for x in range(0,101,10)],timeStep = 0.0005,simType = "",fileName = "elastic",potentialFile = "CuNi.eam.alloy",inTemplate = "in.elasticTemplate",copyDir = "./In",logFile = "log.run"):
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
        self.logFile = logFile
        self.potentialFile = potentialFile
        self.inTemplate = inTemplate
        self.copyDir = copyDir
        return 


    def getWorkDir(self,time,size,temp,concPercent):
        """
        This function returns the path to the directory in which a simulation will be run.
        """
        return "Out/RunTime" + str(int(time)) + "Size" + str(int(size)) + "Temp" + str(int(temp)) + "Conc" + str(int(concPercent))



    def runElasticSims(self):
        """
        Runs the simulations to get the elastic constants
        """
        cwd = os.getcwd()
        sh("mkdir Out")
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for conc in self.concPercents:
                        wd = self.getWorkDir(time,size,temp,conc)
                        sh("mkdir " + wd)
                        self.cpTemplate(wd)
                        os.chdir(wd)
                        inFile = inF.inFile(fileName = self.fileName,readFile = self.inTemplate,runTime=time,timeStep = self.timeStep)
                        inFile.writeInFile(options = ["TEMPERATURE equal " + str(temp),"RANDOM equal " + str(randint(1000000,99999999))])
                        dataFile = dataF.AtomDataFileGenerator(filename = self.fileName,latticeType = self.latticeType,alloy = self.alloy,customLatticeConst = self.latticeConst,systemSize = size, atomTypes = self.numAtomTypes, alloyCompPercent = conc)
                        dataFile.createDataFile()
                        self.runLammps()
                        os.chdir(cwd)
        return


    
    def getElasticConsts(self):
        """
        This function reads a logFile for the results of the simulations. It is very specific to the current
        print statements in in.elasticTemplate so please do not change those.
        """
        f = open(self.logFile)
        searchline = "print \"Bulk Modulus = $(v_bulkmodulus) +/- $(v_dbulkmodulus) ${cunits}\"\n"
        N = -1
        start = False
        values = []
        errors = []
        for line in f:
            if line == searchline:
                N = 1
            if ((N+1)%2):
                sline = line.split()
                if sline[0] == "Total":
                    pass
                else:
                    for i in range(len(sline)):
                        if sline[i] == "=":
                            x = float(sline[i+1])
                        elif sline[i] == "+/-":
                            y = float(sline[i+1])
                    values.append(x)
                    errors.append(y)
            if N > 0:
                N += 1
        f.close()
        return values,errors
    



    def getElasticData(self):
        """
        This function uses getElasticConsts to read the elastic data from all of the directories created by the simulation run and makes a data set with 
        all of the data.
        """
        cwd = os.getcwd()
        header = ["Run Time (ps)","N Atoms","Temperature (K)","Concentraition of Cu","Bulk Mod (GPa)","Shear Mod Aniso (GPa)","Shear Mod Iso (GPa)","Poisson","Youngs","Lames","P-Wave","Bulk Mod Error","Shear Mod Aniso Error","Shear Mod Iso Error","Poisson Error","Youngs Error","Lames Error","P-Wave Error"]
        data = []
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for conc in self.concPercents:
                        try:
                            d = [time,4*size**3,temp,conc]
                            wd = self.getWorkDir(time,size,temp,conc)
                            os.chdir(wd)
                            temporary=open(self.logFile)
                            temporary.close()
                            v,e = self.getElasticConsts()
                            data.append(d + v + e)
                        except:
                            pass
                        os.chdir(cwd)
        return data, header 




class bulkProp(simulation):
    """
    This class allows one to run simulations in NVT or NPT to compute the bulk properties of a material. See the simulation object for list of input parameters
    """
    def __init__(self,lib = "$HOME/RIPS/lib/",lammps = "lmp_daily -in",runTimes = [1,],alloy = "CuNi",latticeConst = 3.6,latticeType = "FCC",numAtomTypes = 2,systemSizes = [14,],temperatures = [1,]+[x for x in range(100,2501,100)],pressures = [0,],lengths = [14*3.6,],concPercents = [x for x in range(0,101,10)],timeStep = 0.0005,simType = "",fileName = "bulk",potentialFile = "CuNi.eam.alloy",inTemplate = "in.elasticTemplate",copyDir = "./In",logFile = "log.run"):
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
        self.logFile = logFile
        self.potentialFile = potentialFile
        self.inTemplate = inTemplate
        self.copyDir = copyDir
        return 


    def setBulkMod(self,latticeConst = ""):
        """
        Automatically set the simulation parameters to compute the bulk modulus give a lattice spacing.
        """
        if latticeConst:
            self.latticeConst = latticeConst
        self.legnths = [x/1000*self.latticeConst for x in range(995,1006)]
        self.temperatures = [1,] +  [x for x in range(100,2501,100)]
        self.concPercents = [x for x in range(0,100,10)]
        self.runTimes = [10,] # 10 ps chosen arbitrarily
        self.systemSizes = [10,] #4000 atoms chosen arbitrarily
        self.fileName = "BulkMod"
        self.inTemplate = "in.BulkMod"
        return

    def setHeatCap(self):
        """
        Automatically set the simulation parameters to compute the heat capacity.
        """
        return

    def setThermExp(self):
        """
        Automatically set the simulation parameters to compute the thermal expansion coefficient.
        """
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

    def runBulkSims(self):
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
    

##    def cleanOutput(self):
##        """
##        This function cleans up lammps output files so that they can be read by a read csv function and jmol.
##        """
##        volOrPress = self.getVolOrPress[0]
##        cwd = os.getcwd()
##        for time in self.runTimes:
##            for size in self.systemSizes:
##                for temp in self.temperatures:
##                    for var in volOrPress:
##                        for concPercent in self.concPercents:
##                            wd = self.getWorkDir(time,size,temp,var,concPercent)
##                            os.chdir(wd)
##                            sh("awk -f " + self.awkLib() + "/awkReadLog log.run > log.data") #Removes everything except for header and data from simulation log files
##                            try:
##                                sh("awk -f " + self.awkLib() + "/awkReadLog log.loop > log.temp") #Removes everything except for header and data from simulation log files
##                                sh("awk -f " + self.awkLib() + "/awkCombineLog log.temp > log.loop") # Removes the extra headers loop files
##                            except:
##                                pass
##                            sh("awk -f " + self.awkLib() + "/awkFixElementId dump.xyz > dump.pos") # Changes the names of the atoms in the dump files to Cu and Ni
##                            os.chdir(cwd)
##        return 
##    


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
                                    data,header = utils.getThermoStats1(self.logFile) # automatically uses log.data as this is the data file after cleanOutput is run
                                    #data,header = utils.getFinalStats(self.logFile)
                                    writer.writerow(header)
                                    writer.writerow(data)
                                else:
                                    data = utils.getThermoStats1(self.logFile)[0]
                                    #data = utils.getFinalStats(self.logFile)[0]
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
                            print("Changing to directory %s" %(wd))
                            os.chdir(wd)
                            try:
                                if not header:
                                    data,header = utils.getThermoStats1(self.logFile) # Used for reading variables defined in initConv.mod
                                    print("The header of the data is:")
                                    print(header)
                                    #data,header = utils.getFinalStats(self.logFile) # Use this when out is whole sim time average
                                    df.append(data)
                                    print("Line of Data")
                                    print(data)
                                else:
                                    data = utils.getThermoStats1(self.logFile)[0]
                                    #data = utils.getFinalStats(self.logFile)[0]
                                    df.append(data)
                                    print("Line of Data")
                                    print(data)
                            except:
                                pass
                            os.chdir(cwd)
                            print("Changing to directory %s" %(cwd)) 
        return pd.DataFrame(df,columns = header)

    def getForwDif(self,xString,yString):
        """
        This function computes the derivative of thermo variable B with respect to A
        using the forward difference method. A and B shoud be strings any of Volume Energy Press or Temp.
        The output are generated using utils.getThermoStats and utils.dForwDif and are:
        X - list of averages of independent variable in sims
        dX - the uncertainties in X
        Y - list of averages of dependent variable in sims
        dY - the uncertainties in Y
        dYdX - the derivative approximated by forward difference
        ddYdX - the uncertainty in ddYdX
        midX - the midpoint between the values in the X variable
        """
        thermoDF = self.getData()
        xSAve = xString+" ave"
        xSSTD = xString+" std"
        ySAve = yString+" ave"
        ySSTD = yString+" std"
        thermoDF = thermoDF.sort_values(xSAve)
        X = list(thermoDF[xSAve])
        dX = list(thermoDF[xSSTD]) 
        Y = list(thermoDF[ySAve])
        dY = list(thermoDF[ySSTD])
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
        bM = [-V[i]*dPdV[i] for i in range(len(dPdV))]
        dbM = [abs(bM[i])*np.sqrt((ddPdV[i]/dPdV[i])**2 + (dV[i]/V[i])**2) for i in range(len(bM))]
        return bM,dbM,V[:-1],dV[:-1]

    def calcThermExp(self):
        """
        This code takes a dataframe generated by utils.getThermoStats and computes the thermal expansion coeff of the values.
        """
        T,dT,V,dV,dVdT,ddVdT,midT = self.getForwDif("Temp","Volume")
        N = len(midT)
        tE = [dVdT[i]/V[i] for i in range(len(dVdT))]
        dtE = [abs(tE[i])*np.sqrt((ddVdT[i]/dVdT[i])**2 + (dV[i]/V[i])**2) for i in range(len(tE))]
        return tE,dtE,T[:-1],dT[:-1]

    def calcHeatCapV(self):
        """
        This code takes a dataframe generated by utils.getThermoStats and computes the heat capacity of the values for constant volume.
        """
        T,dT,E,dE,dEdT,ddEdT,midT = self.getForwDif("Temp","TotEng")
        dmidT = np.array((1/2)*sqrt(dT[i+1]**2 + dT[i]**2) for i in range(len(dT) - 1))
        return dEdT,ddEdT,T[:-1],dT[:-1]
    
    def calcHeatCapP(self):
       """
       This code takes a dataframe generated by utils.getThermoStats and computes the heat capacity of the values for constant pressure.
       """
       T,dT,H,dH,dHdT,ddHdT,midT = self.getForwDif("Temp","Enthalpy")
       dmidT = np.array((1/2)*sqrt(dT[i+1]**2 + dT[i]**2) for i in range(len(dT) - 1))
       return dHdT,ddHdT,T[:-1],dT[:-1]


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


class diffusion(simulation):
    """
    This class is designed to run simulations to compute a diffusion coefficient
    for a material at a range of concentrations, temperatures, and pressures in 
    an NPT ensembe.
    """
    def __init__(self,lib = "$HOME/RIPS/lib/",lammps = "lmp_daily -in",runTimes = [100,],alloy = "CuNi",latticeConst = 3.6,latticeType = "FCC",numAtomTypes = 2,systemSizes = [6,],temperatures = [300,],pressures = [0,],lengths = [6*3.63,],concPercents = [30,],timeStep = 0.0001,simType = "npt",fileName = "CuNi",potentialFile = "CuNi.eam.alloy",inTemplate = "in.Template",copyDir = "./In",logFile = "log.run"):
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
        self.copyDir = copyDir
        self.logFile = logFile
        return 

    def getWorkDir(self,time,size,temp,press,conc):
        """
        Get the name of the directory for the current simulation
        """
        runTime = str(int(time/self.timeStep))
        return "Out/RunTime" + runTime + "Size" + str(int(size)) + "Temp" +  str(int(temp)) + "Conc" + str(int(conc)) + "Press" + str(int(press))

    def runDiffSims(self):
        """
        Creates directories and runs the diffusion simulations
        """
        cwd = os.getcwd()
        sh("mkdir Out")
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for press in self.pressures:
                        for conc in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,press,conc)
                            sh("mkdir "+ wd)
                            self.cpTemplate(wd)
                            os.chdir(wd)
                            inFile = inF.inFile(fileName = self.fileName,readFile = self.inTemplate,runTime=time,timeStep = self.timeStep)
                            inFile.writeInFile(options = ["TEMPERATURE equal " + str(temp), "PRESSURE equal " + str(press),"RANDOM equal "  + str(randint(10000,9999999))])
                            dataFile = dataF.AtomDataFileGenerator(filename = self.fileName,latticeType = self.latticeType,alloy = self.alloy,customLatticeConst = self.latticeConst,systemSize = size, atomTypes =self.numAtomTypes,alloyCompPercent = conc)
                            dataFile.createDataFile()
                            self.runLammps()
                            os.chdir(cwd)
        return 

    def getDiffCoeffs(self,saveFile = None):
        """
        Go into each of the directories for the simulations and calculate the diffusion coefficient from the results
        """
        header = ["Simulation Time","System Size","Temperature (K)","Pressure (bar)","Concentration","Diffusion Coeff (cm" + u"\u00B2" + "s" + u"\u207B\u00B9" + ")","Standard Error of Diff Coeff.","r value of linear fit"]
        data = []
        cwd = os.getcwd()
        for time in self.runTimes:
            for size in self.systemSizes:
                for temp in self.temperatures:
                    for press in self.pressures:
                        for conc in self.concPercents:
                            wd = self.getWorkDir(time,size,temp,press,conc)
                            os.chdir(wd)
                            df = utils.readLog(self.logFile)
                            t = [x*self.timeStep for x in df["Step"]]
                            msd = list(df["c_MSD[4]"])
                            N = len(msd)
                            m,b,r,p,dm = linregress(t[N//10:],msd[N//10:]) # I choose to ignore the first 10% of the data
                            data.append([time,size,temp,press,conc,m/60,dm/60,r])
                            os.chdir(cwd)
        if not saveFile == None:
            f = open(saveFile,mode = "w")
            w = csv.writer(f)
            w.writerow(header)
            for row in data:
                w.writerow(r)
            f.close()
        return pd.DataFrame(data,columns = header)
		
