import math
import time
import random
import pygame
from pygame.locals import *
import numpy
import numpy.random as rand

# Screen constants
BLOCK_RES = 15
GRID_X = 5
GRID_Y = 5
# MAP_WIDTH = (((GRID_X // 2) * 2 + 1)*BLOCK_RES)
# MAP_HEIGHT = (((GRID_Y // 2) * 2 + 1)*BLOCK_RES)
screen_size = (((GRID_X // 2) * 2 + 1), ((GRID_Y // 2) * 2 + 1))

screen_color = (217, 217, 217)
wall_color = (0, 0, 0)
player_color = (0, 170, 255)
goal_color = (255, 0, 0)

# Grid constants
columns, rows = screen_size[0], screen_size[1]

print("X: " + str(columns) + ", Y: " + str(rows))

def new_maze(width=30, height=30, complexity=.4, density=.4):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    # number of components
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    # size of components
    density = int(density * ((shape[0] // 2) * (shape[1] // 2)))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=int)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x = rand.randint(0, shape[1] // 2) * 2
        y = rand.randint(0, shape[0] // 2) * 2  # pick a random position
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:
                neighbours.append((y, x - 2))
            if x < shape[1] - 2:
                neighbours.append((y, x + 2))
            if y > 1:
                neighbours.append((y - 2, x))
            if y < shape[0] - 2:
                neighbours.append((y + 2, x))
            if len(neighbours):
                y_, x_ = neighbours[rand.randint(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z

maze = new_maze(screen_size[0], screen_size[1])

x = screen_size[0]//2
y = screen_size[1]//2

maze[y][x] = 2

print(maze)
