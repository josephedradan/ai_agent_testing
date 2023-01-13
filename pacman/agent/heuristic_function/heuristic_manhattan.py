"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/12/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import TYPE_CHECKING
from typing import Tuple
from pacman.agent.search_problem import SearchProblem

# FIXME: GENERALIZE position TO BE MULTI DIMENSIONAL
def manhattanHeuristic(position: Tuple[int, int], problem: SearchProblem):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
