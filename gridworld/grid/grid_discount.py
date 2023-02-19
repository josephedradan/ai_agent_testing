"""
Date created: 1/19/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Contributors: 
    https://github.com/josephedradan

Reference:

"""
from gridworld.main_grid_world import Gridworld


def getDiscountGrid():
    grid = [[' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', ' ', ' '],
            [' ', '#', 1, '#', 10],
            ['S', ' ', ' ', ' ', ' '],
            [-10, -10, -10, -10, -10]]
    return Gridworld(grid)
