#this import statement won't work since sims isn't in this folder
import sims

#why do you use a variable for this in the if statement, you never turn it into a FALSE under any of this code...
runOne = True 

#-----Instantiate variable values for the simulations here------------
systemSizes = [14,]
pressures = [x for x in range(-10000,10001,1000)]
temperatures = [1,] + [x for x in range(50,2001,50)]
concPercents = [x for x in range(0,101,10)]

#Again, no idea why this is here....? 
if runOne:
	systemSizes = [4,]
	pressures = [0,]
	temperatures = [300,]
	concPercents = [50,] 

#run diffusion simulations
sim = sims.diffusion(lib = "$HOME/Research/git-RIPS/RIPS/lib.PyScripts",lammps = "lmp_mpi -in", runTimes = [100,], alloy = "custom", latticeConst = 3.6, systemSizes = systemSizes,temperatures = temperatures, pressures = pressures, concPercents = concPercents, timeStep = 0.0005, fileName = "diffusion", inTemplate = "in.NPT",copyDir = "./In")

#sim.runDiffSims() #get rid of this?
#do post-processing to obtain diffusion coefficients
df = sim.getDiffCoeffs(saveFile = "diffCoeffs")
print(df.head()) #why only head?
