import numpy as np
import matplotlib.pyplot as plt

#collection of methods that analyze dataframe data
class DataFrameAnalyzer:
    def __init__(self,dataframe,timestep=1):
        self.df = dataframe
        self.timestep = timestep

    def generalPlot(self,X,Y,xlabel='',ylabel='',title='',fname='figure'):
        plt.plot(X,Y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        #plt.legend(loc='upper left')
        plt.grid()
        plt.savefig(fname, format='png')
        plt.clf()
    
    #plot a specific column of dataframe vs RunTime
    def plotColumnAgainstRT(self,columnLabel,fileName):
        Y = self.df[columnLabel].values.astype(float)
        X = np.linspace(0,self.timestep*len(Y),len(Y))
        self.generalPlot(X,Y,'Runtime',columnLabel,columnLabel+' vs. Runtime', fname = fileName)

    def concInterfaceEng(self):
        TE1 = self.df['TotEng1'].values.astype(float)
        TE2 = self.df['TotEng2'].values.astype(float)
        TEM = self.df['TotEngMix'].values.astype(float)
        midIndex = (len(TE1) - 1)//2
        numTerms = len(TE1[midIndex:])
        avgTE1 = np.sum(TE1[midIndex:])/numTerms
        avgTE2 = np.sum(TE2[midIndex:])/numTerms
        avgTEM = np.sum(TEM[midIndex:])/numTerms
        intEng = avgTEM - 0.5*(avgTE1 + avgTE2)
        return intEng


    '''
    def plotColumnVsColumn(self,firstLabel,secondLabel):

    def plotColumnVsAny(self,Label,X)
    # not too necessary, can use generalPlot method
    
    '''

    '''
    def spatialCorrelationFunction(self):

    def pairDistribuationFunction(self):
    
    '''

    '''
    #RETURN A LIST WITH VALUES, FOR A SPECIFIED DF COLUMN ,WHERE IT REMAINED RELATIVELY CONSTANT OVER A GOOD RUNTIME RANGE
    def getConstValueList(self,columnLabel):
        yData = np.array(self.df[columnLabel].tolist())   # GET COLUMN DATA AS TARGET NDARRAY

        binSize = yData.shape()


    # have to find a decent way to find max Error (and alittle, but its fine rn,the min Range value)
    def getConstValueList(df,columnLabel,maxError=2,minRange=10):
        #thermo data is outputedevrey timestepInterval
        
        yData = np.array(df[columnLabel].tolist()).astype(float)   # GET COLUMN DATA AS TARGET NDARRAY
        #plt.plot(yData)
        yGradient = np.gradient(yData)     # timestep is conserved
        plt.plot(yGradient[20:])
        yGGradient = np.gradient(yGradient)   # timestep is conserved
        plt.plot(yGGradient[20:])
        
        constValueRanges= []
        lowRange, uppRange = -1, -1    # -1 means var is not set
            
            
        for ind in range(yGGradient.shape[0]):
            #print(ind,' ',yGGradient[ind], " low: ",lowRange," upp: ",uppRange,' cond: ',(uppRange == -1) and abs(yGradient[ind]) < maxError)
            if lowRange != -1 and abs(yGGradient[ind]) < maxError:  # if lowRange is set, then can set uppRnge
                uppRange = ind
                if ind == (yGGradient.shape[0]-1):
                    constValueRanges.append([lowRange,uppRange])
            elif lowRange != -1 and uppRange != -1:
                if abs(uppRange-lowRange) > minRange and np.mean(yGradient[lowRange:uppRange])<maxError:
                    #print(ind,' ',yGradient[ind], " low: ",lowRange," upp: ",uppRange)
                    constValueRanges.append([lowRange,uppRange])
                lowRange = -1
                uppRange = -1
            
            
            if (uppRange == -1):       # if uppRange is not set then can set lowRange
                lowRange = ind

        return constValueRanges
        '''

    
    
# ---------------------------------------
# USAGE EXAMPLE

'''
LA = LogAnalyzer(df)
LA.plotColumn('TotEng')
'''
