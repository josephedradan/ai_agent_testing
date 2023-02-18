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
from __future__ import annotations


# FIXME: GENERALIZE _position TO BE MULTI DIMENSIONAL
from typing import TYPE_CHECKING
from typing import Tuple

from pacman.agent.search_problem import SearchProblem

def euclideanHeuristic(position: Tuple[int, int], problem: SearchProblem):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5
