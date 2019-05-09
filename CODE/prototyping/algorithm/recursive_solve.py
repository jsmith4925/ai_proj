import numpy
import pandas
from maze_generator import *

WIDTH = 8
HEIGHT = 8

maze = maze(WIDTH, HEIGHT)
maze.reroll()
maze.print_data()

start_X, start_Y = maze.start_pos[0], maze.start_pos[1]
end_X, end_Y = maze.end_pos[0], maze.end_pos[1]
wasHere = numpy.zeros(numpy.shape(maze.data), dtype=bool)
correctPath = numpy.zeros(numpy.shape(maze.data), dtype=bool)

def solveMaze(maze_array):
    for row in range(numpy.shape(maze_array)[0]):
        for col in range(numpy.shape(maze_array)[1]):
            wasHere[row][col] = False
            correctPath[row][col] = False

    recursiveSolve(start_X, start_Y)
    return correctPath

def recursiveSolve(x, y):
    if (x == end_X and y == end_Y):
        return True

    if (maze.data[x][y] == 1 or wasHere[x][y]):
        return False

    wasHere[x][y] = True

    if (x != 1):
        if (recursiveSolve(x-1, y)):
            correctPath[x][y] = True
            return True

    if (x != (numpy.shape(maze.data)[0])-2):
        if (recursiveSolve(x+1, y)):
            correctPath[x][y] = True
            return True

    if (y != 1):
        if (recursiveSolve(x, y-1)):
            correctPath[x][y] = True
            return True
    
    if (y != numpy.shape(maze.data)[1]-2):
        if (recursiveSolve(x, y+1)):
            correctPath[x][y] = True
            return True
    
    return False

solution = solveMaze(maze.data)
print(pandas.DataFrame(solution))