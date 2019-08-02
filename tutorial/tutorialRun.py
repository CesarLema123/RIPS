import sims
import matplotlib.pyplot as plt
sim = sims.simulation()

length = [8*3.63*x/1000 for x in range(995,1006,1)]
sim.setSimParams(lib = "$HOME/git-RIPS/RIPS/lib",systemSizes = [8,],temperatures = [300,], lengths = length,simType = "nvt",fileName = "temp",inTemplate = "in.NVT",concPercents = [30,],lammps = "lmp_daily -in")

#sim.runSims()
#sim.cleanOutput()

#uncomment below to calculate Heat Capacity
#dEdT,ddEdT,nT,dnT = sim.calcHeatCapV()
#plt.errorbar(nT, dEdt, xerr = dnT, yerr = ddEdT, fmt = "o")

#uncomment below to calculate Thermal Expansion
#tE,dtE,nT,dnT = sim.calcThermoExp()
#plt.errorbar(nT, tE, xerr = dnT, yerr = dtE, fmt = "o")

#uncomment below to calculate Bulk Modulus


bM,dbM,nV,dnV = sim.calcBulkModT()
plt.errorbar(nV, bM, xerr = dnV, yerr = dbM, fmt = "o")


plt.show()
print("All Done")

