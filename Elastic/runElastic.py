# Please include the RIPS/lib/PyScripts in the PYTHONPATH variable before running this script

import sims
import csv

# Specify the simulations parameters
systemSizes = [14,]
temperatures = [300,1000,1500]
concPercents = [x for x in range(0,101,10)]
latticeConst = 3.6
logFile = "log.output"

# Initialize the simulation 
sim = sims.elastic(lammps = "lmp_mpi -in",systemSizes = systemSizes,temperatures = temperatures,latticeConst = latticeConst,inTemplate = "in.elasticTemplate",timeStep = 0.0005)
sim.setSimParams(lib = "$HOME/Research/git-RIPS/RIPS/lib",alloy = "custom", runTimes = [100,],concPercents = concPercents,logFile = logFile)




# RUN THE SIMULATION

sim.runElasticSims()




# DATA COLLECTION SECTION

# Get a list of lists with the elastic coeffs. over range speficied above.
data,header = sim.getElasticData()

# Writing the data to a csv 
f = open("ElasticData.csv",mode = "w")
writer = csv.writer(f)
writer.writerow(header)
for row in data:
    writer.writerow(row)
f.close()
exit()
