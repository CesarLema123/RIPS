# Please include the RIPS/lib/PyScripts in the PYTHONPATH variable before running this script

runOne = False

import sims
import csv
sim = sims.elastic(lammps = "lammps.q",systemSizes = [14,],temperatures = [300,1000,1500],inTemplate = "in.elasticTemplate",timeStep = 0.0005)
sim.setSimParams(lib = "$HOME/RIPS070819/RIPS/lib",alloy = "custom", runTimes = [10,],concPercents = [x for x in range(0,101,10)])
if runOne:
	sim.setSimParams(concPercents = [30,])



# RUN THE SIMULATION

#sim.runElasticSims()




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
