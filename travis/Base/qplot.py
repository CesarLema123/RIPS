import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as stats


logFile = "log.loop"


d = pd.read_csv(logFile,sep="\s+")
var = "v_pressSTD"
time = list(0.1*step for step in d["Step"])
Y = list(d[var])

plt.title("%s vs Time" %(var),fontsize = 28)
plt.xlabel("Time (fs)",fontsize = 24)
plt.ylabel("%s" %(var), fontsize = 24)
plt.plot(time,Y)
plt.show()





