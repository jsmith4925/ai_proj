import math
import time
import random

import pygame
from pygame.locals import *
import numpy as np
#   Setting Constants
# Set colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRASS_GREEN = (51, 204, 51)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
LIGHT_RED = (255, 128, 128)
ROAD_BROWN = (102, 70, 70)
AUBURN = (165,42,42)

# Set block types
UNSET = 0
ROUTE = 1
WALL = 2
GOAL = 3
XX = 9  # out of bounds
#temp way of finding direction
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# Set grid square area here: Smallest SECTOR_AREA: 5.
SECTOR_AREA = 45
MARGIN = 50
# Resolution of the grid (Minimum 3)
SECT_X_COUNT = 8
SECT_Y_COUNT = 6

pygame.init()
running = True

# Calculations to set size.
sizeX = MARGIN+SECT_X_COUNT*SECTOR_AREA
sizeY = MARGIN+SECT_Y_COUNT*SECTOR_AREA
size = (sizeX, sizeY)
screen = pygame.display.set_mode(size)
grid = []

# #Format to int count starting at 0
# SECT_X_COUNT -= 1
# SECT_Y_COUNT -= 1

def new_start():
    edge_rows = [[random.randint(0, SECT_Y_COUNT-1),0],
                 [random.randint(0, SECT_Y_COUNT-1),SECT_X_COUNT-1],
                 [0, random.randint(0, SECT_X_COUNT-1)],
                 [SECT_Y_COUNT-1, random.randint(0, SECT_X_COUNT-1)]
                 ]
    return edge_rows[random.randint(0, 3)]


def get_adjacent_values(full_grid, current_Y, current_X):
    values = [XX, XX, XX, XX]
    # current position = full_grid[current_X][current_Y]]
    # with out of bounds check
    # North
    if current_Y < SECT_Y_COUNT-1:
        values[2] = full_grid[current_Y+1][current_X]
    # East
    if current_X < SECT_X_COUNT-1:
        values[1] = full_grid[current_Y][current_X+1]
    # South
    if current_Y > 0:
        values[0] = full_grid[current_Y-1][current_X]
    # West
    if current_X > 0:
        values[3] = full_grid[current_Y][current_X-1]
    # returns a 4 digit array - [N, E, S, W]
    return values


def new_maze():
    # make a new empty map
    grid = [[0] * ((SECT_X_COUNT)) for i in range((SECT_Y_COUNT))]
    # Set surrounding wall
    for column in range(SECT_X_COUNT):
        grid[0][column] = WALL
        grid[SECT_Y_COUNT-1][column] = WALL

    for row in range(SECT_Y_COUNT):
        grid[row][0] = WALL
        grid[row][SECT_X_COUNT-1] = WALL

    # Set Start Location
    start = new_start()
    while get_adjacent_values(grid, start[0], start[1]).count(XX) > 1:
        start = new_start()
    grid[start[0]][start[1]] = GOAL

    # Set Finish Location
    finish = new_start()
    while (
        start == finish or
        get_adjacent_values(grid, finish[0], finish[1]).count(GOAL) > 0 or
        get_adjacent_values(grid, finish[0], finish[1]).count(XX) > 1
    ):  # Potenitally add a 'same wall' check if maps appear too simple?
        finish = new_start()

    grid[finish[0]][finish[1]] = GOAL
    # The entrance to the finish always needs to be clear
    # we set this as road by default here
    print("Start: " + str(start))
    print("Finish: " + str(finish))
    # Plan Route
    grid_complete = plan_route(grid, start, finish)
    return grid

def plan_route(grid, current, finish):

    print(get_adjacent_values(grid, current[0], current[1]))
    

    return grid

#Convert matrix of ints to colour map
def draw_maze(grid):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, [25, 25, sizeX-49, sizeY-49], 2)
    # Fill the grid
    for x in range(SECT_X_COUNT):
        for y in range(SECT_Y_COUNT):
            if grid[y][x] == UNSET:
                pygame.draw.rect(screen, GRASS_GREEN, [
                                 26+(x*SECTOR_AREA), 26+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
            elif grid[y][x] == ROUTE:
                pygame.draw.rect(screen, ROAD_BROWN, [
                                 26+(x*SECTOR_AREA), 26+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
            elif grid[y][x] == WALL:
                pygame.draw.rect(screen, GREEN, [
                                 26+(x*SECTOR_AREA), 26+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
            elif grid[y][x] == GOAL:
                pygame.draw.rect(screen, AUBURN, [
                                 26+(x*SECTOR_AREA), 26+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
    return grid


grid = draw_maze(new_maze())
pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_RCTRL:
                grid = draw_maze(new_maze())
                pygame.display.flip()
            if event.key == K_p:
                print(grid)
        elif event.type == QUIT:
            running = False
