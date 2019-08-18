import numpy as np
import matplotlib.pyplot as plt



# ------------------ INTERFACE TRACKING FUNCTIONS ------------------------------

def averageXPositionOfInterfaceAtoms(ptmData,centroData,xPositionData,CentroLimit = 3, groupAtomsMaxError = .7):
    '''
        Input are matrices of atoms per row and data per timestep in columns
        Centero close to 0 is an atom on a Perfect FCC structure
        
        '''
    # CONDITION TO FIND FCC ATOMS: ptmData == 1 and centroData < CentroLimit
    matIndOfPTMFCC = ptmData == 1              # Boolean matrix that satisfies condition
    matIndOfCentroFCC = centroData < 2         # Boolean matrix arrays that satisfies condition
    FCCMatrix = np.multiply(matIndOfPTMFCC,matIndOfCentroFCC).astype(int)   # Boolean matrix that satisfies both conditions
    
    '''
        #CONDITIONS TO FIND LIQUID ATOM: ptmData == 0 and centroData > centroLimit
        matIndOfPTMLiq = ptmData == 0
        matIndOfCentroLiq = centroData > 2
        liqMatrix = np.multiply(matIndOfPTMLiq,matIndOfCentroLiq).astype(int)      #matrix with 1 for liq AND 0 FCC
        '''
    
    # Atoms from FCC ARRA THAT ARE solid then turn to liquid once
    goodAtomsIndices = getAtomIndicesThatWereSolidThenTurnedLiqOnce(FCCMatrix) # Indices of FCC atoms that melt and stay liquid due to interface
    goodAtomsFCCMatrix = FCCMatrix[goodAtomsIndices]                           # Matrice with only FCC atoms that melt  and stay liquid
    
    return AverageAtomsWithSimilarPositions(xPositionData[goodAtomsIndices],groupAtomsMaxError)    # Average atom x position values with similar starting x positions



def getAtomIndicesThatWereSolidThenTurnedLiqOnce(data):    #atoms that were FCC then all of a suddent turned to liquids
    atomIndCollection = []
    for ind in range(data.shape[0]):    # this could probably be turned to a boolean index array
        melted = 0            # turned to liquid
        addThisAtom = False
        onlyOnePhaseChange = True  # changed from FCC TO liq and no more changes
        atomStartedFCC = (data[ind][0]==1)
        for FCCValue in data[ind]:
            if atomStartedFCC and FCCValue == 0:
                melted = 1
            if melted and FCCValue == 1:
                onlyOnePhaseChange = False
            if atomStartedFCC and melted and onlyOnePhaseChange:
                addThisAtom = True
            else:
                addThisAtom = False
        if addThisAtom:
            atomIndCollection.append(ind)
    return atomIndCollection


# AVERAGE ATOMS THAT BEGIN AS SOLID THEN TURN TO LIQUID AROUND THE SAME STARTING POSITION
def AverageAtomsWithSimilarPositions(data,maxError = .7):
    meanData = []  # each element is collection of arrays with similar starting value and will be mean when returned
    meanValues = []
    for atomInd in range(data.shape[0]):
        if len(meanValues) == 0:
            meanData.append([data[atomInd]])
            meanValues.append(data[atomInd][0])
        else:
            added = False
            for meanValInd in range(len(meanValues)):
                if data[atomInd][0] > (meanValues[meanValInd] - maxError) and data[atomInd][0] < (meanValues[meanValInd] + maxError):
                    meanValues[meanValInd] = np.mean([meanValues[meanValInd],data[atomInd][0]])
                    meanData[meanValInd].append(data[atomInd])
                    added = True
            if not added:
                meanData.append([data[atomInd]])
                meanValues.append(data[atomInd][0])
    #return np.array(meanValues)
    return np.array([np.mean(np.array(group),axis=0) for group in meanData])


def getInterfaceVelocity(ptmData,centroData,xPositionData,CentroLimit = 3, groupAtomsMaxError = .7):
    groupedAtomMeansFCC = averageXPositionOfInterfaceAtoms(ptmData,centroData,xPositionData,CentroLimit = 3, groupAtomsMaxError = .7)
    
    # for visualizations
    for vect in groupedAtomMeansFCC:
        plt.plot(vect)

    return np.mean(np.gradient(np.array([xPos[0] for xPos in groupedAtomMeansFCC])))

#------------------------------------------------------------------------------------



