"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/6/2023

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
from enum import auto


class TypePlayerPacman(Enum):
    PACMAN = auto()  # It is important that PACMAN is first Enum as it determines player movement order
    GHOST = auto()


    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        return False