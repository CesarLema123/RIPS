# Please include the RIPS/lib/PyScripts in the PYTHONPATH variable before running this script

runOne = True

import sims
sim = sims.elastic(lammps = "lammps.q",systemSizes = [14,],temperatures = [300,],inTemplate = "in.elasticTemplate",timeStep = 0.0005)
sim.setSimParams(lib = "$HOME/RIPS070819/RIPS/lib",alloy = "custom", runTimes = [10,])
if runOne:
	sim.setSimParams(concPercents = [30,])
sim.runElasticSims()

