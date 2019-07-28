import numpy as np
import matplotlib.pyplot as plt

#collection of methods that analyze dataframe data
class LogAnalyzer:
    def __init__(self,dataframe,timestep=1):
        self.df = dataframe
        self.timestep = timestep

    def generalPlot(self,X,Y,xlabel='',ylabel='',title=''):
        plt.plot(X,Y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        #plt.legend(loc='upper left')
        plt.grid()
        plt.show()
    
    #plot a specific column of dataframe vs RunTime
    def plotColumnAgainstRT(self,columnLabel):
        Y = self.df[columnLabel].values.astype(float)
        X = np.linspace(0,self.timestep*len(Y),len(Y))
        self.generalPlot(X,Y,'Runtime',columnLabel,columnLabel+' vs. Runtime')

    '''
    def plotColumnVsColumn(self,firstLabel,secondLabel):

    def plotColumnVsAny(self,Label,X)
    # not too necessary, can use generalPlot method
    
    '''





# ---------------------------------------
# USAGE EXAMPLE

'''
LA = LogAnalyzer(df)
LA.plotColumn('TotEng')
'''
