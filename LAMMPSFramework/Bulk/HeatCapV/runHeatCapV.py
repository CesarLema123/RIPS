import sims
import matplotlib.pyplot as plt

# Set simulation parameters as variables
systemSizes = [14,]
latticeConst = 3.6
temperatures = [1,] + [x for x in range(100,2001,100)]
lengths = [x*3.6*14/1000 for x in range(995,1006)]
concPercents = [0,50,70,90,100]
pressures = []

# Initialize the simulation with the variables above.
sim = sims.bulkProp(lib = "$HOME/Research/git-RIPS/RIPS/lib/",lammps = "lmp_mpi -in", runTimes = [100,],alloy = "custom",latticeConst = latticeConst,systemSizes = systemSizes,temperatures = temperatures,pressures = pressures,concPercents = concPercents,timeStep = 0.0005, simType ="nvt",fileName = "HCV", inTemplate = "in.NVT",copyDir = "./In")

# Run the simulations
sim.runBulkSims()
#sim.recordData("HCPData") record the thermodynamic variables

# calculating heat capacity at constant volume
hcv,dhcv,t,dt = sim.calcHeatCapV()

# Further post-processing can be specified here.
plt.errorbar(t,hcv,yerr = dhcv,xerr = dt,fmt = "x",c = "r")
plt.show()
