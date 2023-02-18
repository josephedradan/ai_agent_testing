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
from enum import auto

from common.type_player import TypePlayer


class TypePlayerPacman(TypePlayer):
    """
    Order of Enum constants determines player action order

    It is important that PACMAN is the first Enum constant so auto grading can work properly
    """
    PACMAN = auto()
    GHOST = auto()
