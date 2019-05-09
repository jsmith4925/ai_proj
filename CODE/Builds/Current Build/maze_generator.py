import math
import os
import random
import sys
import time

import numpy
import pandas
import numpy.random as rand


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

class maze():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.data = new_maze(self.x, self.y)
        self.start_pos = [1, 1]
        self.end_pos = [0,0]

    def reroll(self):
        self.data = new_maze(self.x, self.y)
        end_set = False
        while (not end_set):
            temp_end_x = random.randint(0,2) + int(((numpy.shape(self.data))[0]-1)/2)
            temp_end_y = random.randint(0,2) + int(((numpy.shape(self.data))[1]-1)/2)

            if self.data[temp_end_x][temp_end_y] == 0:
                self.end_pos = [temp_end_x, temp_end_y]
                end_set = True

    def print_data(self):
        print(pandas.DataFrame(self.data))
        print("Start Point: {}".format(self.start_pos))
        print("End Point: {}".format(self.end_pos))