"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/28/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""

from multiagent.agent import AgentPacman
from multiagent.agent.evaluation_function import TYPE_EVALUATION_FUNCTION_POSSIBLE
from multiagent.agent.evaluation_function import evaluation_function_food_and_ghost
from multiagent.agent.evaluation_function import evaluation_function_food_and_ghost__attempt_1


class AgentPacmanReflex(AgentPacman):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a game_state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def __init__(self,
                 index: int = 0,
                 evaluation_function: TYPE_EVALUATION_FUNCTION_POSSIBLE = (
                         evaluation_function_food_and_ghost)

                 ):
        super().__init__(index, evaluation_function)


class AgentPacmanReflex_Attempt_1(AgentPacmanReflex):  # NOQA
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a game_state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def __init__(self,
                 index: int = 0,
                 evaluation_function: TYPE_EVALUATION_FUNCTION_POSSIBLE = (
                         evaluation_function_food_and_ghost__attempt_1)

                 ):
        super().__init__(index, evaluation_function)