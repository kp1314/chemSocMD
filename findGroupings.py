import csv
import numpy as np
import pandas as pd  #pandas removes the top row of the csv as its un important
from sys import argv

def main():

    arg1, arg2, arg3 = argv

    childResults = pd.read_csv(arg2).as_matrix()
    parentResults = pd.read_csv(arg3).as_matrix()

    ret = sortChildren(childResults, parentResults)
    print("Sorted innit :P")
    #work out how to print the results of sortChildren

#work out the Differences between the
def differenceSum(childCol, parentCol):
    np.sum(np.square(np.subtract(parentCol, childCol)))


def sortChildren(childResults, parentResults):
    clen = len(childResults)
    plen = len(parentResults)
    parentsChildren = []
    leftOvers = []
    comparisonTable = [[0 for x in range(plen)] for y in range(clen)]

    for i in range(7, clen):
        for j in range(7, plen):
            comparisonTable[i][j] = differenceSum(childResults[i], parentResults[j])

    print(comparisonTable)

if __name__ == "__main__":
    main()
