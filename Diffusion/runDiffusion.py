import sims

runOne = True 

systemSizes = [14,]
pressures = [x for x in range(-10000,10001,1000)]
temperatures = [1,] + [x for x in range(50,2001,50)]
concPercents = [x for x in range(0,101,10)]

if runOne:
	systemSizes = [4,]
	pressures = [0,]
	temperatures = [300,]
	concPercents = [50,] 

sim = sims.diffusion(lib = "$HOME/Research/git-RIPS/RIPS/lib.PyScripts",lammps = "lmp_mpi -in", runTimes = [100,], alloy = "custom", latticeConst = 3.6, systemSizes = systemSizes,temperatures = temperatures, pressures = pressures, concPercents = concPercents, timeStep = 0.0005, fileName = "diffusion", inTemplate = "in.NPT",copyDir = "./In")

#sim.runDiffSims()
df = sim.getDiffCoeffs(saveFile = "diffCoeffs")
print(df.head())
