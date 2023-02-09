"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/29/2022

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

from typing import Callable
from typing import Dict
from typing import Union

from pacman.agent.evaluation_function.evaluation_function_better import evaluation_function_better
from pacman.agent.evaluation_function.evaluation_function_food_and_ghost import evaluation_function_food_and_ghost
from pacman.agent.evaluation_function.evaluation_function_food_and_ghost import (
    evaluation_function_food_and_ghost__attempt_1
)
from pacman.agent.evaluation_function.evaluation_function_state_score import (
    evaluation_function_state_score
)
from pacman.game.directions import Action
from common.state import State

"""
TYPE_EVALUATION_FUNCTION

Notes:
    The real TYPE_EVALUATION_FUNCTION wanted is something like
        Callable[[State, Union[Action, None]] 
    Where the None is optional as in the callable can be 
        _callable(State)
    OR
        _callable(State, Action)
    OR
        _callable(State, None)

    The closest you can can get to mimic this type is 
        Union[
        Callable[[State], float],
        Callable[[State, Action], float]
    ]
    HOWEVER; it does not support
        _callable(State)

    The solution to this problem_multi_agent_tree is to use mypy, but I don't want to implement that because this problem_multi_agent_tree
    should be solved in cPython
        https://mypy.readthedocs.io/en/latest/protocols.html#callback-protocols
"""
TYPE_EVALUATION_FUNCTION = Callable[[State, Union[Action, None]], float]

# class EvaluationFunction(Protocol):
#
#     def __call__(self, state_pacman: State, action: Union[Action, None]) -> float:
#         ...
#

TYPE_EVALUATION_FUNCTION_POSSIBLE = Union[TYPE_EVALUATION_FUNCTION, str]

LIST_EVALUATION_FUNCTION = [
    evaluation_function_food_and_ghost,
    evaluation_function_food_and_ghost__attempt_1,
    evaluation_function_state_score,
    evaluation_function_better,
]

DICT_K_EVALUATION_FUNCTION_NAME_V_EVALUATION_FUNCTION: Dict[str, TYPE_EVALUATION_FUNCTION] = {
    evaluation_function_.__name__: evaluation_function_ for evaluation_function_ in LIST_EVALUATION_FUNCTION
}


def get_evaluation_function(
        name_evaluation_function: Union[str, TYPE_EVALUATION_FUNCTION, None]
) -> TYPE_EVALUATION_FUNCTION:
    evaluation_function = name_evaluation_function

    if isinstance(name_evaluation_function, str):
        evaluation_function = DICT_K_EVALUATION_FUNCTION_NAME_V_EVALUATION_FUNCTION.get(
            name_evaluation_function
        )

    if evaluation_function is None:
        raise Exception("{} is not a valid evaluation function".format(name_evaluation_function))

    return evaluation_function
