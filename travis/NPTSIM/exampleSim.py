from sims import *

sim = simulation()

sim.setSimParams(_numAtoms = [4,],_runTimes = [100,],_temperatures = [2000,],_concInts = list(range(11)))
sim.runSims("npt")
a = sim.recordData("npt")
print(a)
