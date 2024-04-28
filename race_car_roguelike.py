#fastest developer time: 5 min, 13.85 sec




import pygame
import keyboard
import map_generator
import numpy
import math


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()



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
screenWidth = 1000
screenHeight = 700
screen = pygame.display.set_mode((screenWidth, screenHeight))

main_font = pygame.font.SysFont('arial', 25)

carWidth = 50
carHeight = 100

myCar = pygame.transform.scale(pygame.image.load('carSprite.png'), (carWidth, carHeight))
theCar = myCar

roadWidth = 100
roadHeight = 100
myRoad = pygame.transform.scale(pygame.image.load('roadSprite.png'), (roadWidth, roadHeight))
theRoad = myRoad

myIce = pygame.transform.scale(pygame.image.load('iceTrack.png'), (roadWidth, roadHeight))
theIce = myIce

myRamp = pygame.transform.scale(pygame.image.load('rampSprite.png'), (roadWidth, roadHeight))
theRamp = myRamp

myAbyss = pygame.transform.scale(pygame.image.load('abyss.png'), (roadWidth, roadHeight))
theAbyss = myAbyss

menuPic = pygame.transform.scale(pygame.image.load('path.jpg'), (screenWidth, screenHeight))
howtoplayPic = pygame.transform.scale(pygame.image.load('brickwall.jpeg'), (screenWidth, screenHeight))

theta = 0
brakeConstant = 2
currentSpeed = 0
janky = False
gameState = 'home menu'
gameStateOptions = ['home menu', 'game', 'how to play', 'new map']

carTravelX = 0
carTravelY = 0

origin = screenWidth * 0.5
thetaChanged = False
driftConstant = 8
skidThreshold = 15
minJumpSpeed = 13

skidLength = 10
skidTracks = []
centerSkid = [-2 *origin, -2 * origin, 0, 1]

for i in range(skidLength):
    skidTracks.append([-2 *origin, -2 * origin, 0, 1])


# Upgrades
totalMaxSpeed = 25
acceleration = totalMaxSpeed/20
maxSpeed = totalMaxSpeed
turningSpeed = 0.15
responsiveness = 0

# move des tings inside eventually
levelMap = map_generator.newMap()
checkpointsLeft = 0
totalLevels = 15
currentLevel = 1
totalTime = 0

buttonColorAug = 0
buttonColorAugVel = 5

roadMap = []
currentRoad = 'normal'

for i in range(len(levelMap) - 2):
    roadX = 50*levelMap[i][0]
    roadY = 50*levelMap[i][1]
    roadC = ((roadX ** 2) + (roadY ** 2)) ** (1/2)
    roadMap.append([roadX, roadY, numpy.arctan(roadY/(roadX + 0.1)), roadC])


