import csv
childReader = csv.reader(open('children.csv', 'rb'))
parentReader = csv.reader(open('parents.csv', 'rb'))

def main():
    sortChildren(childReader, parentReader)
    #work out how to print the results of sortChildren

#work out the Differences between the
def workOutDifference(childRow, parentRow):


def sortChildren():
    leftOvers = []
