"""
Date created: 1/7/2023

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

# FIXME: THIS DOES NOT TAKE state, IT SHOULD BE GENERAL LIKE A TUPLE OR VECTOR OF DIMENSIONS (x, y, z , ...)

from pacman.agent.search_problem import SearchProblem


def nullHeuristic(state, problem: SearchProblem):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
