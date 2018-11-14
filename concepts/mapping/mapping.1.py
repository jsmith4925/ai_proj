import math
import time
import random

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
SECTOR_AREA = 100
MARGIN = 50
# Resolution of the grid
SECT_Y_COUNT = 5
SECT_X_COUNT = 5

# Calculations to set size.
sizeX = MARGIN+SECT_Y_COUNT*SECTOR_AREA
sizeY = MARGIN+SECT_X_COUNT*SECTOR_AREA
size = (sizeX, sizeY)
screen = pygame.display.set_mode(size)

grid = []
for x in range(SECT_X_COUNT):
    grid.append([])
    for y in range(SECT_Y_COUNT):
        grid[x].append(0)
print(grid)

currentRow = random.randint(0,SECT_X_COUNT-1)
currentColumn = random.randint(0,SECT_Y_COUNT-1)
print(currentRow)
print(currentColumn)
grid[currentRow][currentColumn] = 1

screen.fill(WHITE)
pygame.draw.rect(screen, BLACK, [25, 25, sizeX-49, sizeY-49], 2)



# Fill the grid
for x in range(SECT_X_COUNT):
    for y in range(SECT_Y_COUNT):
        if grid[x][y] == 0:
            pygame.draw.rect(screen, GRASS_GREEN, [26+(y*SECTOR_AREA),26+(x*SECTOR_AREA),SECTOR_AREA,SECTOR_AREA], 0)
        else:
            pygame.draw.rect(screen, ROAD_BROWN, [26+(y*SECTOR_AREA),26+(x*SECTOR_AREA),SECTOR_AREA,SECTOR_AREA], 0)

pygame.display.flip()



while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
