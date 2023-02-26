# str_path_layout.py
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
from typing import TYPE_CHECKING
from typing import Tuple
from typing import Union

from common.util import manhattanDistance
from pacman import constants
from pacman.game.action_direction import ActionDirection
from pacman.game.grid_pacman import GridPacman
from pacman.game.type_player_pacman import EnumPlayerPacman
from pacman.types_ import TYPE_VECTOR

if TYPE_CHECKING:
    pass

VISIBILITY_MATRIX_CACHE = {}


class LayoutPacman:
    """
    A LayoutPacman manages the static information about the game board.
    """

    def __init__(self, list_str_layout_line: List[str]):

        self.width: int = len(list_str_layout_line[0])
        self.height: int = len(list_str_layout_line)

        self.walls: GridPacman = GridPacman(self.width, self.height, False)
        self.food: GridPacman = GridPacman(self.width, self.height, False)
        self.list_capsule: List[TYPE_VECTOR] = []

        self.list_tuple__type_player__position: List[Tuple[EnumPlayerPacman, TYPE_VECTOR]] = []
        self.numGhosts: int = 0

        self._processLayoutText(list_str_layout_line)
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
                ActionDirection.NORTH,
                ActionDirection.SOUTH,
                ActionDirection.WEST,
                ActionDirection.EAST
            ]

            visibility = GridPacman(self.width, self.height, {
                ActionDirection.NORTH: set(),
                ActionDirection.SOUTH: set(),
                ActionDirection.EAST: set(),
                ActionDirection.WEST: set(),
                ActionDirection.STOP: set()
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
        return LayoutPacman(self.layoutText[:])

    def _processLayoutText(self, layoutText: List[List[str]]):
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
        height_layout_max = self.height - 1

        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[height_layout_max - y][x]
                self._process_char_from_layout(x, y, layoutChar)

        # IMPORTANT: SORT IS NECESSARY FOR ORDERING AGENT MOVING ORDER
        self.list_tuple__type_player__position.sort(key=lambda tuple_: tuple_[0] )

        # self.list_tuple__class_player__position = [(i == 0, pos) for i, pos in self.list_tuple__class_player__position]

    def _process_char_from_layout(self, x: int, y: int, char_from_layout: str):
        """
        Makes the actual objects in the str_path_layout

        Notes:
            Given _position and char, add that tuple to

        """

        if char_from_layout == '%':
            self.walls[x][y] = True
        elif char_from_layout == '.':
            self.food[x][y] = True
        elif char_from_layout == 'o':
            self.list_capsule.append((x, y))
        elif char_from_layout == 'P':
            self.list_tuple__type_player__position.append((EnumPlayerPacman.PACMAN, (x, y)))
        elif char_from_layout in ['G']:
            self.list_tuple__type_player__position.append((EnumPlayerPacman.GHOST, (x, y)))
            self.numGhosts += 1
        elif char_from_layout in ['1', '2', '3',
                                  '4']:  # TODO: THIS IS IF THE MAP SPECIFIES GHOSTS EXACTLY # TOOD: ACTUALLY, IDK
            self.list_tuple__type_player__position.append((int(char_from_layout), (x, y)))
            self.numGhosts += 1


def get_layout_pacman(layout_thing: Union[str, LayoutPacman], back=2) -> Union[LayoutPacman, None]:

    if isinstance(layout_thing, LayoutPacman):
        return layout_thing

    if layout_thing.endswith('.lay'):
        layout = get_layout_object_helper('layouts/' + layout_thing)
        if layout is None:
            layout = get_layout_object_helper(layout_thing)

    else:
        layout = get_layout_object_helper(constants.PATH_LAYOUTS + layout_thing + '.lay')

        if layout is None:
            layout = get_layout_object_helper(layout_thing + '.lay')

    if layout is None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = get_layout_pacman(layout_thing, back - 1)
        os.chdir(curdir)

    return layout


def get_layout_object_helper(path_layout: str) -> Union[LayoutPacman, None]:
    """
    Given string_given of path of str_path_layout file, return LayoutPacman object or None

    :param path_layout:
    :return:
    """

    if not os.path.exists(path_layout):
        return None

    with open(path_layout, 'r') as f:
        return LayoutPacman([line.strip() for line in f])
