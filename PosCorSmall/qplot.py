from py_scripts.plot import *



n = 0

df = readDump("dump.atom")
x,y,z,c = df["x"][63*n:63*(n+1)],df["y"][63*n:63*(n+1)],df["z"][63*n:63*(n+1)],df["id"][63*n:63*(n+1)]


position_plot(x,y,z)
