import sims
sim = sims.simulation()
print(dir(sim))

sim.setSimParams(pythonLib = "/home/IPAMNET/tleadbetter/git-RIPS/RIPS/lib/PyScripts",awkLib = "/home/IPAMNET/tleadbetter/git-RIPS/RIPS/lib/AwkFiles",temperatures = list(x for x in range(100,101,100)),concPercents = [30,],pressures = [0,],lengths = [3.6*4,],runTimes = [100,],inTemplate = "in.NVT", alloy = "custom",latticeConst = 3.6,timeStep = 0.0001, simType = "nvt",systemSizes = [4,])

sim.runSims()
sim.cleanOutput()
y,dy,x,dx = sim.calcHeatCapV() #calcThermoExp() calcBulkModT()
plt.errorbar(x,y, yerr = dy,xerr = dx,fmt = "o")
plt.show()
print("All Done")

