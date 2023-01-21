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

from typing import List
from typing import TYPE_CHECKING
from typing import Tuple

from pacman.game.directions import Directions

if TYPE_CHECKING:
    from pacman.game.container_vector import ContainerVector
    from pacman.game.grid_pacman import GridPacman


class Actions:
    """
    A collection of static methods for manipulating move actions.
    """
    # Directions
    dict_k_direction_v_position = {Directions.WEST: (-1, 0),
                                   Directions.STOP: (0, 0),
                                   Directions.EAST: (1, 0),
                                   Directions.NORTH: (0, 1),
                                   Directions.SOUTH: (0, -1)}

    _directionsAsList = [('West', (-1, 0)), ('Stop', (0, 0)), ('East', (1, 0)), ('North', (0, 1)), ('South', (0, -1))]

    TOLERANCE = .001

    @staticmethod
    def reverseDirection(action: Directions):
        if action == Directions.NORTH:
            return Directions.SOUTH
        if action == Directions.SOUTH:
            return Directions.NORTH
        if action == Directions.EAST:
            return Directions.WEST
        if action == Directions.WEST:
            return Directions.EAST
        return action

    @staticmethod
    def vectorToDirection(vector: Tuple[int, ...]):

        dx, dy = vector

        if dy > 0:
            return Directions.NORTH
        if dy < 0:
            return Directions.SOUTH
        if dx < 0:
            return Directions.WEST
        if dx > 0:
            return Directions.EAST
        return Directions.STOP

    @staticmethod
    def directionToVector(direction: Directions, speed: float = 1.0):
        dx, dy = Actions.dict_k_direction_v_position[direction]
        return (dx * speed, dy * speed)

    @staticmethod
    def getPossibleActions(container_vector: ContainerVector, walls: GridPacman):
        possible = []
        x, y = container_vector.position
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int) > Actions.TOLERANCE):
            return [container_vector.get_direction()]

        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y]:
                possible.append(dir)

        return possible

    @staticmethod
    def getLegalNeighbors(position: Tuple[int, int], walls: GridPacman) -> List[Tuple[int, int]]:

        x, y = position
        x_int, y_int = int(x + 0.5), int(y + 0.5)
        neighbors = []
        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_x = x_int + dx
            if next_x < 0 or next_x == walls.width:
                continue
            next_y = y_int + dy
            if next_y < 0 or next_y == walls.height:
                continue
            if not walls[next_x][next_y]:
                neighbors.append((next_x, next_y))
        return neighbors

    @staticmethod
    def getSuccessor(position: Tuple[int, int], action: Directions):
        dx, dy = Actions.directionToVector(action)
        x, y = position
        return (x + dx, y + dy)
