from abc import ABCMeta, abstractmethod
from copy import deepcopy
from collections import deque
import random
import time

class Vane:

    def __init__(self, order, A, B):
        self.order = order
        self.A = A
        self.B = B

#---functions---#
def compute_avg_area(vanes):
    totalArea = 0.0
    numVanes = len(vanes)
    
    for i in range(numVanes):
        totalArea += vanes[i].A + vanes[i].B
        
    return totalArea / numVanes

def compute_score(vanes, avgArea):
    score = 0.0
    numVanes = len(vanes)
    
    for i in range(numVanes - 1):
        score += abs(avgArea - vanes[i].A - vanes[i+1].B)
        
    score += abs(avgArea - vanes[numVanes - 1].A - vanes[0].B)
    
    score = score * -1
    
    return score

def get_Neighbours(bestCandidate, avgArea):
    neighbourList = []
    original = bestCandidate

    for i in range(len(bestCandidate)):
        bestCandidate[0], bestCandidate[i] = bestCandidate[i], bestCandidate[0]
        neighbourList.append(bestCandidate)
        bestCandidate = original

    return neighbourList

def argmax(scores):
    maxVal = max(scores)

    for i in range(len(scores)):
        if scores[i] == maxVal:
            return i
    return 0

#---program---#
print("Enter input file name (press enter to default to \"input.txt\"):")
input = input()

if input == "":
    input = "input.txt"

fin = open(input)

vanes = []
tabuList = []

for line in fin:
    spline = line.split(",")
    vanes.append(Vane(int(spline[0]), float(spline[1]), float(spline[2])))

numVanes = len(vanes)
fin.close()

start = time.perf_counter()

avgArea = compute_avg_area(vanes)

bestVanes = vanes
random.shuffle(bestVanes)
bestCandidate = bestVanes
maxTabuSize = 100
tabuList.append(bestVanes)

while True:
    vNeighbourhood = get_Neighbours(bestCandidate, avgArea)
    bestCandidate = vNeighbourhood[0]

    for vCandidate in vNeighbourhood:
        if((vCandidate not in tabuList) and (compute_score(vCandidate, avgArea) > compute_score(bestCandidate, avgArea))):
            bestCandidate = vCandidate

    if(compute_score(bestCandidate, avgArea) > compute_score(bestVanes, avgArea)):
        bestVanes = bestCandidate

    if(bestVanes in tabuList):
        break

    tabuList.append(bestCandidate)
    if(len(tabuList) > maxTabuSize):
        tabuList.pop(0)

end = time.perf_counter()
elapsed = "%.12f" % (end - start)

fout = open("output.txt", "wt")
fout.write("Elapsed Time: " + elapsed + " sec\n")

for i in range(numVanes):
    fout.write(str(bestVanes[i].order) + "," + str(bestVanes[i].A) + "," + str(bestVanes[i].B) + "\n")
fout.write("Best Score: " + str(compute_score(bestVanes, avgArea)))    
fout.close()






