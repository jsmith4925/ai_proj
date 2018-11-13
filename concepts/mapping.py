import math
import time

import pygame
from pygame.locals import *

# Set colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
LRED = (255, 128, 128)

pygame.init()
running = True

# Smallest space: 5.
sectorArea = 15
# Resolution of the grid
sectorYCount = 40
sectorXCount = 40

sizeX = 50+sectorYCount*sectorArea
sizeZ = 50+sectorXCount*sectorArea

# Set size.
size = (sizeX, sizeZ)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
screen.fill(WHITE)
pygame.draw.rect(screen, BLACK, [25, 25, sizeX-49, sizeZ-49], 2)

pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
