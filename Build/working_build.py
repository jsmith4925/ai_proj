import math
import time
import random
import pygame
from pygame.locals import *
import numpy
import numpy.random as rand
from arena_functions import *
import sys
import os

# GLOBAL CONSTANTS
BLOCK_RES = 20  # >5
MAP_PADDING = 5
GRID_X = 10
GRID_Y = 10

MAP_WIDTH = (MAP_PADDING*2)+(((GRID_X // 2) * 2 + 1)*BLOCK_RES)
MAP_HEIGHT = (MAP_PADDING*2)+(((GRID_Y // 2) * 2 + 1)*BLOCK_RES)

# Class for the orange dude


class Player(object):

    def __init__(self):
        x = BLOCK_RES + (MAP_PADDING * 1.2)
        y = BLOCK_RES + (MAP_PADDING * 1.2)
        self.rect = pygame.Rect(x, y, BLOCK_RES*0.8, BLOCK_RES*0.8)

    def reset(self):
        self.rect.x = BLOCK_RES + (MAP_PADDING * 1.2)
        self.rect.y = BLOCK_RES + (MAP_PADDING * 1.2)

    def move(self, dx, dy):
        # Move each axis separately.
        # Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom


# Nice class to hold a wall rect
class Wall(object):

    def __init__(self, x, y):
        walls.append(self)
        self.rect = pygame.Rect(MAP_PADDING+1+(x*BLOCK_RES),
                                MAP_PADDING+1 + (y*BLOCK_RES),
                                BLOCK_RES,
                                BLOCK_RES)


# Convert matrix of ints to colour map
def draw_maze(grid):
    WALL = (0, 0, 0)
    GOAL = (255, 0, 255)
    screen.fill((217, 217, 217))
    # Fill the self.arena
    for x in range(((GRID_X // 2) * 2 + 1)):
        for y in range(((GRID_Y // 2) * 2 + 1)):
            if grid[y][x] == True:  # Is Wall
                # pygame.draw.rect(screen, WALL,
                #                  [MAP_PADDING+1+(x*BLOCK_RES),
                #                      MAP_PADDING+1 +
                #                      (y*BLOCK_RES),
                #                   BLOCK_RES,
                #                   BLOCK_RES], 0)
                Wall(x, y)

    return grid


def draw_rect(x, y):
    pygame.draw.rect(screen, (217, 217, 217),
                     [MAP_PADDING+1+(x*BLOCK_RES),
                      MAP_PADDING+1 + (y*BLOCK_RES),
                      BLOCK_RES,
                      BLOCK_RES], 0)


def clean_maze(grid, x, y):
    WALL = (0, 0, 0)
    GOAL = (255, 0, 255)
    # screen.fill((217, 217, 217))
    # Fill the self.arena
    x = (x - MAP_PADDING) // BLOCK_RES
    y = (y - MAP_PADDING) // BLOCK_RES

    for px in range(x-1, x+2):
        for py in range(y-1, y+2):
            if grid[py][px] == False:  # Is Wall
                draw_rect(px, py)


def get_end_rect(grid):
    maze_middle_x = (GRID_X // 2)
    maze_middle_y = (GRID_Y // 2)
    if grid[maze_middle_y][maze_middle_x] == False:
        end_rect = pygame.Rect(MAP_PADDING+1+(maze_middle_x*BLOCK_RES),
                               MAP_PADDING+1 + (maze_middle_y*BLOCK_RES),
                               BLOCK_RES,
                               BLOCK_RES)
    elif grid[maze_middle_y+1][maze_middle_x] == False:
        end_rect = pygame.Rect(MAP_PADDING+1+(maze_middle_x*BLOCK_RES),
                               MAP_PADDING+1 + (maze_middle_y+1*BLOCK_RES),
                               BLOCK_RES,
                               BLOCK_RES)
    elif grid[maze_middle_y][maze_middle_x+1] == False:
        end_rect = pygame.Rect(MAP_PADDING+1+(maze_middle_x+1*BLOCK_RES),
                               MAP_PADDING+1 + (maze_middle_y*BLOCK_RES),
                               BLOCK_RES,
                               BLOCK_RES)
    elif grid[maze_middle_y-1][maze_middle_x-1] == False:
        end_rect = pygame.Rect(MAP_PADDING+1+(maze_middle_x-1*BLOCK_RES),
                               MAP_PADDING+1 + (maze_middle_y-1*BLOCK_RES),
                               BLOCK_RES,
                               BLOCK_RES)

    return end_rect


pygame.init()
clock = pygame.time.Clock()

running = True
grid = []
walls = []
player = Player()
size = (MAP_WIDTH, MAP_HEIGHT)
screen = pygame.display.set_mode(size)
grid = draw_maze(new_blank_maze(GRID_X, GRID_Y))
end_rect = get_end_rect(grid)
pygame.display.flip()

while running:
    clock.tick(60)
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    clean_maze(grid, player.rect.x, player.rect.y)

    if player.rect.colliderect(end_rect):
        print("========New Game======")
        walls = []
        player.reset()
        grid = draw_maze(new_maze(GRID_X, GRID_Y))
        pygame.display.flip()

    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall.rect)
    end_rect = get_end_rect(grid)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (0, 170, 255), player.rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

            if event.key == K_RCTRL:
                print("========New Game======")
                walls = []
                player.reset()
                grid = draw_maze(new_maze(GRID_X, GRID_Y))
                pygame.display.flip()

            if event.key == K_LCTRL:
                print("========New Game======")
                walls = []
                player.reset()
                grid = draw_maze(new_blank_maze(GRID_X, GRID_Y))
                pygame.display.flip()

            if event.key == K_p:
                print(grid)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = (pos[0] - MAP_PADDING) // BLOCK_RES
            row = (pos[1] - MAP_PADDING) // BLOCK_RES
            # Set that location
            if grid[row][column] == False:
                grid[row][column] = True

            elif grid[row][column] == True:
                grid[row][column] = False

            draw_maze(grid)
            pygame.display.flip()

        elif event.type == QUIT:
            running = False
        # Move the player if an arrow key is pressed
