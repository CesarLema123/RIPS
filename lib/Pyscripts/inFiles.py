from randm import randomint

class inFile:
    def __init__(self,fileName = "CuNi",readFile = "in.Template",runTime = 1000,timeStep = 0.0001):
        self.fileName = fileName
        self.readFile = readFile
        self.runTime = runTime
        self.timeStep = timeStep
        return

    def setInFileParams(self,fileName = "",readFile = "",runTime = 0,timeStep = 0):
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
        return "data." + self.fileName
    
    def inFile(self):
        return "in." + self.fileName

    def writeInFile(self,options = ["TEMPERATURE equal 300","PRESSURE equal 0","RANDOM equal " + str(randint(1000000,9999999))]):
        reader = open(self.readFile)
        writer = open(self.inFile(),mode = "w")
        simSteps = str(int(self.runTime/self.timeStep))
        writer.write("# --------------- Define Variables --------------\n")
        writer.write("variable INFILE string " + self.inFile() + "\n")
        writer.write("variable DATAFILE string " + self.dataFile() + "\n")
        writer.write("variable RUNTIME equal " + simSteps + "\n")
        for opt in options:
            writer.write("variable " + opt)
        for line in reader:
            writer.write(line)    
        reader.close()
        writer.close()
        return
