import numpy as np
import matplotlib.pyplot as plt

#collection of methods that analyze dataframe data
class LogAnalyzer:
    def __init__(self,dataframe):
        self.df = dataframe

    def generalPlot(self,X,Y,xlabel='',ylabel='',title=''):
        plt.plot(X,Y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        #plt.legend(loc='upper left')
        plt.grid()
        plt.show()
    
    def plotColumn(self,columnLabel):
        Y = self.df[columnLabel].values
        X = np.linspace(0,self.timestep*len(Y),len(Y))
        self.generalPlot(X,Y,'Runtime','Total Energy',)


# ---------------------------------------
# USAGE EXAMPLE

'''
LA = LogAnalyzer(df)
LA.plotColumn('TotEng')
'''
