import sims

runOne = True

systemSizes = [14,]
temperatures = [1,] + [x for x in range(100,2001,100)]
pressures = [0,]
concPercents = [0,50,70,90,100]

if runOne:
    systemSizes = [4,]
    temperatures = [300,]
    pressures = [0,]
    concPercents = [50,]





sim = sims.bulkProp(lib = "$HOME/Research/git-RIPS/RIPS/lib/",lammps = "lmp_mpi -in", runTimes = [10,],alloy = "custom",latticeConst = 3.6,systemSizes = systemSizes,temperatures = temperatures,pressures = pressures,concPercents = concPercents,timeStep = 0.0005, simType ="npt",fileName = "HCP", inTemplate = "in.NPT",copyDir = "./In")

sim.runBulkSims()
sim.recordData("HCPData")
sim.calcHeatCapP()

