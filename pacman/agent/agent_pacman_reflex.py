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

from pacman.agent import AgentPacman
from pacman.agent.evaluation_function import TYPE_EVALUATION_FUNCTION_POSSIBLE
from pacman.agent.evaluation_function import evaluation_function_food_and_ghost
from pacman.agent.evaluation_function import evaluation_function_food_and_ghost__attempt_1


class AgentPacmanReflex(AgentPacman):
    """
    A reflex player chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def __init__(self,
                 evaluation_function: TYPE_EVALUATION_FUNCTION_POSSIBLE = (
                         evaluation_function_food_and_ghost
                 ),
                 **kwargs
                 ):
        super().__init__(evaluation_function)


class AgentPacmanReflex_Attempt_1(AgentPacmanReflex):  # NOQA
    """
    A reflex player chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def __init__(self,
                 index: int = 0,
                 evaluation_function: TYPE_EVALUATION_FUNCTION_POSSIBLE = (
                         evaluation_function_food_and_ghost__attempt_1
                 )
                 ):
        super().__init__(index, evaluation_function)