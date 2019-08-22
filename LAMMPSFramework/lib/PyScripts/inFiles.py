from random import randint

class inFile:
    """
    fileName: Name of the file to be written
    readFile: Name of the template in.*** file to read
    runTime: Desired runtime of the simulation in simulation units
    timeStep: Desired timestep in simulation units
    """
    def __init__(self,fileName = "CuNi",readFile = "in.Template",runTime = 1000,timeStep = 0.0001):
        self.fileName = fileName
        self.readFile = readFile
        self.runTime = runTime
        self.timeStep = timeStep
        return

    def setInFileParams(self,fileName = "",readFile = "",runTime = 0,timeStep = 0):
        """
        Change any of the initial file parameters
        """
        if fileName:
            self.fileName = fileName
        if readFile:
            self.readFile = readFile
        if runTime:
            self.runTime = runTime
        if timeStep:
            self.timeStep = timeStep
        return
    
    def dataFile(self):
        """
        None
        Returns the name of the data file to be written
        """
        return "data." + self.fileName
    
    def inFile(self):
        """
        None
        Returns the name of the in file to be written
        """
        return "in." + self.fileName

    def writeInFile(self,options = ["TEMPERATURE equal 300","PRESSURE equal 0","RANDOM equal " + str(randint(1000000,9999999))]):
        """
        This function writes the given simulation parameters to the top of the template in file.
        options: a a list of strings in the form \"VARIABLENAME lammpsvariable-type vaule\"
        """
        reader = open(self.readFile)
        writer = open(self.inFile(),mode = "w")
        simSteps = str(int(self.runTime/self.timeStep))
        writer.write("# --------------- Define Variables --------------\n")
        writer.write("variable INFILE string " + self.inFile() + "\n")
        writer.write("variable DATAFILE string " + self.dataFile() + "\n")
        writer.write("variable RUNTIME equal " + simSteps + "\n")
        writer.write("variable TIMESTEP equal " + str(self.timeStep)+"\n")
        for opt in options:
            writer.write("variable " + opt + "\n")
        for line in reader:
            writer.write(line)    
        reader.close()
        writer.close()
        return
