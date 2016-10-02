import csv
import numpy as np
import pandas as pd  #pandas removes the top row of the csv as its un important
from sys import argv

def main():

    arg1, arg2, arg3 = argv

    childResults = pd.read_csv(arg2).as_matrix()
    parentResults = pd.read_csv(arg3).as_matrix()
    parentUsers = parentResults[:,3]
    coParentUsers = parentResults[:,4]
    ancillary = parentResults[:,5]
    childAncillarys = childResults[:,3]
    coParents = [-1 for i in range(len(parentUsers))]

    for i in range(len(parentUsers)):
        comp = parentUsers[i]
        for j in range(len(coParentUsers)):
            co = coParentUsers[j]
            if ("".join(co.split())).lower() == ("".join(comp.split())).lower():
                coParents[i] = j
                break

    joinedAncillarys = [[ancillary[i],ancillary[coParents[i]]] for i in range(len(ancillary))]

    # assumes all parents have one co-parent
    ret = sortChildren(childResults[:,4:], parentResults[:,7:], joinedAncillarys, childAncillarys)

    printedCoparents = []
    data = []

    for i in range(len(ret)):
        if i not in printedCoparents:
            couple = [parentResults[:,1][i] + " - " + parentResults[:,5][i] + " and " + parentResults[:,1][coParents[i]] + " - " + parentResults[:,5][coParents[i]]]
            for j in range(len(ret[i])):
                newKid = childResults[:,1][ret[i][j]] + " - " + ("".join(childResults[:,2][ret[i][j]].split())).lower() + " - " + ("".join(childResults[:,3][ret[i][j]].split())).lower()
                couple.append(newKid)
            for j in range(len(ret[coParents[i]])):
                newKid = childResults[:,1][ret[coParents[i]][j]] + " - " + ("".join(childResults[:,2][ret[coParents[i]][j]].split())).lower() + " - " + ("".join(childResults[:,3][ret[coParents[i]][j]].split())).lower()
                couple.append(newKid)
            data.append(couple)
            printedCoparents.append(coParents[i])


    f = open("daveOut.csv", "w", newline='')
    out = csv.writer(f,dialect='excel')

    for i in range(len(data)):
         print("%s\n" %(data[i]))

    out.writerows(data)


# finds position of parent with minimum difference in comparison table
# can't be a parent that has better matches and is full
# can't all be -1 as rejects are dealt with before call to function
def bestParentIndex(differences):
    numdiff = len(differences)
    i = 0

    while i < numdiff:
        if differences[i] != -1:
            break
        i = i + 1

    j = i + 1
    while j < numdiff:
        if differences[j] != -1 and differences[j] < differences[i]:
            i = j
        j = j + 1

    return i

# returns index of max child in a parent's children list
def maxInd(comparisonTable, indexes, parentIndex):
    maxInd = -1

    for i in range(len(indexes)):
        if (comparisonTable[indexes[i]][parentIndex] > maxInd):
            maxInd = i

    return maxInd

# work out the Differences between the children and parents
# could change this to another measure
def differenceSum(childCol, parentCol):
    return np.sum(np.square(np.subtract(parentCol, childCol)))

def sortChildren(childResults, parentResults, parentAncillarys, childAncillarys):
    clen = len(childResults)
    plen = len(parentResults)

    comparisonTable = [[0 for x in range(plen)] for y in range(clen)]

    availableChildren = [x for x in range(len(comparisonTable))]

    #each child's list of differences is a row in comptab
    for i in range(clen):
        for j in range(plen):
            comparisonTable[i][j] = differenceSum(childResults[i], parentResults[j])
            if childAncillarys[i] not in parentAncillarys[j]:
                 comparisonTable[i][j] += len(childResults[0])/2
    rejects = []
    parentsChildren = sortChildrenHelper(comparisonTable, parentResults, availableChildren, rejects)

    clen = len(rejects)
    rejectTable = [[0 for x in range(plen)] for y in range(clen)]
    availableChildren = [x for x in range(len(rejectTable))]

    #each child's list of differences is a row in comptab
    for i in range(clen):
        for j in range(plen):
            rejectTable[i][j] = differenceSum(childResults[rejects[i]], parentResults[j])
            if childAncillarys[rejects[i]] not in parentAncillarys[j]:
                 rejectTable[i][j] += len(childResults[0])/2

    restOfParentsChildren = sortChildrenHelper(rejectTable, parentResults, availableChildren, rejects)

    for i in range(len(restOfParentsChildren)):
        extraChild = restOfParentsChildren[i]
        if extraChild != []:
            parentsChildren[i].append(rejects[restOfParentsChildren[i][0]])
    return parentsChildren

def sortChildrenHelper(comparisonTable, parentResults, availableChildren, rejects):
    plen = len(parentResults)
    # safely assume that there are more children than parents
    parentsChildren = [[] for x in range(plen)]

    numberOfChildren = 1 if len(rejects) > 0 else len(comparisonTable)//plen

    endOfChildren = len(availableChildren)


    while endOfChildren > 0:
        childInd = availableChildren[0]
        hasParent = False

        while hasParent == False:

            if comparisonTable[childInd][0] == -1 and comparisonTable[childInd][1:] == comparisonTable[childInd][:-1]:
                rejects.append(childInd)
                del availableChildren[0]
                endOfChildren = endOfChildren - 1
                hasParent = True
                continue

            bestIndex = bestParentIndex(comparisonTable[childInd])
            newParent = parentsChildren[bestIndex]
            currentDiff = comparisonTable[childInd][bestIndex]

            if len(newParent) == numberOfChildren:
                maxChildPos = maxInd(comparisonTable, newParent, bestIndex)
                maxChild = newParent[maxChildPos]
                if currentDiff >= comparisonTable[maxChild][bestIndex]:
                    comparisonTable[childInd][bestIndex] = -1
                else:
                    parentsChildren[bestIndex][maxChildPos] = childInd
                    comparisonTable[maxChild][bestIndex] = -1
                    availableChildren = availableChildren + [maxChild]
                    del availableChildren[0]
                    hasParent = True
            else:
                parentsChildren[bestIndex].append(childInd)
                del availableChildren[0]
                endOfChildren = endOfChildren - 1
                hasParent = True

    return parentsChildren



if __name__ == "__main__":
    main()
