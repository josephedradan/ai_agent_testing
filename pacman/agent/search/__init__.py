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

from typing import Union

from pacman.agent.search.search import a_star_search
from pacman.agent.search.search import breadth_first_search
from pacman.agent.search.search import depth_first_search
from pacman.agent.search.search import uniform_cost_search
from pacman.game.common import TYPE_SEARCH_FUNCTION

LIST_SEARCH_FUNCTION = [
    breadth_first_search,
    depth_first_search,
    a_star_search,
    uniform_cost_search,
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
