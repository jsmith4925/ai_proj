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
BLUE = (51, 144, 255)
PURPLE = (128, 0, 128)
LIGHT_RED = (183, 75, 75)
ROAD_BROWN = (102, 70, 70)

# Set block types
UNSET = 0
ROUTE = 1
WALL = 2
GOAL = 3
START = 4
XX = 9  # out of bounds
# temp way of finding direction
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# Set grid square area here: Smallest SECTOR_AREA: 5.
SECTOR_AREA = 35
MARGIN = 10
# Resolution of the grid (Minimum 3)
SECT_X_COUNT = 5
SECT_Y_COUNT = 7

pygame.init()
running = True

# Calculations to set size.
sizeX = (MARGIN*2)+(SECT_X_COUNT*SECTOR_AREA)
sizeY = (MARGIN*2)+(SECT_Y_COUNT*SECTOR_AREA)
size = (sizeX, sizeY)
screen = pygame.display.set_mode(size)
grid = []

# #Format to int count starting at 0
# SECT_X_COUNT -= 1
# SECT_Y_COUNT -= 1


def new_start():
    edge_rows = [[random.randint(0, SECT_Y_COUNT-1), 0],
                 [random.randint(0, SECT_Y_COUNT-1), SECT_X_COUNT-1],
                 [0, random.randint(0, SECT_X_COUNT-1)],
                 [SECT_Y_COUNT-1, random.randint(0, SECT_X_COUNT-1)]
                 ]
    return edge_rows[random.randint(0, 3)]


def get_adjacent_values(full_grid, current):
    values = [XX, XX, XX, XX]
    # with out of bounds check
    # North
    if current[0] > 0:
        values[0] = full_grid[current[0]-1][current[1]]
    # East
    if current[1] < SECT_X_COUNT-1:
        values[1] = full_grid[current[0]][current[1]+1]
    # South
    if current[0] < SECT_Y_COUNT-1:
        values[2] = full_grid[current[0]+1][current[1]]
    # West
    if current[1] > 0:
        values[3] = full_grid[current[0]][current[1]-1]
    # returns a 4 digit array - [N, E, S, W]
    return values


def return_random_unset(adjecent_values):
    directions = [i for i, e in enumerate(adjecent_values) if e == UNSET] #the location of the UNSET values in the list
    if directions:
        move = random.choice(directions)
    else:
        move = XX
    return move


def set_block_as_choice(grid, current, direction, block_type):

    if direction == NORTH:
        grid[current[0]-1][current[1]] = block_type
    elif direction == EAST:
        grid[current[0]][current[1]+1] = block_type
    elif direction == SOUTH:
        grid[current[0]+1][current[1]] = block_type
    elif direction == WEST:
        grid[current[0]][current[1]-1] = block_type
    elif direction == XX:
        print("NO MOVE WE COMPLETE")

    return grid


def plan_route(grid, current, finish):
    # [N,E,S,W]
    #ToDo While end not found loop
    move = return_random_unset(get_adjacent_values(grid, current))
    # next_current = current + move
    grid = set_block_as_choice(grid, current, move, ROUTE)    
    remaining_unset = [i for i, e in enumerate(get_adjacent_values(grid, current)) if e == UNSET]#remeber last wall here by finding coord of move+current
    if remaining_unset:
        for remaining in remaining_unset:
            set_block_as_choice(grid, current, remaining, WALL)
    
    return grid


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
    while get_adjacent_values(grid, start).count(XX) > 1:
        start = new_start()
    grid[start[0]][start[1]] = START

    # Set Finish Location
    finish = new_start()
    while (
        start == finish or
        get_adjacent_values(grid, finish).count(START) > 0 or
        get_adjacent_values(grid, finish).count(XX) > 1
    ):  # Potenitally add a 'same wall' check if maps appear too simple?
        finish = new_start()
    grid[finish[0]][finish[1]] = GOAL

    # The entrance to the finish always needs to be clear
    # we set this as road by default here
    finish_opening_direction = return_random_unset(get_adjacent_values(grid, finish))
    grid = set_block_as_choice(grid, finish, finish_opening_direction, ROUTE)  # condense me

    # Plan Route
    grid_complete = plan_route(grid, start, finish)

    return grid


# Convert matrix of ints to colour map
def draw_maze(grid):
    screen.fill(WHITE)
    pygame.draw.rect(screen, (255, 255, 255, 255), [
                     MARGIN, MARGIN, sizeX, sizeY])
    # pygame.draw.rect(Surface, color, Rect, width=0)
    # Fill the grid
    for x in range(SECT_X_COUNT):
        for y in range(SECT_Y_COUNT):
            if grid[y][x] == UNSET:
                pygame.draw.rect(screen, GRASS_GREEN, [
                                 MARGIN+1+(x*SECTOR_AREA), MARGIN+1+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
            elif grid[y][x] == ROUTE:
                pygame.draw.rect(screen, ROAD_BROWN, [
                                 MARGIN+1+(x*SECTOR_AREA), MARGIN+1+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
            elif grid[y][x] == WALL:
                pygame.draw.rect(screen, GREEN, [
                                 MARGIN+1+(x*SECTOR_AREA), MARGIN+1+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
            elif grid[y][x] == START:
                pygame.draw.rect(screen, LIGHT_RED, [
                                 MARGIN+1+(x*SECTOR_AREA), MARGIN+1+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
            elif grid[y][x] == GOAL:
                pygame.draw.rect(screen, BLUE, [
                                 MARGIN+1+(x*SECTOR_AREA), MARGIN+1+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
    return grid


grid = draw_maze(new_maze())
pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_RCTRL:
                print("========New Game======")
                grid = draw_maze(new_maze())
                pygame.display.flip()
            if event.key == K_p:
                print(grid)
        elif event.type == QUIT:
            running = False