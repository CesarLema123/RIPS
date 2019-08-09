import sims
import csv


runOne = True


sim = sims.GrainBdry(lammps = "lmp_daily -in", runTimes = [10,],temperatures = [1,] + [x for x in range(100,1601,100)])
orientations = [[14,0,j,0,1,0,-j,0,14] for j in range(1,3)]
if runOne:
    orientations = [[14,0,1],[0,1,0],[-j,0,14]]
sim.setOrientations(orientations)
sim.runGBSims()

