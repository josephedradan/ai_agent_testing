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

from pacman.agent.search_problem import SearchProblem
from pacman.game.actions import Actions
from pacman.game.directions import Directions
from pacman.graphics.graphics_pacman_display_tkiner import GraphicsPacmanDisplayTkinter


class PositionSearchProblem(SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the agent_pacman_ board.

    The state space consists of (x,y) positions in a agent_pacman_ game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn=lambda x: 1, goal=(1, 1), start=None, warn=True, visualize=True) -> object:
        """
        Stores the start and goal.

        gameState: A GameState object (agent_pacman_.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        super().__init__()
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For graphics_pacman purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):  # TODO: COLORER
        isGoal = state == self.goal

        # For graphics_pacman purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)  # TODO: THIS SHOULD BE THE FINAL STATE ADDED BASICALLY
            # import __main__
            # if '_display' in dir(__main__):
            #     if 'drawExpandedCells' in dir(__main__._display):  # @UndefinedVariable
            #         __main__._display.drawExpandedCells(self._visitedlist)  # @UndefinedVariable

            # TODO: JOSEPH CUSTOM HERE

            if isinstance(self.graphics, GraphicsPacmanDisplayTkinter):
                self.graphics.drawExpandedCells(self._visitedlist)

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for graphics_pacman purposes
        self._expanded += 1  # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x, y))
        return cost
