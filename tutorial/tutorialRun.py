import sys
import os
os.system("cd ../lib/PyScripts")
import sims
os.chdir("cd ../../tutorial")
sim = sims.simulation()

sim.setSimParams(pythonLib = "/home/IPAMNET/tleadbetter/git-RIPS/RIPS/lib/PyScripts",awkLib = "/home/IPAMNET/tleadbetter/git-RIPS/RIPS/lib/AwkFiles",temperatures = [300,],concPercents = [30,],pressures = [0,],runTimes = [100,],inTemplate = "in.NVT", alloy = "custom",timeStep = 0.005, simType = "nvt",systemSizes = [4,])

sim.runSims()
print("All Done")

