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

from pacman.agent.search_problem import SearchProblem

TYPE_HEURISTIC_FUNCTION = Callable[[Tuple[int, int], SearchProblem], float]

from pacman.agent.heuristic_function.heuristic_euclidean import euclideanHeuristic
from pacman.agent.heuristic_function.heuristic_null import nullHeuristic
from pacman.agent.heuristic_function.heuristic_food import foodHeuristic
from pacman.agent.heuristic_function.heuristic_manhattan import manhattanHeuristic

LIST_HEURISTIC_FUNCTION = [
    manhattanHeuristic,
    euclideanHeuristic,
    nullHeuristic,
    foodHeuristic,
]

DICT_K_HEURISTIC_FUNCTION_NAME_V_HEURISTIC_FUNCTION = {
    heuristic_function.__name__: heuristic_function for heuristic_function in LIST_HEURISTIC_FUNCTION
}


def get_heuristic_function(
        heuristic_search_function: Union[TYPE_HEURISTIC_FUNCTION, str]) -> TYPE_HEURISTIC_FUNCTION:
    if isinstance(heuristic_search_function, str):
        function = DICT_K_HEURISTIC_FUNCTION_NAME_V_HEURISTIC_FUNCTION.get(heuristic_search_function)

        if function is None:
            raise Exception("Heuristic search function {} does not exist".format(heuristic_search_function))

        return function

    return heuristic_search_function
