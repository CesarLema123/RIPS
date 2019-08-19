# Please include the RIPS/lib/PyScripts in the PYTHONPATH variable before running this script

runOne = True

import sims
import csv
sim = sims.elastic(lammps = "lmp_mpi -in",systemSizes = [14,],temperatures = [300,1000,1500],inTemplate = "in.elasticTemplate",timeStep = 0.0005)
sim.setSimParams(lib = "$HOME/Research/git-RIPS/RIPS/lib",alloy = "custom", runTimes = [10,],concPercents = [x for x in range(0,101,10)])
if runOne:
	sim.setSimParams(temperatures = [300,1000,1500,2000],concPercents = [0,50,70,90,100])




# RUN THE SIMULATION

sim.runElasticSims()




# DATA COLLECTION SECTION

sim.setLogFile("log.output")
data,header = sim.getElasticData()
f = open("ElasticData.csv",mode = "w")
writer = csv.writer(f)
writer.writerow(header)
for row in data:
    writer.writerow(row)
f.close()
exit()
