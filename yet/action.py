"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/23/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from enum import Enum

from yet.constants import Direction


class Actions:  # TODO: REWRITE
    """
    A collection of static methods for manipulating move actions.
    """
    # Directions
    _directions = {Direction.WEST: (-1, 0),
                   Direction.STOP: (0, 0),
                   Direction.EAST: (1, 0),
                   Direction.NORTH: (0, 1),
                   Direction.SOUTH: (0, -1)}

    _directionsAsList = [('West', (-1, 0)), ('Stop', (0, 0)), ('East', (1, 0)), ('North', (0, 1)), ('South', (0, -1))]

    TOLERANCE = .001

    def reverseDirection(action):
        if action == Direction.NORTH:
            return Direction.SOUTH
        if action == Direction.SOUTH:
            return Direction.NORTH
        if action == Direction.EAST:
            return Direction.WEST
        if action == Direction.WEST:
            return Direction.EAST
        return action

    reverseDirection = staticmethod(reverseDirection)

    def vectorToDirection(vector):
        dx, dy = vector
        if dy > 0:
            return Direction.NORTH
        if dy < 0:
            return Direction.SOUTH
        if dx < 0:
            return Direction.WEST
        if dx > 0:
            return Direction.EAST
        return Direction.STOP

    vectorToDirection = staticmethod(vectorToDirection)

    def directionToVector(direction, speed=1.0):
        dx, dy = Actions._directions[direction]
        return (dx * speed, dy * speed)

    directionToVector = staticmethod(directionToVector)

    def getPossibleActions(config, walls):
        possible = []
        x, y = config.pos
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int) > Actions.TOLERANCE):
            return [config.getDirection()]

        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y]:
                possible.append(dir)

        return possible

    getPossibleActions = staticmethod(getPossibleActions)

    def getLegalNeighbors(position, walls):
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

    getLegalNeighbors = staticmethod(getLegalNeighbors)

    def getSuccessor(position, action):
        dx, dy = Actions.directionToVector(action)
        x, y = position
        return (x + dx, y + dy)

    getSuccessor = staticmethod(getSuccessor)