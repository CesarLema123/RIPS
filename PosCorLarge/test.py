from py_scripts.utils import *

df = readDump("dump.atom")
df = df.sort_values("Time Step")

N = 3430 
n = len(df)
a = n//N

l = 34.72717 
hist1,bins1 = [],[]
for k in range(1,2):
    config = df.iloc[N*(a-k):N*(a-k+1),:]
    hist,bins = position_corrolation(config,l,l,l,10)
    if hist1 == []:
        hist1 = hist
        bins1 = bins
    else:
        for j in range(len(hist)):
            hist1[j] += hist[j]
for j in range(len(hist1)):
    hist1[j] = hist1[j]/(k)

print(hist1)
for j in range(len(bins1) -1):
    bins1[j] = (1/2)*(bins1[j] + bins1[j+1])
plt.plot(bins1[:-1],hist1)
plt.show()
