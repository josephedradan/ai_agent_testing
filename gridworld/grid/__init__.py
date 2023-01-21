"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/19/2023

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
from typing import Union

from gridworld.grid.grid_book import getBookGrid
from gridworld.grid.grid_bridge import getBridgeGrid
from gridworld.grid.grid_cliff import getCliffGrid
from gridworld.grid.grid_cliff_2 import getCliffGrid2
from gridworld.grid.grid_discount import getDiscountGrid
from gridworld.grid.grid_maze import getMazeGrid
from gridworld.main_grid_world import Gridworld

LIST_GET_GRID_WORLD_CALLABLE = [
    getBookGrid,
    getBridgeGrid,
    getCliffGrid,
    getCliffGrid2,
    getDiscountGrid,
    getMazeGrid
]

DICT_K_NAME_GET_GRID_WORLD_CALLABLE_V_GET_GRID_WORLD_CALLABLE = {
    get_grid_world_callable.__name__: get_grid_world_callable for get_grid_world_callable in
    LIST_GET_GRID_WORLD_CALLABLE
}


def get_callable_get_grid_world(name_get_grid_world_callable: Union[str, Callable, None]) -> Callable[[], Gridworld]:
    get_grid_world_function_ = name_get_grid_world_callable

    if isinstance(name_get_grid_world_callable, str):
        get_grid_world_function_ = DICT_K_NAME_GET_GRID_WORLD_CALLABLE_V_GET_GRID_WORLD_CALLABLE.get(
            name_get_grid_world_callable)

    if get_grid_world_function_ is None:
        raise Exception("{} is not a get gridworld callable callable".format(name_get_grid_world_callable))

    return get_grid_world_function_
