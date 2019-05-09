import pygame
from pygame.locals import *
import time

pygame.init()
player = pygame.image.load("driving/resources/images/block.png")
screen = pygame.display.set_mode((480,500))
xpos = 200
ypos = 200
keys=[False,False,False,False]


running = 1
while running:
    pygame.display.set_caption('driving')
    screen.fill(0)
    time.sleep(0.02)
    

    screen.blit(player,(xpos,ypos))
    pygame.display.flip()

    if keys[0]==True:
        xpos-= 5
    if keys[1]==True:
        xpos+= 5
    if keys[2]==True:
        ypos-= 5
    if keys[3]==True:
        ypos+= 5



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
            if event.key==K_LEFT:
                keys[0]=False
            elif event.key==K_RIGHT:
                keys[1]=False
            elif event.key==K_UP:
                keys[2]=False
            elif event.key==K_DOWN:
                keys[3]=False
