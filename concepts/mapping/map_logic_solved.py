import math
import time
import random
import pygame
from pygame.locals import *
import numpy
import numpy.random as rand

def new_maze(width=30, height=30, complexity=.4, density=.4):
    # Only odd shapes
    shape = ((height // 2) * 2 +1, (width // 2) * 2 +1)
    # Adjust complexity and density relative to maze size
    # number of components
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    # size of components
    density = int(density * ((shape[0] // 2) * (shape[1] // 2)))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = rand.randint(0, shape[1] // 2) * 2, rand.randint(0,
                                                shape[0] // 2) * 2  # pick a random position
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

def new_blank_maze(width=30, height=30, complexity=.7, density=.7):
    # Only odd shapes
    shape = ((height // 2) * 2 +1, (width // 2) * 2 +1)
    # Adjust complexity and density relative to maze size
    # number of components
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    # size of components
    density = int(density * ((shape[0] // 2) * (shape[1] // 2)))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1

    return Z

# Convert matrix of ints to colour map
def draw_maze(grid):
    # Set colors.
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    screen.fill(WHITE)
    pygame.draw.rect(screen, (255, 255, 255, 255), [
                     MARGIN, MARGIN, sizeX, sizeY])
    # pygame.draw.rect(Surface, color, Rect, width=0)

    # Fill the grid
    for x in range(((SECT_X_COUNT // 2) * 2 +1)):
        for y in range(((SECT_Y_COUNT // 2) * 2 +1)):
            if grid[y][x] == False:
                pygame.draw.rect(screen, WHITE, [
                                 MARGIN+1+(x*SECTOR_AREA), MARGIN+1+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
            if grid[y][x] == True:
                pygame.draw.rect(screen, BLACK, [
                                 MARGIN+1+(x*SECTOR_AREA), MARGIN+1+(y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)

    #Draw Centre
    grid_middle_x = (SECT_X_COUNT // 2)
    grid_middle_y = (SECT_Y_COUNT // 2)

    if grid[grid_middle_y][grid_middle_x] == False:
        pygame.draw.rect(screen, RED, [
                            MARGIN+1+(grid_middle_x*SECTOR_AREA), MARGIN+1+(grid_middle_y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
    else:
        pygame.draw.rect(screen, RED, [
                            MARGIN+1+((grid_middle_x)*SECTOR_AREA), MARGIN+1+((grid_middle_y+1)*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)

    return grid


if __name__ == "__main__":
    #   Setting Constants
    # Produces a matrix of true or false values in a matrix

    # Set grid square area here: Smallest SECTOR_AREA: 5.
    SECTOR_AREA = 30
    MARGIN = 10
    # Resolution of the grid (Minimum 3)
    SECT_X_COUNT = 10
    SECT_Y_COUNT = 10

    # Calculations to set size.
    sizeX = (MARGIN*2)+(((SECT_X_COUNT // 2) * 2 +1)*SECTOR_AREA)
    sizeY = (MARGIN*2)+(((SECT_Y_COUNT // 2) * 2 +1)*SECTOR_AREA)
    size = (sizeX, sizeY)
    grid = []
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    grid = draw_maze(new_blank_maze(SECT_X_COUNT, SECT_Y_COUNT))
    pygame.display.flip()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RCTRL:
                    print("========New Game======")
                    grid = draw_maze(new_maze(SECT_X_COUNT, SECT_Y_COUNT))
                    pygame.display.flip()
                if event.key == K_LCTRL:
                    print("========New Game======")
                    grid = draw_maze(new_blank_maze(SECT_X_COUNT, SECT_Y_COUNT))
                    pygame.display.flip()
                if event.key == K_p:
                    print(grid)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = (pos[0]- MARGIN) // SECTOR_AREA                
                row = (pos[1]- MARGIN) // SECTOR_AREA 
                # Set that location 
                if grid[row][column] == False:
                    grid[row][column] = True
                elif grid[row][column] == True:
                    grid[row][column] = False
                grid = draw_maze(grid)
                pygame.display.flip()    
            
            elif event.type == QUIT:
                running = False

