"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/29/2023

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

from typing import List
from typing import TYPE_CHECKING
from typing import Union

from common.game_state import GameState
from common.game_state_data import GameStateData
from pacman.game.layout import Layout
from pacman.game.rules.common import TIME_PENALTY
from pacman.game.rules.rules_ghost import GhostRules
from pacman.game.rules.rules_pacman import PacmanRules

if TYPE_CHECKING:
    from pacman.game.directions import Action

class GameStatePacman(GameState):

    def __init__(self, game_state_previous: Union[GameStatePacman, None] = None):
        """
        Generates a new game_state by copying information from its predecessor.
        """
        self.game_state_data: GameStateData

        if game_state_previous is not None:  # Initial game_state
            self.game_state_data = GameStateData(game_state_previous.game_state_data)
        else:
            self.game_state_data = GameStateData()

    def get_deep_copy(self) -> GameState:
        state = type(self)(self)
        state.game_state_data = self.game_state_data.get_deep_copy()
        return state

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        # return hasattr(other, 'game_state_data') and self.game_state_data == other.game_state_data

        if isinstance(other, GameStatePacman):
            return self.game_state_data == other.game_state_data
        return False

    def __hash__(self):
        """
        Allows states to be keys of dictionaries.
        """
        return hash(self.game_state_data)

    def __str__(self):

        return str(self.game_state_data)

    def initialize(self, layout: Layout, numGhostAgents: int = 1000):
        """
        Creates an initial game game_state from a layout array (see layout.py).
        """
        self.game_state_data.initialize(layout, numGhostAgents)

    ####################################################
    # Accessor methods: use these to access GameState data #
    ####################################################


    def getLegalActions(self, agentIndex=0):
        """
        Returns the legal actions for the agent specified.
        """
        #        GameState.set_game_state_explored.add(self)
        if self.isWin() or self.isLose():
            return []

        if agentIndex == 0:  # AgentPacman is moving
            return PacmanRules.getLegalActions(self)
        else:
            return GhostRules.getLegalActions(self, agentIndex)

    def generateSuccessor(self, index_agent: int, action: Action):
        """
        Returns the successor game_state after the specified agent takes the action.
        """
        # Check that successors exist
        if self.isWin() or self.isLose():
            raise Exception('Can\'t generate a successor of a terminal game_state.')

        # Copy current game_state
        game_state_pacman = GameStatePacman(self)

        # Let agent's logic deal with its action's effects on the board
        if index_agent == 0:  # AgentPacman is moving
            game_state_pacman.game_state_data._eaten = [False for i in range(game_state_pacman.getNumAgents())]
            PacmanRules.applyAction(game_state_pacman, action)
        else:  # A ghost is moving
            GhostRules.applyAction(game_state_pacman, action, index_agent)

        # Time passes
        if index_agent == 0:
            game_state_pacman.game_state_data.scoreChange += -TIME_PENALTY  # Penalty for waiting around
        else:
            GhostRules.decrementTimer(game_state_pacman.game_state_data.list_state_agent[index_agent])

        # Resolve multi-agent effects
        GhostRules.checkDeath(game_state_pacman, index_agent)

        # Book keeping
        game_state_pacman.game_state_data._agentMoved = index_agent
        game_state_pacman.game_state_data.score += game_state_pacman.game_state_data.scoreChange

        type(self).set_game_state_explored.add(self)
        type(self).set_game_state_explored.add(game_state_pacman)
        return game_state_pacman

    def getLegalPacmanActions(self) -> List[Action]:
        return self.getLegalActions(0)

    def generatePacmanSuccessor(self, action: Action):
        """
        Generates the successor game_state after the specified agent_pacman_ move
        """
        return self.generateSuccessor(0, action)

    def getPacmanState(self):
        """
        Returns an StateAgent object for agent_pacman_ (in game.py)

        game_state.position gives the current position
        game_state.direction gives the travel vector
        """
        return self.game_state_data.list_state_agent[0].copy()

    def getPacmanPosition(self):
        return self.game_state_data.list_state_agent[0].get_position()

    def getGhostStates(self):
        return self.game_state_data.list_state_agent[1:]

    def getGhostState(self, index_agent: int):
        if index_agent == 0 or index_agent >= self.getNumAgents():
            raise Exception("Invalid index passed to getGhostState")
        return self.game_state_data.list_state_agent[index_agent]

    def getGhostPosition(self, index_agent: int):
        if index_agent == 0:
            raise Exception("Pacman's index passed to getGhostPosition")
        return self.game_state_data.list_state_agent[index_agent].get_position()

    def getGhostPositions(self):
        return [s.get_position() for s in self.getGhostStates()]

    def getNumAgents(self):
        return len(self.game_state_data.list_state_agent)

    def getScore(self):
        return float(self.game_state_data.score)

    def getCapsules(self):
        """
        Returns a list of positions (x,y) of the remaining list_capsule.
        """
        return self.game_state_data.list_capsule

    def getNumFood(self):
        return self.game_state_data.grid_food.count()

    def getFood(self):
        """
        Returns a GridPacman of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = game_state.getFood()
        if currentFood[x][y] == True: ...
        """
        return self.game_state_data.grid_food

    def getWalls(self):
        """
        Returns a GridPacman of boolean wall indicator variables.

        Grids can be accessed via list notation, so to check
        if there is a wall at (x,y), just call

        walls = game_state.getWalls()
        if walls[x][y] == True: ...
        """
        return self.game_state_data.layout.walls

    def hasFood(self, x: int, y: int):
        return self.game_state_data.grid_food[x][y]

    def hasWall(self, x: int, y: int):
        return self.game_state_data.layout.walls[x][y]

    def isLose(self):
        return self.game_state_data._lose

    def isWin(self):
        return self.game_state_data._win
