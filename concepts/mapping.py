import math
import time

import pygame
from pygame.locals import *

# Set colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

pygame.init()
running = True

# Set grid square area here: Smallest space: 5.
sectorArea = 50
# Resolution of the grid
sectorYCount = 10
sectorXCount = 10

sizeX = 50+sectorYCount*sectorArea
sizeY = 50+sectorXCount*sectorArea

# Calculations to et size.
size = (sizeX, sizeY)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
screen.fill(WHITE)
pygame.draw.rect(screen, BLACK, [25, 25, sizeX-49, sizeY-49], 2)

pygame.display.flip()

#Draw the grid.
for x in range(sectorYCount):
    pygame.draw.line(screen,BLACK,[(x*sectorArea+25),25],[(x*sectorArea+25),sizeY-25],2)        #Vertical lines.
for x in range(sectorXCount):
    pygame.draw.line(screen,BLACK,[25,(x*sectorArea+25)],[sizeX-25,(x*sectorArea+25)],2)        #Horizontal lines.

pygame.display.flip()



while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
