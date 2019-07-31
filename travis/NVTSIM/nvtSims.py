from sims import *
import matplotlib.pyplot as plt 

sim = simulation()

sim.setSimParams(_simType = "nvt",_runTimes = [1000,],_numAtoms = [6,],_temperatures = [2000,],_lengths = list(x*6 for x in [3.3,3.35,3.4,3.45,3.5,3.55,3.6,3.65,3.7,3.75,3.8]),_concInts = [3,],_lammps = "lammps.q",_inTemplate = "in.NVT",_pythonLib = "$HOME/RIPS/lib/PyScipts",_awkLib = "$HOME/RIPS/lib/AwkFiles")
#sim.cleanOutput()
df = sim.getData()
sim.recordData()
bM,dbM,V,dV = sim.calcBulkModT(thermoDF = df)
#plt.plot(V,bM,c="r")
plt.errorbar(V,bM,yerr = dbM,xerr = dV,fmt = "x",c="k",label = "Bulk Mod vs Volume at 2000K, 30% Ni 70% Cu, 864 atoms")
plt.xlabel("Volume cubic Angstroms",fontsize = 20)
plt.ylabel("Bulk Modulus",fontsize = 20)
plt.legend(fontsize = 20)
plt.show()
print("All Done")
exit()
