"""
Date created: 12/29/2022

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

from typing import Callable
from typing import Dict
from typing import Protocol
from typing import Union

from common.state import State
from pacman.agent import Agent
from pacman.game.action_direction import Action

from pacman.agent.evaluation_function.evaluation_function_better import evaluation_function_better
from pacman.agent.evaluation_function.evaluation_function_food_and_ghost import evaluation_function_food_and_ghost
from pacman.agent.evaluation_function.evaluation_function_food_and_ghost import (
    evaluation_function_food_and_ghost__attempt_1
)
from pacman.agent.evaluation_function.evaluation_function_state_score import (
    evaluation_function_state_score
)

"""
TYPE_EVALUATION_FUNCTION

Reference:
    Protocol
        Notes:
            Callable and Protocol Callable type hinting
            
            PyCharm does not support it yet i guess...
            
        Reference:
            https://mypy.readthedocs.io/en/latest/protocols.html#callback-protocols
"""
# class EvaluationFunction(Protocol):
#
#     def __call__(self, *args, **kwargs):
#         ...
#
# TYPE_EVALUATION_FUNCTION = EvaluationFunction

TYPE_EVALUATION_FUNCTION = Callable[[Agent, State, Union[Action, None]], float]


TYPE_EVALUATION_FUNCTION_POSSIBLE = Union[TYPE_EVALUATION_FUNCTION, str]

x: TYPE_EVALUATION_FUNCTION = evaluation_function_better

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
