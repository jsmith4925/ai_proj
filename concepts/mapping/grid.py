
"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
 
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
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40
 
# This sets the margin between each cell
MARGIN = 2
RES = 8
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(RES):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(RES):
        grid[row].append(0)  # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
for row in range(RES):
    # Add an empty array that will hold each cell
    # in this row
    grid[0][row] = 2
    grid[row][RES-1] =2
    for column in range(RES):
        grid[column][0] = 2
        grid[RES-1][column] =2
 
grid[0][RES/2] = 1
grid[RES-1][RES/2] = 1
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [(WIDTH+MARGIN)*RES, (HEIGHT+MARGIN)*RES]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one
            if grid[row][column] == 0:
                grid[row][column] = 1
            elif grid[row][column] == 1:
                grid[row][column] = 2
            elif grid[row][column] == 2:
                grid[row][column] = 1
            #print("Click ", pos, "Grid coordinates: ", row, column)
 #when stuck - last square made wall becomes road
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    for row in range(RES):
        for column in range(RES):
            color = GRASS_GREEN
            if grid[row][column] == 1:
                color = ROAD_BROWN
            elif grid[row][column] == 2:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()