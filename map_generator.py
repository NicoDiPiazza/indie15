from random import random
import math
def newMap():
    heightBound = 40
    generatedMap = [[0,0]]

    roadOptions = ['start', 'normal', 'ice', 'upRamp', 'gap']
    normalOptions = ['normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'ice', 'normal', 'upRamp']
    iceOptions = ['normal', 'normal', 'ice', 'ice', 'ice', 'ice', 'ice', 'ice', 'ice', 'ice']
    # gap has 100% chance to follow ramp
    #ice has a 60% chance to follow ice
    #road has a 70% chance to follow road
    #ramp has 10% to follow anything (other than ramp)
    #each point has a 10% chance of being a checkpoint
    #the starting point is always a road

#first three quarters
    for j in range(4* heightBound):
        if j < heightBound:
            newPoint = [generatedMap[j][0] + 1, generatedMap[j][1] - round(random())]
        elif (j < 2 * heightBound):
            newPoint = [generatedMap[j][0] + round(random()), generatedMap[j][1] + 1]
        elif (j < 3 * heightBound):
            newPoint = [generatedMap[j][0] - 1, generatedMap[j][1] + round(random())]
        generatedMap.append(newPoint)


#last quarter    
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

#assigning each node a road type
    for i in range(len(generatedMap)-1):
        if(i == 0):
            generatedMap[i].append('start')
        elif generatedMap[i-1][2] == 'normal' or generatedMap[i-1][2] == 'gap':
            assignment = normalOptions[math.floor(random() * 10)]
            generatedMap[i].append(assignment)
        elif generatedMap[i-1][2] == 'ice':
            assignment = iceOptions[math.floor(random() * 10)]
            generatedMap[i].append(assignment)
        elif  (generatedMap[i-1][2] == 'upRamp') and i != len(generatedMap)-2:
            assignment = 'gap'
            generatedMap[i].append(assignment)
        else:
            generatedMap[i].append('normal')

        checkpoint = random()
        if checkpoint <= 0.07:
            generatedMap[i].append('checkpoint')
        else:
            generatedMap[i].append('not checkpoint')




    return generatedMap


    return generatedMap
