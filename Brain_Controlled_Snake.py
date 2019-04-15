
# coding: utf-8

# In[ ]:


import pygame,sys
import win32api,win32console,win32gui,codecs
import time,random
from pygame.sprite import Sprite

import struct
import socket
import codecs
import time


# In[ ]:


pygame.init()

win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win,0)

white = (0,0,0)
black = (255,255,255)
red = (255,0,0)
green = (0,155,0)

display_width = 1000
display_height = 600

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Brain Controlled Snake")

icon=pygame.image.load("Downloads\_applehead2.png")
pygame.display.set_icon(icon)

img=pygame.image.load("Downloads\_snakehead2.png")
appleimg=pygame.image.load("Downloads\_applehead2.png")

clock = pygame.time.Clock()

AppleThickness=50
block_size = 40
FPS = 60

direction="right"

smallfont = pygame.font.SysFont("lato",25)
medfont = pygame.font.SysFont("lato",50)
largefont = pygame.font.SysFont("lato",80)

def game_intro():
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    intro=False
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        
        message_to_screen("Brain Controlled Snake",green,-10,"large")
        message_to_screen("Press C to play, P to pause or Q to quit",black,70)
        pygame.display.update()
        clock.tick(15)

def pause():
    paused=True
    
    message_to_screen("Paused",black,-100,size="large")
    message_to_screen("Press C to continue or Q to quit",black,25)

    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    paused=False
                elif event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        
        clock.tick(5)
    
def score(score):

    text=smallfont.render("Score: "+str(score),True,black)
    gameDisplay.blit(text,[0,0])

def randAppleGen():

    randApplex = round(random.randrange(0,display_width-AppleThickness))#/10.0)*10.0
    randAppley = round(random.randrange(0,display_height-AppleThickness))#/10.0)*10.0
    return randApplex,randAppley

def snake(block_size,snakeList):

    if direction=="right":
        head=pygame.transform.rotate(img,270)
    if direction=="left":
        head=pygame.transform.rotate(img,90)
    if direction=="up":
        head=img
    if direction=="down":
        head=pygame.transform.rotate(img,180)

    gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, (XnY[0],XnY[1],block_size,block_size))
    
def text_objects(text,color,size):

    if size=="small":
        textSurface=smallfont.render(text,True,color)
    elif size=="medium":
        textSurface=medfont.render(text,True,color)
    elif size=="large":
        textSurface=largefont.render(text,True,color)
    return textSurface,textSurface.get_rect()
    
def message_to_screen(msg,color,y_displace=0,size="small"):

    textSurf,textRect=text_objects(msg,color,size)
    textRect.center=(display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf,textRect)

def _getDecDigit(digit):
    digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    for x in range(len(digits)):
        if digit.lower() == digits[x]:
            return(x)
        
def hexToDec(hexNum):
    decNum = 0
    power = 0
    
    for digit in range(len(hexNum), 0, -1):
        try:
            decNum = decNum + 16 ** power * _getDecDigit(hexNum[digit-1])
            power += 1
        except:
            return
    return(int(decNum))

def eeg_wave():

    UDP_IP = "192.168.0.13"
    UDP_PORT = 2003
    sock = socket.socket(socket.AF_INET,  # Internet
                        socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))
    stocker = []
    counter = 0
    
    while True:
        data, addr = sock.recvfrom(1024)
        
        if 'alpha_absolute' in str(data):

            newData = str(data).split(",")
            newData = newData[1].split("x")
            newData = newData[1:]
            outData = []
            
            for i in newData:
                outData += [hexToDec(i[:-1])]
            newerOut = []
            
            for i in outData:
                if type(i) == int and i > 0:
                    newerOut += [i]

            if len(newerOut) == 0:
                continue

            stocker += [sum(newerOut)/len(newerOut)]
            counter += 1

            if counter == 2:
                s = sum(stocker)/len(stocker)
                if s == sum(newerOut)/len(newerOut):
                    return(1)
                else:
                    return(0)
                
                
def gameLoop():
    
    global direction
    
    direction="right"
    running = True
    gameOver= False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0

    snakeList=[]
    snakeLength=1

    randApplex,randAppley=randAppleGen()
    
    prev = ""
    count = 0
    time_start = 0
    
    while running:
        
        if gameOver==True:
            message_to_screen("Game over",red,-50,size="large")
            message_to_screen("Press C to play again or Q to quit",black,50,size="medium")
            pygame.display.update()
            
        while gameOver==True:
            #gameDisplay.fill(white)
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    gameOver=False
                    running=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        running=False
                        gameOver=False
                    if event.key==pygame.K_c:
                        gameLoop()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

                
        out = eeg_wave()
        
        if out == 0:
            pass
        elif out == 1 and (time.clock() - time_start) > 1:
            if prev == "left":
                direction = "up"
                lead_x_change = 0
                lead_y_change = -block_size
                time_start = time.clock()
            elif prev == "up":
                direction="right"
                lead_x_change = block_size
                lead_y_change = 0
                time_start = time.clock()
            elif prev == "right":
                direction="down"
                lead_x_change = 0
                lead_y_change = block_size
                time_start = time.clock()
            elif prev == "down":
                direction="left"
                lead_x_change = -block_size
                lead_y_change = 0
                time_start = time.clock()
                
        prev = direction
        
        if lead_x >= display_width or lead_x < 0 or lead_y < 0 or lead_y >= display_height:
            gameOver=True
        
        lead_x += lead_x_change
        lead_y += lead_y_change
        

        gameDisplay.fill(white)
        gameDisplay.blit(appleimg,(randApplex,randAppley))
        
        snakeHead=[]
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList)>snakeLength:
            del snakeList[0]
        for eachSegment in snakeList[:-1]:
            if eachSegment==snakeHead:
                gameOver=True
                
        snake(block_size,snakeList)

        score(snakeLength-1)

        pygame.display.update()

        if lead_x > randApplex and lead_x < randApplex + AppleThickness or lead_x + block_size > randApplex and lead_x + block_size<randApplex+AppleThickness:
            if lead_y > randAppley and lead_y < randAppley + AppleThickness:
                randApplex,randAppley = randAppleGen()
                snakeLength+=1
            elif lead_y+block_size > randAppley and lead_y+block_size<randAppley+AppleThickness:
                randApplex,randAppley=randAppleGen()
                snakeLength+=1

        clock.tick(FPS)
    
    pygame.quit()
    quit()
    

game_intro()
gameLoop()

