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
from typing import Callable
from typing import Dict
from typing import Union

from multiagent.agent.evaluation_function.evaluation_function_ import evaluation_function_food_and_ghost
from multiagent.agent.evaluation_function.evaluation_function_ import evaluation_function_food_and_ghost__attempt_1
from multiagent.agent.evaluation_function.evaluation_function_game_state_score import (
    evaluation_function_game_state_score
)
from multiagent.game.directions import Action
from multiagent.game.gamestate import GameState

"""
TYPE_CALLABLE_EVALUATION_FUNCTION

Notes:
    The real TYPE_CALLABLE_EVALUATION_FUNCTION wanted is something like
        Callable[[GameState, Union[Action, None]] 
    Where the None is optional as in the callable can be 
        _callable(GameState)
    OR
        _callable(GameState, Action)
    OR
        _callable(GameState, None)

    The closest you can can get to mimic this type is 
        Union[
        Callable[[GameState], float],
        Callable[[GameState, Action], float]
    ]
    HOWEVER; it does not support
        _callable(GameState)

    The solution to this problem is to use mypy, but I don't want to implement that because this problem
    should be solved in cPython
        https://mypy.readthedocs.io/en/latest/protocols.html#callback-protocols
"""
#
TYPE_CALLABLE_EVALUATION_FUNCTION = Callable[[GameState, Action], float]
TYPE_CALLABLE_EVALUATION_FUNCTION_POSSIBLE = Union[TYPE_CALLABLE_EVALUATION_FUNCTION, str]

DICT_K_EVALUATION_FUNCTION_NAME_V_EVALUATION_FUNCTION: Dict[str, TYPE_CALLABLE_EVALUATION_FUNCTION] = {
    evaluation_function_food_and_ghost.__name__: evaluation_function_food_and_ghost,
    evaluation_function_food_and_ghost__attempt_1.__name__: evaluation_function_food_and_ghost__attempt_1,
    evaluation_function_game_state_score.__name__: evaluation_function_game_state_score,

}


def get_evaluation_function(evaluation_function_name: str) -> TYPE_CALLABLE_EVALUATION_FUNCTION:
    evaluation_function = DICT_K_EVALUATION_FUNCTION_NAME_V_EVALUATION_FUNCTION.get(
        evaluation_function_name
    )

    if evaluation_function is None:
        raise Exception("{} is not a valid evaluation function".format(evaluation_function_name))

    return evaluation_function
