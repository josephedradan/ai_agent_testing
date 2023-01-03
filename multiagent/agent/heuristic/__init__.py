"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/30/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import Callable
from typing import Tuple
from typing import Union

from multiagent.search import SearchProblem

TYPE_HEURISTIC_FUNCTION = Callable[[Tuple[int, int], SearchProblem], float]


def get_heuristic_function(
        heuristic_search_function: Union[TYPE_HEURISTIC_FUNCTION, str]) -> TYPE_HEURISTIC_FUNCTION:
    if isinstance(heuristic_search_function, str):
        function = DICT_K_HEURISTIC_FUNCTION_NAME_V_HEURISTIC_FUNCTION.get(heuristic_search_function)

        if function is None:
            raise Exception("Heuristic search function {} does not exist".format(heuristic_search_function))

        return function

    return heuristic_search_function

# FIXME: THIS SHIT DOES NOT TAKE state, IT SHOULD BE GENERAL LIKE A TUPLE OR VECTOR OF DIMENSIONS (x, y, z , ...)
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


DICT_K_HEURISTIC_FUNCTION_NAME_V_HEURISTIC_FUNCTION = {
    manhattanHeuristic.__name__: manhattanHeuristic,
    euclideanHeuristic.__name__: euclideanHeuristic,
    nullHeuristic.__name__: nullHeuristic

}
