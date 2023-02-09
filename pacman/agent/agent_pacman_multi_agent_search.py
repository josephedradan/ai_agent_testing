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
from abc import ABC
from typing import Callable
from typing import Union

from pacman.agent import AgentPacman
from pacman.agent.evaluation_function.evaluation_function_state_score import evaluation_function_state_score


class AgentPacmanMultiAgentSearch(AgentPacman, ABC):
    """
    This class provides some common elements to all of your
    multi-player searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    # evaluation_function='scoreEvaluationFunction'
    def __init__(self,
                 evaluation_function: Union[Callable, None] = evaluation_function_state_score,
                 depth='2',
                 **kwargs
                 ):

        super().__init__(evaluation_function,**kwargs)
        self.depth = int(depth)
