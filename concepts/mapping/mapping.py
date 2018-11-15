import math
import time

import pygame
from pygame.locals import *

# Set colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRASS_GREEN = (51, 204, 51)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
LIGHT_RED    =(255,128,128)
ROAD_BROWN = (83, 64, 45)

pygame.init()
running = True
#
#   Setting Constants
# Set grid square area here: Smallest space: 5.
SECTOR_AREA = 50
MARGIN = 50
# Resolution of the grid
SECT_Y_COUNT = 10
SECT_X_COUNT = 10

# Calculations to set size.
sizeX = MARGIN+SECT_Y_COUNT*SECTOR_AREA
sizeY = MARGIN+SECT_X_COUNT*SECTOR_AREA
size = (sizeX, sizeY)
screen = pygame.display.set_mode(size)
grid = []

clock = pygame.time.Clock()
screen.fill(WHITE)
pygame.draw.rect(screen, BLACK, [25, 25, sizeX-49, sizeY-49], 2)

#Draw the grid.
    #Vertical lines.
for x in range(SECT_Y_COUNT):
    pygame.draw.line(screen,BLACK,[(x*SECTOR_AREA+25),25],[(x*SECTOR_AREA+25),sizeY-25],2)
    #Horizontal lines.
for x in range(SECT_X_COUNT):
    pygame.draw.line(screen,BLACK,[25,(x*SECTOR_AREA+25)],[sizeX-25,(x*SECTOR_AREA+25)],2)



pygame.display.flip()
print(grid)



while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
