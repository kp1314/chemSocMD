import csv
import numpy as np
import pandas as pd  #pandas removes the top row of the csv as its un important
from sys import argv

def main():

    arg1, arg2, arg3 = argv

    childResults = pd.read_csv(arg2).as_matrix()
    parentResults = pd.read_csv(arg3).as_matrix()

    ret = sortChildren(childResults[:,7:], parentResults[:,7:])

    i=0
    for x in ret:
        print('parent %s has children %s\n' %(i, x))
        i= i + 1

    #work out how to print the results of sortChildren

# finds position of parent with minimum difference in comparison table
# can't be a parent that has better matches  and is full
def bestParentIndex(differences):
    currMinPos = 0
    for i in range(len(differences)):
        if differences[i] != -1 and differences[i] < differences[currMinPos]:
                currMinPos = i
    return currMinPos

# returns index of max child in a parent's children list
def maxInd(comparisonTable, indexes, parentIndex):
    maxInd = -1

    for i in range(3):
        if (comparisonTable[indexes[i]][parentIndex] > maxInd):
            maxInd = i

    return maxInd

# work out the Differences between the children and parents
# could change this to another measure
def differenceSum(childCol, parentCol):
    return np.sum(np.square(np.subtract(parentCol, childCol)))

def sortChildren(childResults, parentResults):
    clen = len(childResults)
    plen = len(parentResults)
    parentsChildren = [[] for x in range(plen)]
    availableChildren = [x for x in range(clen)]
    comparisonTable = [[0 for x in range(plen)] for y in range(clen)]

    #each child's list of differences is a rown in comptab
    for i in range(clen):
        for j in range(plen):
            comparisonTable[i][j] = differenceSum(childResults[i], parentResults[j])

    endOfChildren = len(availableChildren)
    while len(availableChildren) >= 3:


        while endOfChildren > 0:
            childInd = availableChildren[0]
            hasParent = False

            while hasParent == False:
                bestIndex = bestParentIndex(comparisonTable[childInd])
                newParent = parentsChildren[bestIndex]
                currentDiff = comparisonTable[childInd][bestIndex]

                if len(parentsChildren[bestIndex]) == 3:
                    maxChildPos = maxInd(comparisonTable, newParent, bestIndex)
                    maxChild = newParent[maxChildPos]
                    if currentDiff > comparisonTable[maxChild][bestIndex]:
                        comparisonTable[childInd][bestIndex] = -1
                    else:
                        parentsChildren[bestIndex][maxChildPos] = childInd
                        comparisonTable[maxChild][bestIndex] = -1
                        availableChildren = availableChildren + [maxChild]
                        del availableChildren[0]
                        hasParent = True
                else:
                    parentsChildren[bestIndex] = parentsChildren[bestIndex] + [childInd]
                    del availableChildren[0]
                    i=i-1
                    endOfChildren = endOfChildren - 1
                    hasParent = True
    return parentsChildren



if __name__ == "__main__":
    main()
