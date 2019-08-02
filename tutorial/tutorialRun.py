import sims
sim = sims.simulation()
print(dir(sim))

sim.setSimParams(lib = "/home/IPAMNET/tleadbetter/git-RIPS/RIPS/lib",temperatures = list(x for x in range(100,101,100)),concPercents = [30,],pressures = [0,],lengths = [3.6*4,],runTimes = [100,],inTemplate = "in.NVT", alloy = "custom",latticeConst = 3.6,timeStep = 0.0001, simType = "nvt",systemSizes = [4,])

sim.runSims()
sim.cleanOutput()

#uncomment below to calculate Heat Capacity
#dEdT,ddEdT,nT,dnT = sim.calcHeatCapV()
#plt.errorbar(nT, dEdt, xerr = dnT, yerr = ddEdT, fmt = "o")

#uncomment below to calculate Thermal Expansion
#tE,dtE,nT,dnT = sim.calcThermoExp()
#plt.errorbar(nT, tE, xerr = dnT, yerr = dtE, fmt = "o")

#uncomment below to calculate Bulk Modulus
length = [4*x in range(3.55,3.66,0.01)]
sim.setSimParams(lib = "/home/IPAMNET/tleadbetter/git-RIPS/RIPS/lib",temperatures = [900,],concPercents = [30,],pressures = [0,],lengths = length,runTimes = [100,],inTemplate = "in.NVT", alloy = "custom",latticeConst = 3.6,timeStep = 0.0001, simType = "nvt",systemSizes = [4,])
bM,dbM,nV,dnV = sim.calcBulkModT()
plt.errorbar(nV, bM, xerr = dnV, yerr = dbM, fmt = "o")


plt.show()
print("All Done")

