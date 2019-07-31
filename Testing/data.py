from utils import *
import numpy as np

var = "Temp"
#for f in ["log.drag",] + list("log.kT%d" %(n) for n in [100,1000,10000,100000]):
for i in range(3,7):
    df = readLog("log." + str(i))
    x = list(df[var])
    n = len(x)
    x = x[n//3:]
    a = sum(x)/len(x)
    s = np.sqrt(sum((a - y)**2 for y in x)/len(x))
    print("ave %0.4f std %0.4f" %(a,s))
