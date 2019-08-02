def findDiff(fileName):
	"""
	This function calculates a diffusion coefficient given a log file from lammps.
	"""
	#import time and msd as vectors from specified sim
	t = list(thermoDF["Step"])       #CHANGE ACTUAL NAME
	msd = list(thermoDF["c_MSD[4]"]) #CHANGE ACTUAL NAME
	
	#compute Diffusion Coeff
	slope, intercept, r_value, p_value, std_err = stats.linregress(t, msd)
	DCoeff = slope/6 * 10**(-1)
	print('R-sq value: ', r_value, '\n', 'Diff Coeff (cmsq/s): ','{0:.15f}'.format(DCoeff))
  return DCoeff

def calcDiff(self,thermoDF = None):
	"""
	This code takes a dataframe generated by getData and computes the diffusion coefficient.
	"""
	if type(thermoDF) == type(None):
		thermoDF = self.getData()
		thermoDf = thermoDF.sort_values("Concentration") #CHANGE ACTUAL NAME
        
        
#create an array to store concentration vs. Diffusion Coeffient
result = np.zeros((11,2))
temp = 2000 #specifies constant temperature to look at. CHANGE TO DYNAMIC
for conc in range(11):
	logFile = "C" + str(conc) + "log.data"
	#store concentration as a percentage of Ni in first column #CHANGE TO JUST BE TWO LISTS/VECTORS
	result[conc,0] = conc*10 
	result[conc,1] = findDiff(logFile)
        
        return conc, diffu
