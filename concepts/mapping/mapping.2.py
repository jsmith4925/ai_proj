import math
import time
import random

import pygame
from pygame.locals import *

#   Setting Constants
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

#Set block types
UNSET = 0
ROUTE = 1
WALL = 2
GOAL = 3
XX = 9 # out of bounds

# Set grid square area here: Smallest SECTOR_AREA: 5.
SECTOR_AREA = 50
MARGIN = 50
# Resolution of the grid
SECT_Y_COUNT = 8
SECT_X_COUNT = 8

pygame.init()
running = True

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

def get_adjacent_values(full_grid, current_X, current_Y):
    values = [XX,XX,XX,XX]
    #current position = full_grid[current_X][current_Y]]
    #with out of bounds check
    #North
    if current_Y < SECT_Y_COUNT-1:
        values[0] = full_grid[current_X][current_Y+1]
    #East
    if current_X < SECT_X_COUNT-1:
        values[1] = full_grid[current_X+1][current_Y]
    #South
    if current_Y > 0:
        values[2] = full_grid[current_X][current_Y-1]
    #West
    if current_X > 0:
        values[3] = full_grid[current_X-1][current_Y]
    # returns a 4 digit array - [N, E, S, W]
    return values


def new_maze():
    #make a new empty map
    grid=[]
    for x in range(SECT_X_COUNT):
        grid.append([])
        for y in range(SECT_Y_COUNT):
            grid[x].append(UNSET)
    #Set surrounding wall
    for row in range(SECT_X_COUNT):
        grid[0][row] = WALL
        grid[row][SECT_X_COUNT-1] = WALL
        for column in range(SECT_Y_COUNT):
            grid[column][0] = WALL
            grid[SECT_Y_COUNT-1][column] =WALL
    #Set Start Location
    start = new_start()    
    grid[start[0]][start[1]]=GOAL
    while get_adjacent_values(grid, start[0],start[1]).count(XX) > 1:
        grid[start[0]][start[1]]=WALL        
        start = new_start()    
        grid[start[0]][start[1]]=GOAL
    #Set Finish Location
    finish = new_start()
    grid[finish[0]][finish[1]]=GOAL
    while (
        start == finish or
        get_adjacent_values(grid, finish[0],finish[1]).count(GOAL) > 0 or
        get_adjacent_values(grid, finish[0],finish[1]).count(XX) > 1
    ):    #Potenitally add a 'same wall' check if maps appear too simple
        print("Caught Collision")
        grid[finish[0]][finish[1]]=WALL
        finish = new_start()
        grid[finish[0]][finish[1]]=GOAL
    # The entrance to the finish always needs to be clear
    # we set this as road by default here

    #Plan Route

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, [25, 25, sizeX-49, sizeY-49], 2)
    # Fill the grid
    for x in range(SECT_X_COUNT):
        for y in range(SECT_Y_COUNT):
            if grid[x][y] == UNSET:
                pygame.draw.rect(screen, GRASS_GREEN, [26+(y*SECTOR_AREA),26+(x*SECTOR_AREA),SECTOR_AREA,SECTOR_AREA], 0)
            elif grid[x][y] == ROUTE:
                pygame.draw.rect(screen, ROAD_BROWN, [26+(y*SECTOR_AREA),26+(x*SECTOR_AREA),SECTOR_AREA,SECTOR_AREA], 0)
            elif grid[x][y] == WALL:
                pygame.draw.rect(screen, GREEN, [26+(y*SECTOR_AREA),26+(x*SECTOR_AREA),SECTOR_AREA,SECTOR_AREA], 0)
            elif grid[x][y] == GOAL:
                pygame.draw.rect(screen, RED, [26+(y*SECTOR_AREA),26+(x*SECTOR_AREA),SECTOR_AREA,SECTOR_AREA], 0)
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

    pygame.display.flip()