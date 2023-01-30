"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/12/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import TYPE_CHECKING

from pacman.agent.search_problem.search_problem_position import PositionSearchProblem
from common.game_state import GameState

if TYPE_CHECKING:
    from pacman.game.grid_pacman import GridPacman


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem_multi_agent_tree for finding a path to any food.

    This search problem_multi_agent_tree is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem_multi_agent_tree to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState: GameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        super().__init__(gameState)
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem_multi_agent_tree definition.
        """
        x, y = state

        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        self.food: GridPacman
        self.walls: GridPacman

        # Note that self.food is the same a foodGrid from problem_multi_agent_tree 7 and foodGrid CHANGES OVER (foodHeuristic)
        list_position_food_remaining = self.food.asList()

        ####################
        """
        Recall that list_position_food_remaining changes so just check if the state, which is a tuple of the position,
        is in the list_position_food_remaining.

        """

        return state in list_position_food_remaining
