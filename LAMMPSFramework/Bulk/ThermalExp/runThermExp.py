import sims
import matplotlib.pyplot as plt


# Set simulation parameters as variables
latticeConst = 3.6
systemSizes = [15,]
lengths = [x*3.6*15/1000 for x in range(995,1006)]
temperatures = [300,]
concPercents = [50,]

# Initialize the simulation with the variables above.
sim = sims.bulkProp(lib = "$HOME/git-RIPS/RIPS/lib/PyScripts",lammps = "lmp_mpi -in",runTimes = [1000,],alloy = "custom",latticeConst = latticeConst,numAtomTypes = 2,systemSizes = systemSizes,temperatures = temperatures,pressures = [],lengths = lengths,concPercents = concPercents,timeStep = 0.0001,simType = "nvt",fileName = "thermExp",potentialFile ="CuNi.eam.alloy",inTemplate = "in.NVT",copyDir = "./In",logFile="log.run")

# Run the simulations
sim.runBulkSims()

# Calculating the coefficient of thermal expansion
TEC,dTEC,T,dT = sim.calcThermExp()


# Further post-processing can be specified here.
plt.errorbar(T,TEC,yerr = dTEC,xerr=dT,c="r",fmt="x",label = "Thermal Expansion Coeff. vs Temperature")
plt.xlabel("Temperature (K)")
plt.ylabel("Thermal Expansion Coeff. (1/K)")
plt.legend()
plt.show()
