### Citations ###
# 1. Image of a space background
# Original Source: Codeskulptor
# URL to Original: http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png
# First Use: Line 45 (renamed to bg.png)
#
# 2. Image of a Space Ship
# Original Source: Codeskulptor
# URL to Original: http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png
# First Use: Line 52 (renamed to ship.png)
#
# 3. Image of a Asteriod
# Original Source: Codeskulptor
# URL to Original: http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png
# First Use: Line 190 (renamed to asteroid.png)

###
from cmu_graphics import *
import math
import random
global bg
score = 0
asteriods = []
friction_rate = .1
rad = math.pi/180 #The math library uses radians, so this is to help convert degrees to radians
topspeed = 20 # The top speed
speed = .6 # The acceleration rate
rotate = .35
app.stepsPerSecond = 50
horzSpeed=0
vertSpeed=0
rotateSpeed=0
gamestate = 0 # 0 = menu, 1 = game
lives = 3
mainmenu = []
lasers = []
cycle = 0
prev = 0
lasercolors = ['paleGreen','lightGreen','greenYellow','mediumSpringGreen',
    'chartreuse','springGreen','lawnGreen','limeGreen','lime'] 
def stage():
    global gamestate, mainmenu, play,bg
    gamestate = 0.5
    bg = Image('bg.png',0,0)
    mainmenu.append(Label('Asteriod', 165, 50, size=60,font='Star jedi outline',fill='white')) # Title Top Text
    mainmenu.append(Label('Smash', 290, 100, size=60,font='Star jedi outline',fill='white')) # Title Bottom Text
    play = Label('Play',200,190,size=60,bold=True,fill='white',font='Bangers')
    mainmenu.append(play) # Playbutton
    mainmenu.append(Rect(100,160,200,60,fill=None,border=rgb(255,192,203),borderWidth=5)) 
sprite=Image('ship.png',200,200) # The main character/sprite
sprite.rotateAngle = -90
def onMousePress(x,y):
    try: # if the game is started on the gamestate of 1 it will break this code making debugging annoying
        global gamestate,play,display_score
        if play.hits(x,y):
            gamestate = 1
            display_score = Label(0,35,25,fill='white',size=25,bold=True)
    except:
        pass
        
def onKeyHold(key):
    if gamestate == 1:
        global horzSpeed, vertSpeed, rotateSpeed
        SpriteAngle = sprite.rotateAngle 
        for i in key:
            if i == 'd':
                if rotateSpeed < 30:
                    rotateSpeed += rotate
            elif i == 'a':
                if rotateSpeed > -30:
                    rotateSpeed -= rotate
            # I can only move the sprite up and down, left and right, so 
            #if the sprite is at an angle it needs to move on that line/angle
            # So the trig determines
            elif i == 'w' :
                vertSpeed += speed*math.sin(SpriteAngle*rad)
                horzSpeed += speed*math.cos(SpriteAngle*rad)
            elif i == 's' :
                vertSpeed -= speed*math.sin(SpriteAngle*rad)
                horzSpeed -= speed*math.cos(SpriteAngle*rad)
            elif i == 'space': #Shoots the laser
                createLaser(sprite.centerX,sprite.centerY,SpriteAngle)
        if horzSpeed > topspeed: # Limits the sprites speed
            horzSpeed = topspeed
        if horzSpeed < -topspeed:
            horzSpeed = -topspeed
        if vertSpeed > topspeed:
            vertSpeed = topspeed
        if vertSpeed < -topspeed:
            vertSpeed = -topspeed
def createLaser(x,y,spriteangle):
    global lasers,prev
    if cycle - prev > 5: # Creates a delay in the lasers, (5)
        laserposX, laserposY = getPointInDir(x, y, spriteangle, 30) # Determines location for the laser
        lasers.append(Rect(laserposX,laserposY,15,2,fill=random.choice(lasercolors),rotateAngle=spriteangle))
        prev = cycle # updates the prev variable, to ensure the delay works
    pass
    
def keeponscreen(object):
    if object.centerX > 400: #Keeps the sprite within the screen
        object.centerX = 0 #Teleports the sprite on the otherside of the screen
    if object.centerX < 0:
        object.centerX = 400
    if object.centerY > 400:
        object.centerY = 0
    if object.centerY < 0:
        object.centerY = 400
        
def friction():
    global horzSpeed, vertSpeed, rotateSpeed #Slows the rotation and Speed down to 0 for playability
    if horzSpeed > 0:
        horzSpeed -= friction_rate
    if horzSpeed < 0:
        horzSpeed += friction_rate
    if vertSpeed > 0:
        vertSpeed -= friction_rate
    if vertSpeed < 0:
        vertSpeed += friction_rate
    if rotateSpeed > 0:
        rotateSpeed -= friction_rate
    if rotateSpeed < 0:
        rotateSpeed += friction_rate
 
def asteriodCollisons(asteriods):
    for i in asteriods: # Checks all the asteriod if they are hit
        if sprite.hitsShape(i):
            i.visible = False
            asteriods.remove(i)
            lives = -1 #Takes a way a life
            bg.toFront()
            return lives
def onStep():
    global cycle, score, display_score,lives,gamestate
    keeponscreen(sprite)
    cycle += 1
    if gamestate== 0: # The Mainmenu
        stage()
    if gamestate ==1:# The Actual Game
        for i in mainmenu:
            i.visible=False
        mainmenu.clear()
        bg.toBack()
        display_score.toFront()
    if gamestate == 2: # Game over screen
        bg.toFront()
        Label('Game Over', 200, 150, size=60,font='Yrsa',fill='white')
        Label(f'Score: {str(score)}', 200, 200, size=30,font='Yrsa',fill='white')
    if lives <= 0:
        gamestate = 2
    friction()
    sprite.rotateAngle += rotateSpeed # Rotates the sprite
    sprite.centerX += horzSpeed # Moves the sprite based on horz speed
    sprite.centerY += vertSpeed #Moves the sprite based on vert speed
    for i in lasers:
        if i.centerX > 400 or i.centerX < 0 or i.centerY > 400 or i.centerY < 0: # Deletes laser if off screen
            i.visible = False
            lasers.remove(i) 
        i.centerY += 9*math.sin(i.rotateAngle*rad) # Moves the laser based on the angle of the user
        i.centerX += 9*math.cos(i.rotateAngle*rad)
        for a in asteriods: # Checks to see if the laser hits an asteriod
            if i.hitsShape(a):
                a.visible = False
                asteriods.remove(a)
                score+=10 # Adds to the score for shooting an asteriod
                display_score.value = score
    if random.randint(0,90) == 1 and gamestate == 1 and len(asteriods) < 15: #Randomly creates and asteriod if the Game is playing
        size = random.uniform(.25,1.5) # Random Size Asteriod
        x = random.randint(0,375) # Random position
        y = random.randint(0,375)
        if sprite.hits(x,y): # Makes sure the asteriod isnt going to summon on the user
            pass
        else:
            asteriods.append(Image('asteroid.png',x,y,height=82*size,width=79*size)) # Creates the asteriod
            for i in asteriods:
                if i.hitsShape(sprite): # also removes the asteriod to prevent it from spawning on the user
                    i.visible = False
                    asteriods.remove(i)
    try:
        lives = lives + asteriodCollisons(asteriods) #Checks to see if the sprite hits an asteriods and subtracts from lives
    except:
        pass
cmu_graphics.run()