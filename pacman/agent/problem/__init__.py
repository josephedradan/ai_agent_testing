"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/31/2022

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

from typing import Type
from typing import Union

from pacman.agent.problem.agent_pacman__search_problem import AnyFoodSearchProblem
from pacman.agent.problem.agent_pacman__search_problem import CornersProblem
from pacman.agent.problem.agent_pacman__search_problem import FoodSearchProblem
from pacman.agent.problem.agent_pacman__search_problem import PositionSearchProblem
from pacman.agent.problem.agent_pacman__search_problem import SearchProblem

DICT_K_PROBLEM_NAME_V_PROBLEM = {
    PositionSearchProblem.__name__: PositionSearchProblem,
    FoodSearchProblem.__name__: FoodSearchProblem,
    CornersProblem.__name__: CornersProblem,
    SearchProblem.__name__: SearchProblem,
    AnyFoodSearchProblem.__name__: AnyFoodSearchProblem,
}


def get_class_search_problem(search_problem: Union[str, Type[SearchProblem]]) -> Type[SearchProblem]:
    if isinstance(search_problem, str):

        problem = DICT_K_PROBLEM_NAME_V_PROBLEM.get(search_problem)

        if problem is None:
            raise Exception("Problem does not exist")

        return problem

    return search_problem
