"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/7/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""

# FIXME: THIS SHIT DOES NOT TAKE state_pacman, IT SHOULD BE GENERAL LIKE A TUPLE OR VECTOR OF DIMENSIONS (x, y, z , ...)

from pacman.agent.search_problem import SearchProblem


def nullHeuristic(state, problem: SearchProblem):
    """
    A heuristic function estimates the cost from the current state_pacman to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
