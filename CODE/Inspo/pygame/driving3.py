import pygame
from pygame.locals import *
import time
import math

pygame.init()
player = pygame.image.load("driving/resources/images/block.png")
screen = pygame.display.set_mode((480,500))
xpos = 200
ypos = 200
keys=[False,False,False,False]
direction = 0
forward = 0

running = 1
while running:
    pygame.display.set_caption('driving')
    screen.fill(1)

    
    if keys[0]==True:
        direction-= 2
    if keys[1]==True:
        direction+= 2
    if keys[2]==True:
        forward+= 0.2
    if keys[3]==True and forward >= 0:
        forward-= 0.2
    
    movex=math.cos(direction/57.29)*forward
    movey=math.sin(direction/57.29)*forward
    xpos+=movex
    ypos-=movey

    playerrot = pygame.transform.rotate(player,direction)
    screen.blit(playerrot, (xpos,ypos))
    pygame.display.flip()
    time.sleep(0.02)

    for event in pygame.event.get():
    # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
            
        if event.type == pygame.KEYDOWN:
            if event.key==K_LEFT:
                keys[0]=True
            elif event.key==K_RIGHT:
                keys[1]=True
            elif event.key==K_UP:
                keys[2]=True
            elif event.key==K_DOWN:
                keys[3]=True

        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                keys[0]=False
            elif event.key==pygame.K_RIGHT:
                keys[1]=False
            elif event.key==pygame.K_UP:
                keys[2]=False
            elif event.key==pygame.K_DOWN:
                keys[3]=False
