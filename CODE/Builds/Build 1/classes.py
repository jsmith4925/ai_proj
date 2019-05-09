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
BLOCK_RES = 30  # >5
MAP_PADDING = 5
GRID_X = 7
GRID_Y = 7

MAP_WIDTH = (MAP_PADDING*2)+(((GRID_X // 2) * 2 + 1)*BLOCK_RES)
MAP_HEIGHT = (MAP_PADDING*2)+(((GRID_Y // 2) * 2 + 1)*BLOCK_RES)


# Draw command for moving box set to Sprite#
class Player:
    x = BLOCK_RES + (MAP_PADDING * 1.1)
    y = BLOCK_RES + (MAP_PADDING * 1.1)
    speed = 0.1

    def moveRight(self):
        self.x = self.x + self.speed

    def moveLeft(self):
        self.x = self.x - self.speed

    def moveUp(self):
        self.y = self.y - self.speed

    def moveDown(self):
        self.y = self.y + self.speed


class Arena:
    def __init__(self):
        self.arena = new_maze(GRID_X, GRID_Y)
        self.walls = []

    def new_arena(self):
        self.arena = new_maze(GRID_X, GRID_Y)

    def new_empty_arena(self):
        self.arena = new_blank_maze(GRID_X, GRID_Y)

    def draw_arena(self, _display_screen):
        # Set colors.
        WALL = (0, 0, 0)
        GOAL = (255, 0, 255)

        # Fill the self.arena
        for x in range(((GRID_X // 2) * 2 + 1)):
            for y in range(((GRID_Y // 2) * 2 + 1)):
                if self.arena[y][x] == True:  # Is Wall
                    pygame.draw.rect(_display_screen, WALL,
                                     [MAP_PADDING+1+(x*BLOCK_RES),
                                      MAP_PADDING+1 +
                                      (y*BLOCK_RES),
                                         BLOCK_RES,
                                         BLOCK_RES], 0)

        # Draw Centre
        maze_middle_x = (GRID_X // 2)
        maze_middle_y = (GRID_Y // 2)
        if self.arena[maze_middle_y][maze_middle_x] == False:
            pygame.draw.rect(_display_screen, GOAL,
                             [MAP_PADDING+1+(maze_middle_x*BLOCK_RES),
                              MAP_PADDING+1+(maze_middle_y*BLOCK_RES),
                              BLOCK_RES,
                              BLOCK_RES], 0)
        elif self.arena[maze_middle_y+1][maze_middle_x] == False:
            pygame.draw.rect(_display_screen, GOAL,
                             [MAP_PADDING+1+(maze_middle_x*BLOCK_RES),
                              MAP_PADDING+1+((maze_middle_y+1)*BLOCK_RES),
                              BLOCK_RES,
                              BLOCK_RES], 0)
        elif self.arena[maze_middle_y][maze_middle_x+1] == False:
            pygame.draw.rect(_display_screen, GOAL,
                             [MAP_PADDING+1+((maze_middle_x+1)*BLOCK_RES),
                              MAP_PADDING+1+(maze_middle_y*BLOCK_RES),
                              BLOCK_RES,
                              BLOCK_RES], 0)
        elif self.arena[maze_middle_y-1][maze_middle_x-1] == False:
            pygame.draw.rect(_display_screen, GOAL,
                             [MAP_PADDING+1+((maze_middle_x-1)*BLOCK_RES),
                              MAP_PADDING+1+((maze_middle_y-1)*BLOCK_RES),
                              BLOCK_RES,
                              BLOCK_RES], 0)


class Program:

    def __init__(self):
        self.running = True
        self._display_screen = None
        self._images = None
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.player = Player()
        self.arena = Arena()
        self.arena.new_arena()

    def on_init(self):
        pygame.init()
        size = (MAP_WIDTH, MAP_HEIGHT)
        self._display_screen = pygame.display.set_mode(size)
        pygame.display.set_caption('AI Maze')
        self._running = True
        self._images = pygame.image.load("Build\images\\robbert.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_screen.fill((217, 217, 217))
        self.arena.draw_arena(self._display_screen)
        self._images = pygame.transform.scale(
            self._images,
            (math.floor(BLOCK_RES*0.8),
             math.floor(BLOCK_RES*0.8))
        )
        self._display_screen.blit(self._images, (self.player.x, self.player.y))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def start(self):
        if self.on_init() is False:
            self._running = False
        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if (keys[K_ESCAPE]):
                self._running = False

            if (keys[K_RCTRL]):
                self.arena.new_arena()
                self.arena.draw_arena(self._display_screen)
                pygame.display.flip()

            if (keys[K_LCTRL]):
                self.arena.new_empty_arena()
                self.arena.draw_arena(self._display_screen)
                pygame.display.flip()

            if (keys[K_RIGHT]):
                self.player.moveRight()

            if (keys[K_LEFT]):
                self.player.moveLeft()

            if (keys[K_UP]):
                self.player.moveUp()

            if (keys[K_DOWN]):
                self.player.moveDown()

            self.on_render()
            self.on_loop()
        self.on_cleanup()


if __name__ == "__main__":
    Game = Program()
    Game.start()
