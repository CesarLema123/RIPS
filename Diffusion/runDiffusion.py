import sims

# Set simulation parameters as variables

systemSizes = [14,]
pressures = [x for x in range(-10000,10001,1000)]
temperatures = [1,] + [x for x in range(50,2001,50)]
concPercents = [x for x in range(0,101,10)]

# Initialize the simulation with the variables above.
sim = sims.diffusion(lib = "$HOME/Research/git-RIPS/RIPS/lib.PyScripts",lammps = "lmp_mpi -in", runTimes = [200,], alloy = "custom", latticeConst = 3.6, systemSizes = systemSizes,temperatures = temperatures, pressures = pressures, concPercents = concPercents, timeStep = 0.0005, fileName = "diffusion", inTemplate = "in.NPT",copyDir = "./In")


# Run the simulations
sim.runDiffSims()

# Get the diffusion coefficients from the simulations run above and store them as a pandas dataframe. 
df = sim.getDiffCoeffs(saveFile = "diffCoeffs")


# Further post-processing can be specified here.
print(df.head())
