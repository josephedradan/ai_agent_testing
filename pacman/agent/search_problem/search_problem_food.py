"""
Date created: 1/12/2023

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

from typing import TYPE_CHECKING

from pacman.game.handler_action_direction import HandlerActionDirection
from pacman.game.action_direction import ActionDirection


if TYPE_CHECKING:
    pass
    from common.state_pacman import StatePacman


class FoodSearchProblem:
    """
    A search problem_multi_agent_tree associated with finding a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem_multi_agent_tree is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's _position
      foodGrid:       a GridPacman (see game.py) of either True or False, specifying remaining food
    """

    def __init__(self, state_pacman: StatePacman):
        self.start = (state_pacman.getPacmanPosition(), state_pacman.getFood())
        self.walls = state_pacman.getWalls()

        self.startingGameState = state_pacman
        self._expanded = 0  # DO NOT CHANGE
        self.heuristicInfo = {}  # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1  # DO NOT CHANGE
        for direction in [ActionDirection.NORTH, ActionDirection.SOUTH, ActionDirection.EAST, ActionDirection.WEST]:
            x, y = state[0]
            dx, dy = HandlerActionDirection.get_vector_from_action_direction(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:

                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append((((nextx, nexty), nextFood), direction, 1))
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x, y = self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = HandlerActionDirection.get_vector_from_action_direction(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost
