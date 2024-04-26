import pygame
import keyboard
import map_generator
import numpy


pygame.init()
pygame.font.init()



# small Functions

def moveRel(graphics:list):
    for i in graphics:
        
        newTheta = i[2] + thetaChanged
        
        graphicsX = (i[3] * numpy.cos(newTheta))
        graphicsY = (i[3] * numpy.sin(newTheta)) + currentSpeed
        newC = ((graphicsX ** 2) + (graphicsY ** 2)) ** (1/2)
        newTheta = numpy.arctan(graphicsY/(graphicsX + .000128753))
        if  graphicsX < 0:
            newTheta = newTheta + numpy.pi
        i[0]= graphicsX
        i[1] = graphicsY
        i[2] = newTheta
        i[3] = newC

#Variable initialization

stop = False
dt = 100
screenWidth = 500
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))

main_font = pygame.font.SysFont('arial', 25)

carWidth = 50
carHeight = 100

myCar = pygame.transform.scale(pygame.image.load('topDownCar.jpg'), (carWidth, carHeight))
theCar = myCar

theta = 0
brakeConstant = 5
currentSpeed = 0

carTravelX = 0
carTravelY = 0

origin = screenWidth * 0.5
thetaChanged = False
driftConstant = 3
skidThreshold = 15

skidLength = 10
skidTracks = []
centerSkid = [-2 *origin, -2 * origin, 0, 1]

for i in range(skidLength):
    skidTracks.append([-2 *origin, -2 * origin, 0, 1])


# Upgrades
acceleration = 5
maxSpeed = 50
turningSpeed = 0.3
responsiveness = 0

levelMap = map_generator.newMap()

roadMap = []

for i in range(len(levelMap) - 2):
        #pygame.draw.rect(screen, [200, 0, 0], pygame.Rect(10 * i[0] + 100, 10 * i[1] + 100, 5, 5))
        roadX = 100*levelMap[i][0]
        roadY = 100*levelMap[i][1]
        roadC = ((roadX ** 2) + (roadY ** 2)) ** (1/2)
        roadMap.append([roadX, roadY, numpy.arctan(roadY/(roadX + 0.1)), roadC])


# main loop
while ( stop != True):
    
    for event in pygame.event.get():
        #key inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                #stops the loop
                stop = True

    thetaChanged = 0
    if keyboard.is_pressed('a'):
        thetaChanged = + turningSpeed
    if keyboard.is_pressed('d'):
 
        thetaChanged = - turningSpeed
    if (keyboard.is_pressed('w') and currentSpeed < maxSpeed):
        currentSpeed = currentSpeed + acceleration
    if (keyboard.is_pressed('space') and currentSpeed > brakeConstant*acceleration):
        currentSpeed = currentSpeed - (brakeConstant * acceleration)
    elif keyboard.is_pressed('space'):
        currentSpeed = 0

    carTheta = driftConstant * currentSpeed *thetaChanged

    if currentSpeed > maxSpeed:
        currentSpeed = maxSpeed
    
    theCar = pygame.transform.rotate(myCar, carTheta)

    # calculating the road's position and orientation relative to the car


    moveRel(roadMap)
    moveRel(skidTracks)

    #skid mark calculation
    if abs(carTheta) >= skidThreshold:
        skidTracks.pop(0)
        skidTracks.pop(1)
        skidX = numpy.sin(carTheta)
        skidY = numpy.cos(carTheta)
        skidC = ((skidX ** 2) + (skidY ** 2)) ** (1/2)
        centerSkid = [skidX, skidY, 0, skidC]

        
        skidTracks.append(centerSkid)
        skidTracks.append(centerSkid)
    else:
        for i in range(skidLength):
            skidTracks.pop(0)
            skidTracks.append([-2 *origin, -2 * origin, 0, 1])
    




    #graphics
    
    pygame.draw.rect(screen, [200, 200, 200], pygame.Rect(0, 0, screenWidth, screenHeight))
    screen.blit(theCar, (screenWidth/2 - theCar.get_width()/2, screenHeight/2 - theCar.get_height()/2))
    screen.blit(main_font.render(str(currentSpeed), True, [0, 0, 0]), [screenWidth * 0.3, screenHeight * 0.85])

    for i in roadMap:
        if i == roadMap[0]:
            pygame.draw.rect(screen, [0, 200, 0], pygame.Rect(i[0] + origin,i[1] + origin, 30, 30))
        else:
            pygame.draw.rect(screen, [200, 0, 0], pygame.Rect(i[0] + origin,i[1] + origin, 5, 5))

    for i in range(len(skidTracks)-1):
        if i>0:
            pygame.draw.line(screen, [0, 0, 0], (skidTracks[i-1][0] + origin,skidTracks[i-1][1] + origin), (skidTracks[i][0] + origin,skidTracks[i][1] + origin), 3)
    

    #time between each frame
    pygame.time.wait(dt)
    #updates the frame
    pygame.display.update()