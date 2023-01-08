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

# FIXME: THIS SHIT DOES NOT TAKE state, IT SHOULD BE GENERAL LIKE A TUPLE OR VECTOR OF DIMENSIONS (x, y, z , ...)
from typing import Tuple

from pacman.agent.problem import SearchProblem


def nullHeuristic(state, problem: SearchProblem):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


# FIXME: GENERALIZE position TO BE MULTI DIMENSIONAL
def manhattanHeuristic(position: Tuple[int, int], problem: SearchProblem):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


# FIXME: GENERALIZE position TO BE MULTI DIMENSIONAL
def euclideanHeuristic(position: Tuple[int, int], problem: SearchProblem):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5
