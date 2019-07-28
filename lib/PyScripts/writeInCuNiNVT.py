from random import randint
import os #subprocess # subprocess.run("string", shell = True)
import sys

TIMESTEP = 0.0001 # fs

READFILE = "in.Template"
DATAFILE = "data.CuNi"
WRITEFILE = "in.CuNi"
MY_PYTHON_LIB = '$HOME"/travis/lib/PyScripts"'


if len(sys.argv) > 1:
	_runTime,_numAtoms,_concInt,_temperature,_length = list(sys.argv[i+1] for i in range(5))
else:
	exit()
_runTime = float(_runTime)


simSteps = str(int(_runTime/TIMESTEP))



os.system("python " + MY_PYTHON_LIB + "/writeData.py " + _numAtoms + " " + _concInt)
reader = open(READFILE)
writer = open(WRITEFILE,mode="w")
writer.write("# --------------- Define Variables --------------\n")
writer.write("variable RUNTIME equal " + simSteps + "\n")
writer.write("variable TEMPERATURE equal " + _temperature + "\n")
writer.write("variable LENGTH equal " + _length + "\n")
writer.write("variable RANDOM equal " + str(randint(1000000,9999999)) + "\n\n")
for line in reader:
	writer.write(line)	
reader.close()
writer.close()
		

