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
# Set grid square area here: Smallest SECTOR_AREA: 5.
SECTOR_AREA = 20
MARGIN = 50
# Resolution of the grid
SECT_Y_COUNT = 20
SECT_X_COUNT = 20

# Calculations to set size.
sizeX = MARGIN+SECT_Y_COUNT*SECTOR_AREA
sizeY = MARGIN+SECT_X_COUNT*SECTOR_AREA
size = (sizeX, sizeY)
screen = pygame.display.set_mode(size)
grid = []

def new_start():
    edge_rows = [[0,random.randint(0,SECT_X_COUNT-1)],
    [SECT_X_COUNT-1, random.randint(0,SECT_X_COUNT-1)],
    [random.randint(0,SECT_X_COUNT-1),0],
    [random.randint(0,SECT_X_COUNT-1),SECT_X_COUNT-1]
    ]
    return edge_rows[random.randint(0,3)]

def build_road(x, y):
    grid = new_maze()
    if grid[x][y] == 1:
        return False
    if grid[x][y] == 3:
        return False
    elif grid[x][y] == 2:
        return True

    # mark as visited
    grid[x][y] = 1

    # explore neighbors clockwise starting by the one on the right
    if ((x < len(grid)-1 and build_road(x+1, y))
        or (y > 0 and build_road(x, y-1))
        or (x > 0 and build_road(x-1, y))
        or (y < len(grid)-1 and build_road(x, y+1))):
        return True

    return False

def new_maze():
    #make a new round
    grid=[]
    for x in range(SECT_X_COUNT):
        grid.append([])
        for y in range(SECT_Y_COUNT):
            grid[x].append(0)

    start = new_start()    
    finish = new_start()
    while start == finish:
        finish = new_start()
    grid[finish[0]][finish[1]]=2
    grid[start[0]][start[1]]=3

    return grid

grid = new_maze()

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_RCTRL:
                grid = new_maze()
        elif event.type == QUIT:
            running = False
    
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, [25, 25, sizeX-49, sizeY-49], 2)
    # Fill the grid
    for x in range(SECT_X_COUNT):
        for y in range(SECT_Y_COUNT):
            if grid[x][y] == 0:
                pygame.draw.rect(screen, GRASS_GREEN, [26+(y*SECTOR_AREA),26+(x*SECTOR_AREA),SECTOR_AREA,SECTOR_AREA], 0)
            elif grid[x][y] == 1:
                pygame.draw.rect(screen, ROAD_BROWN, [26+(y*SECTOR_AREA),26+(x*SECTOR_AREA),SECTOR_AREA,SECTOR_AREA], 0)
            elif grid[x][y] == 2:
                pygame.draw.rect(screen, RED, [26+(y*SECTOR_AREA),26+(x*SECTOR_AREA),SECTOR_AREA,SECTOR_AREA], 0)

    pygame.display.flip()
