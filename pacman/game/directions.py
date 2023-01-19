"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/11/2022

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


class Directions():
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {NORTH: WEST,
            SOUTH: EAST,
            EAST:  NORTH,
            WEST:  SOUTH,
            STOP:  STOP}

    RIGHT = dict([(y, x) for x, y in list(LEFT.items())])

    REVERSE = {NORTH: SOUTH,
               SOUTH: NORTH,
               EAST: WEST,
               WEST: EAST,
               STOP: STOP}


Action = Directions


class Temp(Enum):
    NORTH = "North"

    def __str__(self):
        return self.value

print(Directions.NORTH)
print(Temp.NORTH)
print(Directions.NORTH == Temp.NORTH)

