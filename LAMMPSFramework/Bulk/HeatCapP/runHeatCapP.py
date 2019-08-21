import sims
import matplotlib.pyplot as plt

# Set simulation parameters as variables
systemSizes = [14,]
temperatures = [1,] + [x for x in range(100,2001,100)]
pressures = [0,]
concPercents = [0,50,70,90,100]

# Initialize the simulation with the variables above.
sim = sims.bulkProp(lib = "$HOME/Research/git-RIPS/RIPS/lib/",lammps = "lmp_mpi -in", runTimes = [10,],alloy = "custom",latticeConst = 3.6,systemSizes = systemSizes,temperatures = temperatures,pressures = pressures,concPercents = concPercents,timeStep = 0.0005, simType ="npt",fileName = "HCP", inTemplate = "in.NPT",copyDir = "./In")

# Run the simulations
sim.runBulkSims()

#sim.recordData("HCPData") record the thermodynamic variables

# calculating the heat capacity
hcp,dhcp,t,dt = sim.calcHeatCapP()


# Further post-processing can be specified here.
plt.errorbar(t,hcp,yerr = dhcp,xerr = dt,fmt = "x",c = "r")
plt.show()
