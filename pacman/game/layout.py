# layout.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import os
import random
from functools import reduce
from typing import List
from typing import Tuple
from typing import Union

from pacman import constants
from pacman.game.directions import Directions
from pacman.game.grid import Grid
from pacman.util import manhattanDistance

VISIBILITY_MATRIX_CACHE = {}


class Layout:
    """
    A Layout manages the static information about the game board.
    """

    def __init__(self, list_str_layout_line: List[str]):
        self.width: int = len(list_str_layout_line[0])
        self.height: int = len(list_str_layout_line)
        self.walls: Grid = Grid(self.width, self.height, False)
        self.food: Grid = Grid(self.width, self.height, False)
        self.list_capsule = []
        self.agentPositions = []
        self.numGhosts = 0
        self.processLayoutText(list_str_layout_line)
        self.layoutText = list_str_layout_line
        self.totalFood = len(self.food.asList())
        # self.initializeVisibilityMatrix()

        self.visibility = None

    def getNumGhosts(self):
        return self.numGhosts

    def initializeVisibilityMatrix(self):
        global VISIBILITY_MATRIX_CACHE
        if reduce(str.__add__, self.layoutText) not in VISIBILITY_MATRIX_CACHE:
            vecs = [(-0.5, 0), (0.5, 0), (0, -0.5), (0, 0.5)]

            directions = [
                Directions.NORTH,
                Directions.SOUTH,
                Directions.WEST,
                Directions.EAST
            ]

            visibility = Grid(self.width, self.height, {
                Directions.NORTH: set(),
                Directions.SOUTH: set(),
                Directions.EAST: set(),
                Directions.WEST: set(),
                Directions.STOP: set()
            })

            for x in range(self.width):
                for y in range(self.height):
                    if self.walls[x][y] == False:
                        for vec, direction in zip(vecs, directions):
                            dx, dy = vec
                            next_x, next_y = x + dx, y + dy

                            while ((next_x + next_y) != int(next_x) + int(next_y) or
                                   not self.walls[int(next_x)][int(next_y)]
                            ):
                                visibility[x][y][direction].add((next_x, next_y))

                                next_x, next_y = x + dx, y + dy

            self.visibility = visibility

            VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)] = visibility
        else:
            self.visibility = VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)]

    def is_wall(self, pos: Tuple[int, int]) -> bool:
        x, col = pos
        return self.walls[x][col]

    def get_position_legal_random(self) -> Tuple[int, int]:
        x = random.choice(list(range(self.width)))
        y = random.choice(list(range(self.height)))
        while self.is_wall((x, y)):
            x = random.choice(list(range(self.width)))
            y = random.choice(list(range(self.height)))
        return (x, y)

    def get_position_corner_random(self) -> Tuple[int, int]:
        poses = [(1, 1),
                 (1, self.height - 2),
                 (self.width - 2, 1),
                 (self.width - 2, self.height - 2)
                 ]
        return random.choice(poses)

    def get_position_corner_furthest(self, pacPos):
        poses = [(1, 1),
                 (1, self.height - 2),
                 (self.width - 2, 1),
                 (self.width - 2, self.height - 2)
                 ]
        dist, pos = max([(manhattanDistance(p, pacPos), p) for p in poses])

        return pos

    def isVisibleFrom(self, ghostPos, pacPos, pacDirection):
        row, col = [int(x) for x in pacPos]
        return ghostPos in self.visibility[row][col][pacDirection]

    def __str__(self):
        return "\n".join(self.layoutText)

    def deepCopy(self):
        return Layout(self.layoutText[:])

    def processLayoutText(self, layoutText):
        """
        Coordinates are flipped from the input format to the (x,y) convention here

        The shape of the maze.  Each character
        represents a different type of object.
         % - Wall
         . - Food
         o - Capsule
         G - Ghost
         P - Pacman
        Other characters are ignored.
        """
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[maxY - y][x]
                self.processLayoutChar(x, y, layoutChar)
        self.agentPositions.sort()
        self.agentPositions = [(i == 0, pos) for i, pos in self.agentPositions]

    def processLayoutChar(self, x, y, layoutChar):
        if layoutChar == '%':
            self.walls[x][y] = True
        elif layoutChar == '.':
            self.food[x][y] = True
        elif layoutChar == 'o':
            self.list_capsule.append((x, y))
        elif layoutChar == 'P':
            self.agentPositions.append((0, (x, y)))
        elif layoutChar in ['G']:
            self.agentPositions.append((1, (x, y)))
            self.numGhosts += 1
        elif layoutChar in ['1', '2', '3', '4']:
            self.agentPositions.append((int(layoutChar), (x, y)))
            self.numGhosts += 1


def get_layout(name: str, back=2) -> Union[Layout, None]:
    if name.endswith('.lay'):
        layout = get_layout_object_helper('layouts/' + name)
        if layout is None:
            layout = get_layout_object_helper(name)

    else:
        layout = get_layout_object_helper(constants.PATH_LAYOUTS + name + '.lay')

        if layout is None:
            layout = get_layout_object_helper(name + '.lay')

    if layout is None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = get_layout(name, back - 1)
        os.chdir(curdir)

    return layout


def get_layout_object_helper(path_layout: str) -> Union[Layout, None]:
    """
    Given string_given of path_file_test of layout file, return Layout object or None

    :param path_layout:
    :return:
    """

    if not os.path.exists(path_layout):
        return None

    with open(path_layout, 'r') as f:
        return Layout([line.strip() for line in f])
