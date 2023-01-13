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
from typing import Callable
from typing import List
from typing import Union

from pacman.agent.heuristic_function import TYPE_HEURISTIC_FUNCTION
from pacman.agent.search_problem import SearchProblem
from pacman.game.directions import Action

TYPE_SEARCH_FUNCTION = Callable[[SearchProblem, Union[TYPE_HEURISTIC_FUNCTION, None]],
                                List[Action]]

from pacman.agent.search.search import aStarSearch
from pacman.agent.search.search import breadthFirstSearch
from pacman.agent.search.search import depthFirstSearch
from pacman.agent.search.search import uniformCostSearch

LIST_SEARCH_FUNCTION = [
    breadthFirstSearch,
    depthFirstSearch,
    aStarSearch,
    uniformCostSearch,
]

DICT_K_NAME_SEARCH_FUNCTION_V_SEARCH_FUNCTION = {
    search_function_.__name__: search_function_ for search_function_ in LIST_SEARCH_FUNCTION
}


def get_search_function(
        name_search_function: Union[str, TYPE_SEARCH_FUNCTION, None]) -> TYPE_SEARCH_FUNCTION:
    search_function = name_search_function

    if isinstance(name_search_function, str):
        search_function = DICT_K_NAME_SEARCH_FUNCTION_V_SEARCH_FUNCTION.get(
            name_search_function
        )

    if search_function is None:
        raise Exception("{} is not a valid search function".format(name_search_function))

    return search_function
