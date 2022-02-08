# Updated Animation Starter Code
from tkinter import *
import random
import pyaudio
import sys
import numpy as np
import aubio
import threading 
import copy
import PIL


#sourced and modified from the Aubio Demos in GitHub
#https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py
def getPitch() :
    p = pyaudio.PyAudio()

    # open stream
    buffer_size = 1024
    pyaudio_format = pyaudio.paFloat32
    n_channels = 1
    samplerate = 44100
    stream = p.open(format=pyaudio_format,
                    channels=n_channels,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=buffer_size)

    if len(sys.argv) > 1:
        # record 5 seconds
        output_filename = sys.argv[1]
        record_duration = 5 # exit 1
        outputsink = aubio.sink(sys.argv[1], samplerate)
        total_frames = 0
    else:
        # run forever
        outputsink = None
        record_duration = None
    tolerance = 0.8
    win_s = 4096 # fft size
    hop_s = buffer_size # hop size
    pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)
    
    print("*** starting recording")
   
    
    audiobuffer = stream.read(buffer_size)
    signal = np.fromstring(audiobuffer, dtype=np.float32)

    pitch = pitch_o(signal)[0]
    confidence = pitch_o.get_confidence()
    
    #print(pitch)

    #print("{}".format(pitch))
    
    if outputsink:
        outputsink(signal, len(signal))

        
    
    print("*** done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return pitch
    
    


#animation shell code from 15-112 Website
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.mapWidth = data.width*70
    data.radius = 20
    data.cx = data.radius
    data.groundY = int(data.height * 2/3 + 70)
    data.cy = data.groundY - data.radius
    data.timerDelay = 10
    data.speed = 5
    data.scroll = 0
    data.timer = 0
    data.isDead = False 
    data.mode = "screen"
    data.desert = PhotoImage(file = "desert.gif")
    
    #data.bird = PhotoImage(file="normal bird.png")
    #data.drawBird = False 
    
    #cactus data
    data.cacti = []
    data.cactusThickness = 10
    data.cactusPosition = 0
    
    for cactusX in range(data.width,data.mapWidth,data.width) :
        y = int(random.randint((data.groundY-data.height//6),data.groundY-20))
        data.cacti.append([cactusX+random.randint(0,data.width//2), y])
        
    #mountain data
    data.mountains = []
    
        
    #jump data
    data.pitchList = [] 
    data.isJumping = False
    data.isFalling = False 
    
    
    #Score Data
    data.hiScore = 0
    data.currentScore = 0
                    
    
    #Gold Coin Data
    data.coins = []
    data.coinRadius = 10
    for coinPositions in range(data.width+20,data.mapWidth+20,data.width) :
        y = int(random.randint(20,data.groundY-data.height//2))
        data.coins.append([coinPositions,y])
    
    
    #Deadly Coin Data
    data.deadlyCoins = []
    data.deadlyCoinRadius = 10
    for coinPositions in range(data.width*3//2, data.mapWidth*3//2,data.width*2) :
        y = int(random.randint(40,data.groundY-data.height//2))
        data.deadlyCoins.append([coinPositions,y])
        
    #Night Mode Data
    #data.color = 99
    data.red = 255
    data.blue = 255
    data.green = 255
    data.isNight = False
    data.scoreTextColor = "black"
    
    #Character Data
    data.firstBoxColor = "black"
    data.secondBoxColor = "black"
    data.thirdBoxColor = "black"
    data.fourthBoxColor = "black"
    data.characterName = "Facebook"
    data.displayInstruction = False 
    data.flashingInstruction = False
    data.characterInstruction = True 
    data.facebook = PhotoImage(file="facebook.gif")
    data.comcast = PhotoImage(file="comcast.gif")
    data.att = PhotoImage(file = "att.gif")
    data.verizon = PhotoImage(file = "verizon.gif")
    data.characterScreen = PhotoImage(file = "desert screen.gif")
    
    
    #Bird Data
    data.normalBird = PhotoImage(file = "normal bird.gif")
    data.screamingBird = PhotoImage(file = "screaming bird.gif")
    data.fallingBird = PhotoImage(file = "falling bird.gif")
    data.deadBird = PhotoImage(file = "dead bird.gif")
    
    #Start Screen Data
    data.screenJumping = True
    data.screenFalling = False 
    
    
    #Character List Data
    data.characterList = []
    data.newList =[]
    data.coinsCollected = 0
    data.coinNewList = copy.copy(data.coins)
    data.facebookList = ["The telecom operators do not block the access to any number\nand there will be no deliberate delay connection\nto a particular number,\nunless the law specifies","Free Basics is an open platform(?)\nlaunched by Facebook\nthat provides free access to selected websites\n and internet services","Free Basics is not an open platform\nas Facebook defines its technical guidelines & reserves\nthe right to change the rules.","It's an app that offers users in\ndeveloping markets a 'free'\nFacebook-centric version of\n\the internet","Since Facebook rolled out Free Basics\nin a lot of developing nations\nit has become THE Internet itself for\na lot of people","In Myanmar,FB launched with the\ngovt's support. Later, during the Rohingya\ncrisis, it was\naccused of supporting ethnic cleansing."]
    
        
        
        
        
####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "screen"): screenMousePressed(event, data)
    elif (data.mode == "playGame"):   gameMousePressed(event, data)
    elif (data.mode == "character"):       characterMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "screen"): screenKeyPressed(event, data)
    elif (data.mode == "playGame"):   gameKeyPressed(event, data)
    elif (data.mode == "character"): characterKeyPressed(event,data)
    
def timerFired(data):
    if (data.mode == "screen"): screenTimerFired(data)
    elif (data.mode == "playGame"):   gameTimerFired(data)
    elif (data.mode == "character"):       characterTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "screen"): screenRedrawAll(canvas, data)
    elif (data.mode == "playGame"):   gameRedrawAll(canvas, data)
    elif (data.mode == "character"):       characterRedrawAll(canvas, data)
    
    
# Screen mode
####################################

def screenMousePressed(event, data):
    pass

def screenKeyPressed(event, data):
    data.mode = "character"
    data.cy = data.groundY - data.radius
    

def screenTimerFired(data):
    if data.timer%5000 == 0:
        if data.screenJumping :
            data.cy -= data.speed
            if data.cy - data.radius <= data.width//2 :
                data.screenJumping = False 
                data.screenFalling = True
        
        if data.screenFalling :
            data.cy += data.speed
        
            if data.cy + data.radius >= data.groundY - data.radius :
                #print("um wtf")
                data.cy = data.groundY - data.radius
                data.screenJumping = True
                data.screenFalling = False 
        
        

def screenRedrawAll(canvas, data):
    canvas.create_image(data.width//2,data.height//2,image = data.desert)
    canvas.create_text(data.width//2, data.height//4,
                       text="The No Internet Game", font="Arial 20")
    canvas.create_text(data.width//4 + 30,data.height//4 + 20,text="Try:",font = "Arial 15",anchor = "w")
    canvas.create_text(data.width//4+40,data.height//4 + 45, text = "Checking the network cable, modem, and router\nReconnecting to WiFi", font = "Arial 10",anchor = "w")
    canvas.create_text(data.width//4 + 32, data.height//4 + 65, text = "ERR_INTERNET_DISCONNECTED", font = "Arial 10", anchor = "w")
    canvas.create_text(data.width//4 + 15,data.height//4 + 85,text = "Press any key to choose a character!", font = "Arial 15", anchor = "w")
    #canvas.create_text(data.width//2+30,data.height//4 + 60, text = "Reconnecting to Wi-Fi", font = "Arial 10", anchor = "e")
    #canvas.create_rectangle(0-data.scroll,data.groundY,data.width,data.height,fill="black")
    canvas.create_image(data.cx-data.scroll,data.cy,image = data.normalBird)
    
#Mode Template code from Animation Demos in 15-112 Website
####################################
# character mode
####################################

def characterMousePressed(event, data):
    if ((event.x > data.width//8) and (event.x < data.width//2 - 40) and \
    (event.y > data.height//4 - 60) and (event.y < data.height//2 - 80)) :
        data.characterName = "Facebook"
        data.firstBoxColor = "red"
        data.displayInstruction = True
        data.characterInstruction = False 
        
        
    elif ((event.x > data.width//8) and (event.x<data.width//2 - 40) and \
    (event.y > data.height*3//4 - 100) and (event.y < data.height - 120)) :
        #print("I clicked")
        data.characterName = "AT&T"
        data.secondBoxColor = "red"
        data.displayInstruction = True
        data.characterInstruction = False 
    
    elif ((event.x > data.width//2 + 40) and (event.x < data.width*7//8) and \
    (event.y > data.height//4 - 60) and (event.y < data.height//2 - 80)) :
        
        data.characterName = "Comcast"
        data.thirdBoxColor = "red"
        data.displayInstruction = True
        data.characterInstruction = False 
        #print(data.characterName)
        
    elif ((event.x > data.width//2 + 40) and (event.x < data.width*7//8) and \
    (event.y > data.height*3//4-100) and (event.y < data.height - 120)) :
        data.characterName = "Verizon"
        data.fourthBoxColor = "red"
        data.displayInstruction = True 
        data.characterInstruction = False 
    
    

def characterKeyPressed(event, data):
    data.mode = "playGame"

def characterTimerFired(data):
    data.timer += 1
    if data.timer%50 == 0 :
        data.flashingInstruction = False
    else :
        data.flashingInstruction = True
    
def drawClickToPlay(canvas,data) :
    canvas.create_text(data.width//2,data.height//2,
    text = "Press any key to start playing!"
    ,fill = "red",font = "Arial 15 bold")

def characterRedrawAll(canvas, data):
    canvas.create_image(data.width//2,data.height//2,image = data.characterScreen)
    if data.characterInstruction :
        canvas.create_text(data.width//2,50,
        text = "CLICK ON THE OPTIONS BELOW TO CHOOSE A CHARACTER!",
        fill = "red", font = "Courier 15 bold")
    if data.displayInstruction :
        canvas.create_text(data.width//2,data.height//2-55,
        text = "Raise your voice pitch to make the bird fly")
        canvas.create_text(data.width//2,data.height//2-40,
        text = "Collect the gold coins to increase your points")
        canvas.create_text(data.width//2,data.height//2-25,
        text="Don't hit the green coins or the cacti else you're ded lolol")
        if data.flashingInstruction :
            drawClickToPlay(canvas,data)
        
    #first character name
    canvas.create_rectangle(data.width//8,data.height//4-60,data.width//2 \
    - 40,data.height//2-80, fill = data.firstBoxColor)
    canvas.create_image(data.width//8 + 3*data.width//16 - 20, data.height//4 - \
    60 + data.height//8 - 10,image = data.facebook)
    
    
    
    #second character name
    canvas.create_rectangle(data.width//8, data.height*3//4 - 100, \
    data.width//2 - 40, data.height-120,fill=data.secondBoxColor)
    canvas.create_image(data.width//8 + 3*data.width//16 - 20, \
    data.height*5//8 + 15,image = data.att)
    
    
    #third character name
    canvas.create_rectangle(data.width//2 + 40, data.height//4-60,\
    data.width*7//8, data.height//2 - 80, fill = data.thirdBoxColor)
    canvas.create_image(data.width*3//16 - 20 + data.width//2 + 40, \
    data.height//4 - 60 + data.height//8 - 10, image = data.comcast)
    
    
    #fourth character name 
    canvas.create_rectangle(data.width//2 + 40, data.height*3//4 - 100, \
    data.width*7//8, data.height - 120, fill = data.fourthBoxColor)
    canvas.create_image(data.width//2 + 40 + 3*data.width//16 - 20, \
    data.height//8 - 10 + data.height*3//4 - 100, image = data.verizon)



#Game mode
####################################

def gameMousePressed(event, data):
    # use event.x and event.y
    if data.isDead :
        if ((event.x > data.width//2 - 20) and (event.x < data.width//2 + 20) \
        and (event.y > data.height//2 -10) and (event.y < data.height//2 + 10)) :
            init(data)
    
    


def gameKeyPressed(event, data):
    # use event.char and event.keysym
   pass
        


            
def circleMovement(data) :
    data.cx += data.speed
    xLeft = data.cx - data.radius
    xRight = data.cx + data.radius
    yTop = data.cy - data.radius
    yBottom = data.cy + data.radius
    #put a buffer
    buffer = data.width * 2/3
    #Check whether we're scrolling out of the buffer distance
    if (data.cx + data.radius + buffer) >= (data.scroll + data.width) :
        data.scroll += data.speed
        
        

#this function is only to draw two clouds that remain stationary on the canvas
def drawClouds(data,canvas) :
    pass
    

def deadlyCoinsDraw(data,canvas) :
    for coins in data.deadlyCoins :
        x = coins[0]
        y = coins[1]
        canvas.create_oval(x-data.deadlyCoinRadius-data.scroll,
        y-data.deadlyCoinRadius,x+data.deadlyCoinRadius-data.scroll,
        y+data.deadlyCoinRadius,fill = "green")



    
def drawCacti(data,canvas) : 
    #print(data.cacti)
    shift = random.randint(-20,20)
    for cactus in data.cacti :
        #print(cactus)
        height = cactus[1]
        cactusPosition = cactus[0]
        canvas.create_rectangle(cactusPosition-data.scroll,data.groundY,
        data.cactusThickness+cactusPosition-data.scroll,height,
        fill = "green",width = 0)
        
        #top circle
        left = cactusPosition - data.scroll
        top = height - data.cactusThickness//2
        right = cactusPosition + data.cactusThickness - data.scroll
        bottom = height + data.cactusThickness//2
        canvas.create_oval(left,top,right,bottom,fill="green",width=0)
        
        #left cactus branch
        xRightTop = cactusPosition - data.scroll
        yRightTop = height + 0.3*(data.groundY - height)
        xRightBottom = cactusPosition - data.scroll
        yRightBottom = yRightTop + data.cactusThickness
        yLeftTop = yRightTop - 3
        xLeftTop = cactusPosition - 10 - data.scroll
        xLeftBottom = cactusPosition - 10 - data.scroll
        yLeftBottom = yLeftTop + data.cactusThickness
        #print(xRightTop,yRightTop,xRightBottom,yRightBottom,xLeftBottom,
        #yLeftBottom,xLeftTop,yLeftTop)
        canvas.create_polygon(xRightTop,yRightTop,xRightBottom,yRightBottom,
        xLeftBottom,yLeftBottom,xLeftTop,yLeftTop,fill = "green")
        
        # first circle
        left1 = xLeftTop - data.cactusThickness//2 
        top1 = yLeftTop
        right1 = xLeftTop + data.cactusThickness/2 
        bottom1 = yLeftBottom
        canvas.create_oval(left1,top1,right1,bottom1,fill = "green",width=0)
        
        #left cactus branch's top rectangle
        xTop = left1
        yTop = top1 - 0.3*(data.groundY-height)
        xBottom = right1
        yBottom = bottom1 - data.cactusThickness//2 - 1
        canvas.create_rectangle(xTop,yTop,xBottom,yBottom,fill="green",width=0)
        
        # second circle
        left2 = left1
        top2 = yTop - data.cactusThickness//2
        right2 = right1
        bottom2 = yTop + data.cactusThickness//2
        canvas.create_oval(left2,top2,right2,bottom2,fill="green",width=0)
        
        """Right Cactus Branch"""
        xLTop = cactusPosition + data.cactusThickness - data.scroll
        yLTop = height + 0.2*(data.groundY - height)
        xLBottom = cactusPosition + data.cactusThickness - data.scroll
        yLBottom = yLTop + data.cactusThickness
        xRTop = cactusPosition + data.cactusThickness + 10 - data.scroll
        yRTop = yLTop - 3
        xRBottom = cactusPosition + data.cactusThickness + 10 - data.scroll
        yRBottom = yRTop + data.cactusThickness
        canvas.create_polygon(xLTop,yLTop,xLBottom,yLBottom,xRBottom,yRBottom,\
        xRTop,yRTop,fill="green")
        
        #third circle 
        left3 = xRTop - data.cactusThickness//2
        top3 = yRTop
        right3 = xRTop + data.cactusThickness//2
        bottom3 = yRBottom
        canvas.create_oval(left3,top3,right3,bottom3,fill="green",width=0)
        
        #right cactus's top rectangle
        topX = left3
        topY = top3 - 0.4*(data.groundY - height)
        bottomX = right3
        bottomY = bottom3 - data.cactusThickness//2 - 1
        canvas.create_rectangle(topX,topY,bottomX,bottomY,fill="green",width=0)
        
        #fourth circle
        left4 = left3
        top4 = topY - data.cactusThickness//2
        right4 = topX + data.cactusThickness
        bottom4 = top4 + data.cactusThickness
        canvas.create_oval(left4,top4,right4,bottom4,fill="green",width=0)
        
        
#function to find distance between two points
def distance(x1,y1,x2,y2) :
    x = (x2 - x1)**2
    y = (y1 - y2)**2
    return (x+y)**0.5

        
#to find whether the ball is being collided by the cactus
def cactusCollision(data) :
    index = 0
    while index < len(data.cacti) :
        cactus = data.cacti[index]
        cactusPosition = cactus[0]
        height = cactus[1]
        #check whether the cactus's left branch area is being hit
        if ((data.cx + data.radius >= cactusPosition -10) and \
        (data.cx + data.radius <= cactusPosition + data.cactusThickness + 10) \
        and (data.cy + data.radius >= height - 3 - 0.2*(data.groundY - height) \
        - data.cactusThickness//2)) or ((data.cx - data.radius <= cactusPosition\
         + data.cactusThickness + 10) and \
         (data.cx -data.radius >= cactusPosition - 10) and \
         (data.cy + data.radius >= height-3 - 0.2*(data.groundY-height) - \
         data.cactusThickness//2)) :
            print("collide with cactus")
            data.isDead = True
            return
        index += 1
        

def drawCharacterList(data,canvas) :
    if data.characterName == "Facebook" :
        data.characterList = data.facebookList
    elif data.characterName == "Comcast" :
        data.characterList = data.comcastList
    elif data.characterName == "Verizon" :
        data.characterList = data.verizonList
    elif data.characterName == "AT&T" :
        data.characterList = data.attList
    if len(data.newList) > 0 :
        for coins in data.newList :
            x = coins[0]
            y = coins[1]
            if len(data.characterList) >= data.coinsCollected and data.coinsCollected > 0:
                line = data.characterList[data.coinsCollected - 1]
                canvas.create_text(x-data.scroll,y,text = line, font = "Arial 5 bold")
                data.newList = data.newList[1:]

#to check if dino is colliding with coins and also to make then disappear 
#if they do
def coinCollision(data) :
    index = 0 
    while index < len(data.coins) :
        coins = data.coins[index]
        x = coins[0]
        y = coins[1] 
        print(data.cx,x)
        #check if the upper part of ball hits the coin 
        #print(x,y)
        #print(data.scroll)
        if distance(data.cx,data.cy,x+data.coinRadius,y) <= data.radius + \
        data.coinRadius :   ### should this be data.cx or data.cx + data.radius
            #print("if coin part")
            data.coinsCollected += 1
            data.newList.append(coins)
            data.coins.pop(index)
            data.currentScore += 10
            
            return
        index += 1

        
def deadlyCoinCollision(data) :
    index = 0 
    while index < len(data.deadlyCoins):
        coins = data.deadlyCoins[index]
        x = coins[0]
        y = coins[1] 
        #print(data.cx,x)
        #check if the upper part of ball hits the coin 
        #print(x,y)
        #print(data.scroll)
        if distance(data.cx,data.cy,x+data.deadlyCoinRadius,y) <= data.radius + \
        data.deadlyCoinRadius :   ### should this be data.cx or data.cx + data.radius
            print("coin death lolololol")
            data.isDead = True
            return
        index += 1
    

            
    
    
        

def drawCoins(data,canvas) :
    for coins in data.coins :
        height = coins[1]
        coinPosition = coins[0]
        canvas.create_oval(coinPosition-data.coinRadius-data.scroll,
        height-data.coinRadius,coinPosition+data.coinRadius-data.scroll,
        height+data.coinRadius,fill="gold")
        canvas.create_text(coinPosition-data.scroll,height,text = "+10", 
        font = "Ariel 5")

# from 112 Website on Strings
def readFile(path,data):
    with open(path, "rt") as f:
        return f.read()
        
def writeFile(path, contents,data):
    with open(path, "wt") as f:
        f.write(str(data.currentScore) + " " + data.characterName + "\n")


def getScores(path,data) :
    scores = []
    for line in readFile("score.txt",data).splitlines() :
        words = line.split(" ") 
        if words == [""]: continue 
        scores += [(int(words[0]),words[1])]
    return ((sorted(scores))[::-1])         
    

def gameTimerFired(data):
    cactusCollision(data)
    deadlyCoinCollision(data)
    if data.isDead == False :
        
        data.timer += 1
        circleMovement(data)
        
        x = getPitch()
        coinCollision(data)
        cactusCollision(data)
        #print(x)
        
        #night mode
        if (data.currentScore%50 > 30 and data.currentScore%50 < 49) :
            print("night",data.currentScore%50)
            data.isNight = True
        else :
            data.isNight = False 
            
        if data.isNight :
            if data.red > 0 and data.blue > 0 and data.green > 0 :
                if data.timer%2 == 0 :
                    data.red -= 5
                    data.green -= 5
                    data.blue -= 5
            else :
                data.red = 0
                data.blue = 0
                data.green = 0
        
        elif not(data.isNight) :
            if data.red < 255 and data.blue < 255 and data.green < 255 :
                data.red += 5
                data.blue += 5
                data.green += 5
        
        
        #score modification
        if data.timer%5 == 0 :
            data.currentScore += 1
        
        contentsToWrite = str(data.currentScore) + " " + str(data.characterName) + "\n"
        
        if len(getScores("score.txt",data)) == 0 :
            data.hiScore = data.currentScore
        #contentsRead = readFile("score.txt", data)    
        if len(getScores("score.txt",data)) > 0:
            data.hiScore = getScores("score.txt",data)[0][0]
            if data.currentScore > data.hiScore :
                data.hiScore = data.currentScore
            
        #the ball should jump only when it's on the ground
        if x > 65 and data.cy >= data.groundY - data.radius:
            data.isJumping = True
            #print("adding")
            data.pitchList.append(x)
            
        if data.isJumping == True :
            data.cy -= x//7
            if (x == 0 and data.cy < data.groundY - data.radius) or (data.cy-data.radius < 0):
                #print("going into if")
                data.isFalling = True
                data.isJumping = False 
                #print("falling",data.isFalling)
                #print("jumping",data.isJumping)
        if data.isFalling == True :
            #print("I'm falling")
            if data.cy + data.pitchList[len(data.pitchList)-1]//7 >= data.groundY - data.radius:
                data.cy = data.groundY - data.radius
            else :
                data.cy += data.pitchList[len(data.pitchList)-1]//7
            #print(data.pitchList[len(data.pitchList)-1]//7)
            
            data.pitchList[len(data.pitchList)-1] = data.pitchList[len(data.pitchList)-1] + 1
            
            
        if data.cy >= data.groundY - data.radius :
            data.isFalling = False
            data.isJumping = False 
    
    else :
        writeFile("score.txt",str(data.currentScore) + " " + data.characterName + "\n",data)

#from Spring 2016 Notes
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)


def gameRedrawAll(canvas, data):
    canvas.create_image(data.width//2,data.height//2,image = data.desert)
    #canvas.create_image(0-data.scroll,0,data.width-data.scroll,data.height,image = data.desert)
    
    if data.isNight :
        canvas.create_rectangle(0,0,data.width,data.height,
        fill=rgbString(data.red,data.green,data.blue),width=0)
        canvas.create_oval(data.width*3//4, data.height//4 - 30, \
        data.width*3//4 + 60, data.height//4 + 30,fill="white",width = 0)
        canvas.create_oval(data.width*3//4-5, data.height//4 - 25, \
        data.width*3//4 + 45, data.height//4 + 25,fill=rgbString(data.red,data.green,data.blue),width = 0)
        data.scoreTextColor = "white"
    elif data.isNight == False :
        data.scoreTextColor = "black"
    # draw in canvas
    
    
    #canvas.create_rectangle(0-data.scroll,data.groundY,data.width,\
    #data.height,fill="tan4")
    
    
    drawCacti(data,canvas)
    drawCoins(data,canvas)
    deadlyCoinsDraw(data,canvas)
    
    canvas.create_text(data.width//8,data.height//10 - 10, text = "Character :" + data.characterName, font = "Arial 10 bold", fill = data.scoreTextColor)
    
    canvas.create_text(data.width*1/8,data.height//10,text = "Hi-Score: " + \
    str(data.hiScore) + " Score: " + str(data.currentScore),
    font = "Arial 10 bold",fill=data.scoreTextColor)
    if data.isJumping :
        canvas.create_image(data.cx - data.scroll,
        data.cy,image = data.screamingBird)
    elif data.isFalling :
        canvas.create_image(data.cx-data.scroll,
        data.cy,image = data.fallingBird)
    else :
        canvas.create_image(data.cx-data.scroll,
        data.cy,image = data.normalBird)
    
    if data.isDead :
        print("DED lolol")
        canvas.create_text(data.width//2,data.height//2-60,text="GAMEOVER!")
        canvas.create_text(data.width//2,data.height//2 -40, 
        text = "YOU HIT NET NEUTRALITY")
        canvas.create_image(data.cx-data.scroll,data.cy,
        image = data.deadBird)
        canvas.create_rectangle(data.width//2 - 20,\
        data.height//2-10,data.width//2 + 20,data.height//2+10,fill = "blue")
        
    
    

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 25 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(500, 500)




# if __name__ == "__main__": 
#     # creating thread 
#     t1 = threading.Thread(target=run, args=()) 
#     t2 = threading.Thread(target=getPitch, args=()) 
#   
#     # starting thread 1 
#     t1.start() 
#     # starting thread 2 
#     t2.start() 
#   
#     # wait until thread 1 is completely executed 
#     t1.join()   
#     # wait until thread 2 is completely executed 
#     t2.join() 
#   
#     # both threads completely executed 
#     print("Done!") 


