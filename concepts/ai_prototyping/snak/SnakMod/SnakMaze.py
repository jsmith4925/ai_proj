# Imports
from math import asin, degrees, pi, radians, sqrt
from random import randint, shuffle

import numpy as np
import pandas as pds
import pygame
from keras.layers import Dense
from keras.models import Sequential

from functions import *

# import coremltools ?? 2.7 only so :/


class Direction:
    left, right, up, down = range(4)


class NodeType:
    empty, player, goal, wall = range(4)


# Screen constants
BLOCK_RES = 10
GRID_X = 50
GRID_Y = 50
# MAP_WIDTH = (((GRID_X // 2) * 2 + 1)*BLOCK_RES)
# MAP_HEIGHT = (((GRID_Y // 2) * 2 + 1)*BLOCK_RES)
screen_size = (((GRID_X // 2) * 2 + 1), ((GRID_Y // 2) * 2 + 1))

screen_color = (217, 217, 217)
wall_color = (0, 0, 0)
player_color = (0, 170, 255)
goal_color = (255, 0, 0)

# Grid constants
columns, rows = screen_size[0], screen_size[1]


class SnakeNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def removeDuplicates(input_file_name, output_file_name):
    with open(input_file_name, "r") as input_file, open(output_file_name, "w") as output_file:
        output_file.writelines(unique_everseen(input_file))


def getGrid():
    grid = [[0 for x in range(columns)] for y in range(rows)]
    boolGrid = new_maze(columns, rows)

    for x in range(columns):
        for y in range(rows):
            if boolGrid[y][x] == 1:
                grid[x][y] = NodeType.wall


def getGetPlayerNode(x, y, grid):
    # learn how this is used, may be irrelivant
    player_node = []
    segment = PlayerNode(x, y)
    player_node.append(segment)

    grid[x][y] = NodeType.player

    return player_node

# getGrownSnake goes here ://


def drawNode(x, y, grid, screen):
    if grid[x][y] == NodeType.player:
        color = player_color
    elif grid[x][y] == NodeType.goal:
        color = goal_color
    elif grid[x][y] == NodeType.wall:
        color = wall_color
    else:
        color = screen_color

    pygame.draw.rect(screen, color, pygame.Rect(
        x*BLOCK_RES, y*BLOCK_RES, BLOCK_RES, BLOCK_RES))


def isGameOver(player_node, grid):
    # How strict are we being? dead on touch lol
    player = player_node[0]

    return grid[player.x][player.y] == NodeType.wall\
        or player.x == 0\
        or player.y == 0\
        or player.x == columns-1\
        or player.y == rows-1


def advancePlayer(player_node, direction, grid):
    # head = snake_nodes[0]
    # tail = snake_nodes.pop()
    # grid[tail.x][tail.y] = NodeType.empty

    # if direction == Direction.up:
    #     tail.x = head.x
    #     tail.y = head.y - 1
    # elif direction == Direction.down:
    #     tail.x = head.x
    #     tail.y = head.y + 1
    # elif direction == Direction.left:
    #     tail.x = head.x - 1
    #     tail.y = head.y
    # elif direction == Direction.right:
    #     tail.x = head.x + 1
    #     tail.y = head.y

    # snake_nodes.insert(0, tail)

    # if grid[tail.x][tail.y] != NodeType.food and grid[tail.x][tail.y] != NodeType.wall:
    #     grid[tail.x][tail.y] = NodeType.snake_head

    # for i in range(1, len(snake_nodes)):
    #     grid[snake_nodes[i].x][snake_nodes[i].y] = NodeType.wall

    return player_node


def drawNodes(grid, screen):
    for x in range(columns):
        for y in range(rows):
            drawNode(x, y, grid, screen)


def getNeighboringNodes(player_node, direction, grid):
    player = player_node[0]

    if direction == Direction.right:
        return (grid[player.x][player.y-1],
                grid[player.x+1][player.y],
                grid[player.x][player.y+1])
    elif direction == Direction.left:
        return (grid[player.x][player.y+1],
                grid[player.x-1][player.y],
                grid[player.x][player.y-1])
    elif direction == Direction.up:
        return (grid[player.x-1][player.y],
                grid[player.x][player.y-1],
                grid[player.x+1][player.y])
    else:
        return (grid[player.x+1][player.y],
                grid[player.x][player.y+1],
                grid[player.x-1][player.y])


def areNeighboringNodesBlocked(left, forward, right):
    return (int(left == NodeType.wall),
            int(forward == NodeType.wall),
            int(right == NodeType.wall))


def isAnyNeighboringNodesBlocked(left, forward, right):
    return left == NodeType.wall or forward == NodeType.wall or right == NodeType.wall


def distanceBetweenPlayerAndGoal(player_node, goal_position):
    plyaer = player_node[0]

    goal_x, goal_y = goal_position

    base = abs(goal_x - player.x)
    perpendicular = abs(goal_y - player.y)

    hypotenuse = sqrt(base**2 + perpendicular**2)
    return hypotenuse


def getOrthogonalAngle(player_node, goal_position, absolute_direction):
    player = player_node[0]

    goal_x, goal_y = goal_position

    base = goal_x - player.x
    perpendicular = goal_y - player.y

    hypotenuse = sqrt(base**2 + perpendicular**2)+0.00001

    angle = degrees(asin(perpendicular/hypotenuse)) % 90

    if absolute_direction == Direction.right:
        if base >= 0 and perpendicular <= 0:
            angle = angle + 0
        elif base <= 0 and perpendicular <= 0:
            angle = angle + 90
        elif base <= 0 and perpendicular >= 0:
            angle = angle + 90
        else:
            angle = angle + 0
    elif absolute_direction == Direction.up:
        if base >= 0 and perpendicular <= 0:
            angle = angle + 0
        elif base <= 0 and perpendicular <= 0:
            angle = angle + 0
        elif base <= 0 and perpendicular >= 0:
            angle = angle + 90
        else:
            angle = angle + 90
    elif absolute_direction == Direction.left:
        if base >= 0 and perpendicular <= 0:
            angle = angle + 90
        elif base <= 0 and perpendicular <= 0:
            angle = angle + 0
        elif base <= 0 and perpendicular >= 0:
            angle = angle + 0
        else:
            angle = angle + 90
    else:
        if base >= 0 and perpendicular <= 0:
            angle = angle + 90
        elif base <= 0 and perpendicular <= 0:
            angle = angle + 90
        elif base <= 0 and perpendicular >= 0:
            angle = angle + 0
        else:
            angle = angle + 0

    return radians(angle-90)/(pi/2)


'''
Neural Net functions
'''


def neuralInputs(player_node, grid, absolute_direction, goal_position):
    return (areNeighboringNodesBlocked(*getNeighboringNodes(player_node,
                                                            absolute_direction,
                                                            grid)),
            getOrthogonalAngle(player_node,
                               goal_position,
                               absolute_direction))


def getTrainedModel(data, labels):

    model = Sequential()
    model.add(Dense(5, input_shape=(5,), activation="relu"))
    model.add(Dense(25, activation="relu"))
    model.add(Dense(25, activation="relu"))
    model.add(Dense(1, activation="linear"))
    model.summary()
    model.compile(loss="mean_squared_error",
                  optimizer="adam", metrics=["accuracy"])
    model.fit(data, labels, epochs=1)

    return model


def getRelativeDirection(current_direction, next_direction):

    if current_direction == Direction.right:
        if next_direction == Direction.up:
            return -1
        elif next_direction == Direction.right:
            return 0
        else:
            return 1
    elif current_direction == Direction.left:
        if next_direction == Direction.down:
            return -1
        elif next_direction == Direction.left:
            return 0
        else:
            return 1
    elif current_direction == Direction.up:
        if next_direction == Direction.left:
            return -1
        elif next_direction == Direction.up:
            return 0
        else:
            return 1
    else:
        if next_direction == Direction.right:
            return -1
        elif next_direction == Direction.down:
            return 0
        else:
            return 1


def getPredictedDirection(player_node, absolute_direction, model, inputs, grid, shuffle_predictions):
    player = player_node[0]  # needed?

    relative_directions = [-1, 0, 1]

    if shuffle_predictions == True:
        shuffle(relative_directions)

    no_match_found = False
    for relative_direction in relative_directions:
        prediction = model.predict(np.array([[inputs[0][0],
                                              inputs[0][1],
                                              inputs[0][2],
                                              inputs[1],
                                              relative_direction]]))
        if prediction > 0.9:
            break
        no_match_found = True

    if no_match_found == True and shuffle_predictions == True:
        for relative_direction in relative_directions:
            prediction = model.predict(np.array([[inputs[0][0],
                                                  inputs[0][1],
                                                  inputs[0][2],
                                                  inputs[1],
                                                  relative_direction]]))
            if prediction >= 0:
                break

    if absolute_direction == Direction.right:
        if relative_direction == -1:
            return Direction.up, relative_direction
        elif relative_direction == 0:
            return Direction.right, relative_direction
        else:
            return Direction.down, relative_direction
    elif absolute_direction == Direction.left:
        if relative_direction == -1:
            return Direction.down, relative_direction
        elif relative_direction == 0:
            return Direction.left, relative_direction
        else:
            return Direction.up, relative_direction
    elif absolute_direction == Direction.up:
        if relative_direction == -1:
            return Direction.left, relative_direction
        elif relative_direction == 0:
            return Direction.up, relative_direction
        else:
            return Direction.right, relative_direction
    else:
        if relative_direction == -1:
            return Direction.right, relative_direction
        elif relative_direction == 0:
            return Direction.down, relative_direction
        else:
            return Direction.left, relative_direction


def getOutputForTraining(target_output, inputs, player_node, relative_direction):

    return "\n{},{},{},{},{},{}".format(target_output,
                                        inputs[0][0],
                                        inputs[0][1],
                                        inputs[0][2],
                                        inputs[1],
                                        relative_direction)


def generateGoal(grid):
    goal_position = (25, 25)
    grid[goal_position[0]][goal_position[1]] = NodeType.goal
    return goal_position


def checkForGoalCollision(player_node, grid):
    player = player_node[0]
    return grid[player.x][player.y] == NodeType.goal


def resetStuckPosition():
    return [[0 for x in range(columns)] for y in range(rows)]


def run_game(death_count, font, model):

    # Game Objects
    score_count = 0
    grid = getGrid()
    directions = [Direction.right, Direction.left,
                  Direction.up, Direction.down]
    direction = directions[2]  # start going right.. maybe change?
    player_position = (1, 1)
    goal_position = generateGoal(grid)
    player_node = getGetPlayerNode(player_position[0],
                                   player_position[1],
                                   grid)
    screen = pygame.display.set_mode((screen_size[0]*BLOCK_RES,
                                      screen_size[1]*BLOCK_RES))

    stuck_position = resetStuckPosition()

    # Game Loop
    while not isGameOver(player_node, grid):

        game_stats_label = font.render("Deaths: {} High Score: {}".format(
            death_count, score_count), 1, (0, 200, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # Drawing
        screen.fill(screen_color)
        drawNodes(grid, screen)
        screen.blit(game_stats_label, (0, 0))
        pygame.display.flip()

        # Clock ticking
        pygame.time.Clock().tick(999999999999)

        # If player gets stuck in the same position for too long (5 times), shuffle the predictions
        stuck_position[player_node[0].x][player_node[0].y] += 1
        shuffle_predictions = (
            stuck_position[player_node[0].x][player_node[0].y] > 5)

        # Manual controls
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and direction != Direction.down:
            direction = Direction.up
        elif pressed[pygame.K_DOWN] and direction != Direction.up:
            direction = Direction.down
        elif pressed[pygame.K_LEFT] and direction != Direction.right:
            direction = Direction.left
        elif pressed[pygame.K_RIGHT] and direction != Direction.left:
            direction = Direction.right

        # Random controls
        # pressed = randint(0, 3)
        # if pressed == 0 and direction!=Direction.down: direction = Direction.up
        # elif pressed == 1 and direction!=Direction.up: direction = Direction.down
        # elif pressed == 2 and direction!=Direction.right: direction = Direction.left
        # elif pressed == 3 and direction!=Direction.left: direction = Direction.right

        # AI controls
        current_direction = direction
        inputs = neuralInputs(player_node, grid, direction, goal_position)
        direction, relative_direction = getPredictedDirection(
            player_node, direction, model, inputs, grid, shuffle_predictions)

        previous_distance_between_player_and_goal = distanceBetweenPlayerAndGoal(
            player_node, goal_position)
        player_node = advancePlayer(player_node, direction, grid)
        current_distance_between_player_and_goal = distanceBetweenPlayerAndGoal(
            player_node, goal_position)

        # If game is over, target output is -1
        # If snake has moved away from the goal, target output is 0
        # If snake has moved closer to the goal, target output is 1
        if isGameOver(player_node, grid):
            target_output = -1
        elif current_distance_between_player_and_goal >= previous_distance_between_player_and_goal:
            target_output = 0
        else:
            target_output = 1

        output = getOutputForTraining(
            target_output, inputs, player_node, getRelativeDirection(current_direction, direction))
        file = open("Data.csv", "a")
        file.write(output)
        file.close()

        if checkForGoalCollision(player_node, grid):
            score_count += 1
            grid = getGrid()
            player_position = (1, 1)
            goal_position = generateGoal(grid)
            shuffle_predictions = False
            stuck_position = resetStuckPosition()


# Load CSV file, indicate that the first column represents labels
data = pds.read_csv("Data.csv", usecols=[1, 2, 3, 4, 5])
labels = pds.read_csv("Data.csv", usecols=[0])
model = getTrainedModel(data, labels)
# coreml_model = coremltools.converters.keras.convert(model)
# coreml_model.save("SnakeModel.mlmodel")
death_count = 0
pygame.init()
font = pygame.font.SysFont("monospace", 40)

while True:
    death_count += 1
    run_game(death_count, font, model)
