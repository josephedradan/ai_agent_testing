"""
Date created: 12/31/2022

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
from __future__ import annotations

from typing import Type
from typing import Union

from pacman.agent.search_problem.search_problem import SearchProblem
from pacman.agent.search_problem.search_problem_corners import CornersProblem
from pacman.agent.search_problem.search_problem_food import FoodSearchProblem
from pacman.agent.search_problem.search_problem_position import PositionSearchProblem
from pacman.agent.search_problem.search_problem_position_any_food import AnyFoodSearchProblem

DICT_K_NAME_SUBCLASS_PROBLEM_V_SUBCLASS_PROBLEM = {
    PositionSearchProblem.__name__: PositionSearchProblem,
    FoodSearchProblem.__name__: FoodSearchProblem,
    CornersProblem.__name__: CornersProblem,
    SearchProblem.__name__: SearchProblem,
    AnyFoodSearchProblem.__name__: AnyFoodSearchProblem,
}


def get_subclass_search_problem(search_problem: Union[str, Type[SearchProblem], None]) -> Type[SearchProblem]:
    if isinstance(search_problem, str):

        problem = DICT_K_NAME_SUBCLASS_PROBLEM_V_SUBCLASS_PROBLEM.get(search_problem)

        if problem is None:
            raise Exception("Problem does not exist")

        return problem

    return search_problem
