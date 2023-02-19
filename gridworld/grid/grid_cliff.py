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


def getCliffGrid():
    grid = [[' ', ' ', ' ', ' ', ' '],
            ['S', ' ', ' ', ' ', 10],
            [-100, -100, -100, -100, -100]]
    return Gridworld(grid)
