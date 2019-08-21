import sims
import csv


temperatures = [300,]
concPercents = [50,]
systemSizes = [14,]
orientations = [[14,0,j,0,1,0,-j,0,14] for j in range(1,15,1)]
latticeConst = 3.6

sim = sims.GrainBdry(lammps = "lmp_mpi -in", runTimes = [100,],systemSizes = systemSizes,concPercents = concPercents,temperatures = temperatures,latticeConst = latticeConst)
sim.setOrientations(orientations)
sim.runGBSims()

