import sys

sys.path = ['/home/IPAMNET/tleadbetter/RIPS/lib/PyScripts',] + sys.path

from sims import *
import matplotlib.pyplot as plt 

sim = simulation()

sim.setSimParams(_runTimes = [1000,],_numAtoms = [8,],_temperatures = list(range(100,2001,100)),_pressures = [0,],_concInts = [3,],_lammps = "lmp_daily -in",_inTemplate = "in.Template",_pythonLib = "$HOME/RIPS/lib/PyScipts",_awkLib = "$HOME/RIPS/lib/AwkFiles")
#sim.cleanOutput()
df = sim.getData()
print(df)
sim.recordData()
tE,dtE,T,dT = sim.calcThermExp()
#plt.plot(V,bM,c="r")
plt.errorbar(T,tE,yerr = dtE,xerr = dT,fmt = "x",c="k",label = "Thermal Expansion Coeff. vs Temp at 0 bar, 30% Ni 70% Cu, 2048 atoms")
plt.xlabel("Temperature Kelvin",fontsize = 20)
plt.ylabel("Thermal Exapnsion Coeff",fontsize = 20)
plt.legend(fontsize = 20)
plt.show()
#sim.simQPlot(logFile = "log.loop")
print("All Done")
exit()
