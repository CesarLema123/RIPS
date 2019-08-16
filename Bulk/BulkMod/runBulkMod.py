import sims.py
systemSizes = [14,] # Run cubic simulations with this many atoms per side
temperatures = [1,] + [x for x in range(50,2001,50)] # Simulation temperatures
lengths = [3.6*14*x/1000 for x in range(995,1006)] # Side lengths of the simulation box
concPercents = [x for x in range(0,101,10)] # range of concentrations of Cu

sim = sims.bulkProp(lib = "$HOME/Research/git-RIPS/RIPS/",lammps = "lmp_mpi -in",runTimes = [10,],alloy = "custom",latticeConst = 3.6,temperatures = temperatures,systemSizes = systemSizes,lengths = lengths, pressures = [], concPercents = concPercents,timeStep = 0.0005,simType = "nvt",fileName = "bulkMod",potentialFile = "CuNi.eam.alloy",inTemplate = "in.NVT",copyDir = "./In",logFile = "log.run")


