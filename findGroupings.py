import csv
import numpy as np
import pandas as pd  #pandas removes the top row of the csv as its un important
from sys import argv

def main():

    arg1, arg2, arg3 = argv

    childResults = pd.read_csv(arg2).as_matrix()
    parentResults = pd.read_csv(arg3).as_matrix()
    

    ret = sortChildren(childResults[:,7:], parentResults[:,7:])
    print("Sorted innit :P")
    #work out how to print the results of sortChildren

#work out the Differences between the
def differenceSum(childCol, parentCol):
    return np.sum(np.square(np.subtract(parentCol, childCol)))


def sortChildren(childResults, parentResults):
    clen = len(childResults)
    plen = len(parentResults)
    print("\n plen is \n", plen)
    parentsChildren = []
    leftOvers = []
    comparisonTable = [[0 for x in range(plen)] for y in range(clen)]

    for i in range(clen):
        for j in range(plen):
            comparisonTable[i][j] = differenceSum(childResults[i], parentResults[j])

    print(comparisonTable)
    print("\n Comparison Table len is ", len(comparisonTable))
    print("\n Comparison Table 0 len is ", len(comparisonTable[0]))

if __name__ == "__main__":
    main()
