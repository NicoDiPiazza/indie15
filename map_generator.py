from random import random
def newMap():
    heightBound = 20
    generatedMap = [[0,0]]

    roadOptions = ['normal', 'upRamp', 'gap']

    for j in range(4* heightBound):
        if j < heightBound:
            newPoint = [generatedMap[j][0] + 1, generatedMap[j][1] - round(random())]
        elif (j < 2 * heightBound):
            newPoint = [generatedMap[j][0] + round(random()), generatedMap[j][1] + 1]
        elif (j < 3 * heightBound):
            newPoint = [generatedMap[j][0] - 1, generatedMap[j][1] + round(random())]
        generatedMap.append(newPoint)
    
    while generatedMap[len(generatedMap) -1] != [0,0]:
        if generatedMap[len(generatedMap) -1][0] > 0:
            newPoint = [generatedMap[len(generatedMap) -1][0] -1]
        else:
            newPoint = [0]
        if generatedMap[len(generatedMap) -1][1] > 0:
            newPoint.append(generatedMap[len(generatedMap) -1][1] -1)
        else:
            newPoint.append(0)
        generatedMap.append(newPoint)



    return generatedMap