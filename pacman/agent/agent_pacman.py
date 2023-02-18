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
from __future__ import annotations

import random
from abc import ABC
from typing import TYPE_CHECKING

from pacman.agent import Agent
from pacman.agent.evaluation_function import TYPE_EVALUATION_FUNCTION
from pacman.agent.evaluation_function import TYPE_EVALUATION_FUNCTION_POSSIBLE
from pacman.agent.evaluation_function import get_evaluation_function
from pacman.agent.evaluation_function.evaluation_function_state_score import (
    evaluation_function_state_score
)
from pacman.game.actiondirection import Action

if TYPE_CHECKING:
    from common.state import State


class AgentPacman(Agent):

    def __init__(self,
                 evaluation_function: TYPE_EVALUATION_FUNCTION_POSSIBLE = (
                         evaluation_function_state_score
                 ),
                 depth='2',
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.depth = int(depth)

        # Resolve evaluation_function if the evaluation_function is a string
        if isinstance(evaluation_function, str):
            evaluation_function = get_evaluation_function(evaluation_function)

        assert evaluation_function is not None

        self.evaluation_function: TYPE_EVALUATION_FUNCTION = evaluation_function

    def getAction(self, state: State) -> Action:
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous name_project, getAction takes a State and returns
        some ActionDirection.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = state.getLegalActions(self)

        # Choose one of the best actions
        scores = [self.evaluation_function(self, state, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]

        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        """
        Notes:
            1.  Calls evaluationFunction for each move and puts the result of the call into a list of max scores
            2.  Select the max score of the list of max scores
            3.  Make a list of indices that represents the action (e.g. index for "North" action is 3) that 
                has the max score
            4.  randomly select a index in list of indices
            5.  Use legalMoves and input the randomly selected index to get an action (e.g "North") and return it
        """

        # print("legalMoves[chosenIndex]", type(legalMoves[chosenIndex]), legalMoves[chosenIndex])

        return legalMoves[chosenIndex]
