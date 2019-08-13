import sims
import csv


runOne = True


sim = sims.GrainBdry(lammps = "lmp_daily -in", runTimes = [10,],systemSizes = [4,])
temperatures = [100,300,750,1000,1500]
concentrations = [0,70,90,100]
orientations = [[14,0,j,0,1,0,-j,0,14] for j in range(1,3)]
if runOne:
    orientations = [[14,0,1,0,1,0,-1,0,14],]
    temperatures = [300,]
    concentrations = [30,]
sim.setOrientations(orientations)
sim.setSimParams(temperatures = temperatures,concPercents = concentrations)
sim.runGBSims()

