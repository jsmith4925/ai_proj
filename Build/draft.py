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

# =========Setting Constants==============
# Set self.maze square area here: Smallest SECTOR_AREA: 5.
SECTOR_AREA = 20
MARGIN = 10
# Resolution of the self.maze (Minimum 3)
SECT_X_COUNT = 40
SECT_Y_COUNT = 40
# Calculations to set size.
sizeX = (MARGIN*2)+(((SECT_X_COUNT // 2) * 2 + 1)*SECTOR_AREA)
sizeY = (MARGIN*2)+(((SECT_Y_COUNT // 2) * 2 + 1)*SECTOR_AREA)
size = (sizeX, sizeY)
walls = []


class Player:
    x = SECTOR_AREA + (MARGIN * 1.01)
    y = SECTOR_AREA + (MARGIN * 1.01)
    speed = 3

    def moveRight(self):
        self.x = self.x + self.speed

    def moveLeft(self):
        self.x = self.x - self.speed

    def moveUp(self):
        self.y = self.y - self.speed

    def moveDown(self):
        self.y = self.y + self.speed


class Wall:
    def __init__(self):
        walls = []

    def add_wall(self):
        if self not in walls:
            walls.append(self)

    def print_walls(self):
        print(len(walls))


class Maze:
    def __init__(self):
        self.maze = new_maze(SECT_X_COUNT, SECT_Y_COUNT)

    def new_blank_maze(self):
        self.maze = new_blank_maze(SECT_X_COUNT, SECT_Y_COUNT)

    def new_maze(self):
        self.maze = new_maze(SECT_X_COUNT, SECT_Y_COUNT)

    def draw_maze(self, _display_screen):
        # Set colors.
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)

        # Fill the self.maze
        for x in range(((SECT_X_COUNT // 2) * 2 + 1)):
            for y in range(((SECT_Y_COUNT // 2) * 2 + 1)):
                if self.maze[y][x] == False:
                    pygame.draw.rect(_display_screen, WHITE,
                                     [MARGIN+1+(x*SECTOR_AREA),
                                      MARGIN+1+(y*SECTOR_AREA),
                                      SECTOR_AREA, SECTOR_AREA], 0)
                if self.maze[y][x] == True:
                    pygame.draw.rect(_display_screen, BLACK,
                                     [MARGIN+1+(x*SECTOR_AREA),
                                      MARGIN+1+(y*SECTOR_AREA),
                                         SECTOR_AREA, SECTOR_AREA],
                                     0)
                    Wall.add_wall((x, y))
        # Draw Centre
        maze_middle_x = (SECT_X_COUNT // 2)
        maze_middle_y = (SECT_Y_COUNT // 2)
        if self.maze[maze_middle_y][maze_middle_x] == False:
            pygame.draw.rect(_display_screen, RED, [
                MARGIN+1+(maze_middle_x*SECTOR_AREA), MARGIN+1+(maze_middle_y*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)
        else:
            pygame.draw.rect(_display_screen, RED, [
                MARGIN+1+((maze_middle_x)*SECTOR_AREA), MARGIN+1+((maze_middle_y+1)*SECTOR_AREA), SECTOR_AREA, SECTOR_AREA], 0)

    def print_maze(self):
        print(self.maze)

# Game loop


class App_Runner:

    player = 0

    def __init__(self):
        self._running = True
        self._display_screen = None
        self._images = None
        self.player = Player()
        self.clock = pygame.time.Clock()
        self.maze = Maze()
        self.walls = Wall()

    def on_init(self):
        pygame.init()
        self._display_screen = pygame.display.set_mode(size, pygame.HWSURFACE)

        pygame.display.set_caption('AI Maze')
        self._running = True
        self._images = pygame.image.load("Build\images\\robbert.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_screen.fill((0, 0, 0))
        self.maze.draw_maze(self._display_screen)
        self._images = pygame.transform.scale(
            self._images, (math.floor((SECTOR_AREA*0.9)), math.floor((SECTOR_AREA*0.9))))
        self._display_screen.blit(self._images, (self.player.x, self.player.y))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            pygame.event.pump()
            self.clock.tick(60)
            keys = pygame.key.get_pressed()

            if (keys[K_ESCAPE]):
                self._running = False

            if (keys[K_RIGHT]):
                self.player.moveRight()

            if (keys[K_LEFT]):
                self.player.moveLeft()

            if (keys[K_UP]):
                self.player.moveUp()

            if (keys[K_DOWN]):
                self.player.moveDown()

            if (keys[K_RCTRL]):
                self.maze.new_maze()
                self.maze.draw_maze(self._display_screen)
                pygame.display.flip()

            if (keys[K_LCTRL]):
                self.maze.new_blank_maze()
                self.maze.draw_maze(self._display_screen)
                pygame.display.flip()

            if (keys[K_p]):
                self.walls.print_walls()

            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    Game = App_Runner()
    Game.on_execute()