# main loop
while ( stop != True):
    
    if gameState == 'home menu':
        if keyboard.is_pressed('p'):
            gameState = 'game'
        if keyboard.is_pressed('h'):
            gameState = 'how to play'
        if keyboard.is_pressed('q'):
            stop = True
        
        buttonColorAug = buttonColorAug + buttonColorAugVel

        if buttonColorAug <= 0 or buttonColorAug >= 50:
            buttonColorAugVel = - buttonColorAugVel
        #Graphics
        screen.blit(menuPic, (0, 0))
        screen.blit(pygame.font.SysFont('impact', 100).render('Formula 15', True, [0, 0, 0]), [screenWidth * 0.25, screenHeight * 0.25])
        pygame.draw.rect(screen, [200 + buttonColorAug, 200 - buttonColorAug, 200 + buttonColorAug], pygame.Rect(screenWidth * 0.15, screenHeight * 0.83, 600, 50))
        screen.blit(main_font.render('Press "p" to start playing, and "h" for how to play.', True, [0, 0, 0]), [screenWidth * 0.2, screenHeight * 0.85])
    
    if gameState == 'how to play':
        if keyboard.is_pressed('m'):
            gameState = 'home menu'
        if keyboard.is_pressed('q'):
            stop = True

        #Graphics
        screen.blit(howtoplayPic, (0, 0))
        screen.blit(main_font.render('Use "w" to accelerate. "a" and "d" are for right and left', True, [0, 0, 0]), [screenWidth * 0.05, screenHeight * 0.05])
        screen.blit(main_font.render('Use spacebar to brake.', True, [0, 0, 0]), [screenWidth * 0.05, screenHeight * 0.15])
        screen.blit(main_font.render('Ice is slippery. The grass off the track slows you down.', True, [0, 0, 0]), [screenWidth * 0.05, screenHeight * 0.25])
        screen.blit(main_font.render('You cannot jump if you are too slow.', True, [0, 0, 0]), [screenWidth * 0.05, screenHeight * 0.35])
        screen.blit(main_font.render('Try to make it through all 15 levels! (there are checkpoints along the track; hit them and then the start)', True, [0, 0, 0]), [screenWidth * 0.05, screenHeight * 0.45])
        screen.blit(main_font.render('Press "m" to get back to the main menu.', True, [0, 0, 0]), [screenWidth * 0.05, screenHeight * 0.55])
        screen.blit(main_font.render('Press "q" to quit at any time', True, [0, 0, 0]), [screenWidth * 0.05, screenHeight * 0.65])

    if gameState == 'win screen':
        if keyboard.is_pressed('q'):
            stop = True
        pygame.draw.rect(screen, [0, 0, 0], pygame.Rect(0, 0, screenWidth, screenHeight))
        screen.blit(main_font.render('YOU WON!', True, [250, 250, 250]), [screenWidth * 0.05, screenHeight * 0.05])
        screen.blit(main_font.render('Total time: ' + str(math.floor(3.33*totalTime) / 100) + 'sec', True, [250, 250, 250]), [screenWidth * 0.15, screenHeight * 0.25])
        screen.blit(main_font.render('Press "q" to quit', True, [250, 250, 250]), [screenWidth * 0.15, screenHeight * 0.65])

    
    if gameState == 'game':

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
        if (keyboard.is_pressed('space') and currentSpeed > -1):
            currentSpeed = currentSpeed - (brakeConstant * acceleration)

        carTheta = driftConstant * currentSpeed *thetaChanged

        if currentSpeed > maxSpeed:
            currentSpeed = maxSpeed

        if currentRoad == 'gap' and currentSpeed < minJumpSpeed:
            currentSpeed = -2

        if currentRoad == 'ice':
            turningSpeed = 0.07
            carTheta = 2*carTheta
        else:
            turningSpeed= 0.15

        theCar = pygame.transform.rotate(myCar, carTheta)

        if currentRoad == 'upRamp' or currentRoad == 'gap':
            theCar = pygame.transform.scale(myCar, (60, 120))
            theCar = pygame.transform.rotate(theCar, carTheta)


        roadAngles = []
        # calculating the road's position and orientation relative to the car

        if  janky != True:
            moveRel(roadMap)
            moveRel(skidTracks)

        for i in range(len(roadMap) -1):
            
            deltaX = roadMap[i][0] - roadMap[i+1][0]
            deltaY = roadMap[i][1] - roadMap[i+1][1]
            roadTheta = -math.degrees(numpy.arctan(deltaY/(deltaX + 0.0000021853)))
            roadAngles.append(roadTheta)
            

        if janky:
            moveRel(roadMap)
            moveRel(skidTracks)

        #skid mark calculation
        if abs(carTheta) >= skidThreshold:
            skidTracks.pop(0)
            
            skidX = numpy.sin(carTheta)
            skidY = numpy.cos(carTheta)
            skidC = ((skidX ** 2) + (skidY ** 2)) ** (1/2)
            centerSkid = [skidX, skidY, 0, skidC]

            
            skidTracks.append(centerSkid)
            
        else:
            for i in range(skidLength):
                skidTracks.pop(0)
                skidTracks.append([-2 *origin, -2 * origin, 0, 1])
        


        #graphics
        
        pygame.draw.rect(screen, [0, 100, 0], pygame.Rect(0, 0, screenWidth, screenHeight))

        roadIndex = 0
        tooFarAway = True
        currentRoad = 'off track'
        maxSpeed = totalMaxSpeed
        checkpointsLeft = 0
        for i in roadMap:
            
            if i == roadMap[0]:
                pygame.draw.rect(screen, [0, 200, 0], pygame.Rect(i[0] + origin - 150,i[1] + origin, 300, 30))

            elif (levelMap[roadIndex+1][2] == 'normal'):
                theRoad = pygame.transform.rotate(myRoad, roadAngles[roadIndex])
                screen.blit(theRoad, (i[0] + origin - theRoad.get_width()/2, i[1] + origin - theRoad.get_height()/2))
                roadIndex = roadIndex + 1
            elif (levelMap[roadIndex+1][2] == 'gap'):
                theAbyss = pygame.transform.rotate(myAbyss, roadAngles[roadIndex])
                screen.blit(theAbyss, (i[0] + origin - theAbyss.get_width()/2, i[1] + origin - theAbyss.get_height()/2))
                roadIndex = roadIndex + 1
            elif (levelMap[roadIndex+1][2] == 'upRamp'):
                theRamp = pygame.transform.rotate(myRamp, roadAngles[roadIndex])
                screen.blit(theRamp, (i[0] + origin - theRamp.get_width()/2, i[1] + origin - theRamp.get_height()/2))
                roadIndex = roadIndex + 1
            else:
                theIce = pygame.transform.rotate(myIce, roadAngles[roadIndex])
                screen.blit(theIce, (i[0] + origin - theIce.get_width()/2, i[1] + origin - theIce.get_height()/2))
                roadIndex = roadIndex + 1

            if levelMap[roadIndex][3] == 'checkpoint':
                checkpointsLeft = checkpointsLeft + 1




            if((i[0]**2)+(i[1]**2))**(1/2) <= roadWidth/1:
                tooFarAway = False
                if currentRoad != 'start':
                    currentRoad = levelMap[roadIndex][2]
                levelMap[roadIndex][3] = 'not checkpoint'
            

            

        if tooFarAway:
            maxSpeed = totalMaxSpeed/5

        if currentRoad == 'start' and checkpointsLeft == 0:
            if currentLevel >= totalLevels:
                gameState = 'win screen'
            
            levelMap = map_generator.newMap()
            pygame.time.delay(600)
            currentLevel = currentLevel +1
            roadMap = []
            for i in range(len(levelMap) - 2):
                roadX = 50*levelMap[i][0]
                roadY = 50*levelMap[i][1]
                roadC = ((roadX ** 2) + (roadY ** 2)) ** (1/2)
                roadMap.append([roadX, roadY, numpy.arctan(roadY/(roadX + 0.1)), roadC])

            
        
        for i in range(len(skidTracks)-1):
            if i>0:
                pygame.draw.line(screen, [0, 0, 0], (skidTracks[i-1][0] + origin,skidTracks[i-1][1] + origin), (skidTracks[i][0] + origin,skidTracks[i][1] + origin), 3)
        
        screen.blit(theCar, (origin - theCar.get_width()/2, origin - theCar.get_height()/2))
        pygame.draw.rect(screen, [200, 200, 200], pygame.Rect(screenWidth * 0.15, screenHeight * 0.13, 300, 200))
        screen.blit(main_font.render(str(checkpointsLeft)+ ' checkpoints to go', True, [0, 0, 0]), [screenWidth * 0.2, screenHeight * 0.15])
        screen.blit(main_font.render('level ' +str(currentLevel) + '/' + str(totalLevels), True, [0, 0, 0]), [screenWidth * 0.2, screenHeight * 0.25])
        screen.blit(main_font.render('speed: ' + str(currentSpeed * 4), True, [0, 0, 0]), [screenWidth * 0.2, screenHeight * 0.35])

        totalTime = totalTime + 1

    

    #time between each frame
    clock.tick(30)
    #print(clock.get_fps())
    #updates the frame
    pygame.display.update()
