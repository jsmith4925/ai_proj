import pygame
from pygame.locals import *
import time

pygame.init()
player = pygame.image.load("resources/images/block.png")
screen = pygame.display.set_mode((480,500))
xpos = 200
ypos = 200
running = 1
while running:
    pygame.display.set_caption('driving')
    screen.fill(0)

    screen.blit(player,(xpos,ypos))

    pygame.display.flip()



    for event in pygame.event.get():
    # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key==K_LEFT:
                xpos-= 5
            elif event.key==K_RIGHT:
                xpos+= 5
            elif event.key==K_UP:
                ypos-=5
            elif event.key==K_DOWN:
                ypos+= 5
