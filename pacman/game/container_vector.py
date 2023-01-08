"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/27/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from __future__ import annotations

from typing import Tuple
from typing import Union

from pacman.game.actions import Actions
from pacman.game.directions import Directions


class ContainerVector:
    """
    A ContainerVector holds the (x,y) coordinate of a character, along with its
    traveling direction.

    The convention for positions, like a graph, is that (0,0) is the lower left corner, x increases
    horizontally and y increases vertically.  Therefore, north is the direction of increasing y, or (0,1).
    """

    def __init__(self, pos: Tuple[int, ...], direction: Directions):
        self.position: Tuple[int, ...] = pos
        self.direction: Directions = direction

    def get_position(self) -> Tuple[int, ...]:
        return self.position

    def get_direction(self) -> Directions:
        return self.direction

    # def isInteger(self) -> bool:
    #     x, y = self.position
    #     return x == int(x) and y == int(y)

    def __eq__(self, container_vector_possible: Union[ContainerVector, None]):
        if container_vector_possible is None:
            return False

        return self.position == container_vector_possible.position and self.direction == container_vector_possible.direction

    def __hash__(self):
        # x = hash(self.position)
        # y = hash(self.direction)
        return hash((self.position, self.direction))

    def __str__(self):
        return "(x, y)=" + str(self.position) + ", " + str(self.direction)

    def get_configuration_successor(self, vector: Tuple[int, ...]) -> ContainerVector:  # FIXME: NOT GENERALIZED
        """
        Generates a new container_vector reached by translating the current
        container_vector by the action vector.  This is a low-level call and does
        not attempt to respect the legality of the movement.

        Actions are movement vectors.
        """
        x, y = self.position
        dx, dy = vector
        direction = Actions.vectorToDirection(vector)

        if direction == Directions.STOP:
            direction = self.direction  # There is no stop direction

        return ContainerVector((x + dx, y + dy), direction)
