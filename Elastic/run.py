# Please include the RIPS/lib/PyScripts in the PYTHONPATH variable before running this script

import sims
sim = sims.elastic(systemSizes = [14,],temperatures = [300,],inTemplate = "in.elasticTemplate",timeStep = 0.0005)
sim.setParams(lib = "$HOME/git-RIPS/RIPS/lib",alloy = "custom", runTimes = [10,])
sim.runElasticSims()

