"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/27/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
###################################################
# YOUR INTERFACE TO THE PACMAN WORLD: A GameState #
###################################################
from __future__ import annotations

from typing import List
from typing import TYPE_CHECKING
from typing import Union

from pacman.game.game_state_data import GameStateData
from pacman.game.rules.common import TIME_PENALTY
from pacman.game.rules.rules_ghost import GhostRules
from pacman.game.rules.rules_pacman import PacmanRules

if TYPE_CHECKING:
    from pacman.game.directions import Action


class GameState:
    """
    A GameState specifies the full game game_state, including the food, list_capsule,
    agent configurations and score changes.

    GameStates are used by the Game object to capture the actual game_state of the game and
    can be used by agents to reason about the game.

    Much of the information in a GameState is stored in a GameStateData object.  We
    strongly suggest that you access that data via the accessor methods below rather
    than referring to the GameStateData object directly.

    Note that in classic Pacman, Pacman is always agent 0.
    """


    #############################################
    #             Helper methods:               #
    # You shouldn't need to call these directly #
    #############################################

    def __init__(self, game_state_previous: Union[GameState, None]=None):
        """
        Generates a new game_state by copying information from its predecessor.
        """
        if game_state_previous is not None:  # Initial game_state
            self.data: GameStateData = GameStateData(game_state_previous.data)
        else:
            self.data: GameStateData = GameStateData()

    def get_deep_copy(self) -> GameState:
        state = GameState(self)
        state.data = self.data.get_deep_copy()
        return state

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        return hasattr(other, 'data') and self.data == other.data

    def __hash__(self):
        """
        Allows states to be keys of dictionaries.
        """
        return hash(self.data)

    def __str__(self):

        return str(self.data)

    def initialize(self, layout, numGhostAgents=1000):
        """
        Creates an initial game game_state from a layout array (see layout.py).
        """
        self.data.initialize(layout, numGhostAgents)


    ####################################################
    # Accessor methods: use these to access game_state data #
    ####################################################

    # static variable keeps track of which states have had getLegalActions called
    explored = set()

    def getAndResetExplored():
        tmp = GameState.explored.copy()
        GameState.explored = set()
        return tmp

    getAndResetExplored = staticmethod(getAndResetExplored)

    def getLegalActions(self, agentIndex=0):
        """
        Returns the legal actions for the agent specified.
        """
        #        GameState.explored.add(self)
        if self.isWin() or self.isLose():
            return []

        if agentIndex == 0:  # AgentPacman is moving
            return PacmanRules.getLegalActions(self)
        else:
            return GhostRules.getLegalActions(self, agentIndex)

    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor game_state after the specified agent takes the action.
        """
        # Check that successors exist
        if self.isWin() or self.isLose():
            raise Exception('Can\'t generate a successor of a terminal game_state.')

        # Copy current game_state
        state = GameState(self)

        # Let agent's logic deal with its action's effects on the board
        if agentIndex == 0:  # AgentPacman is moving
            state.data._eaten = [False for i in range(state.getNumAgents())]
            PacmanRules.applyAction(state, action)
        else:  # A ghost is moving
            GhostRules.applyAction(state, action, agentIndex)

        # Time passes
        if agentIndex == 0:
            state.data.scoreChange += -TIME_PENALTY  # Penalty for waiting around
        else:
            GhostRules.decrementTimer(state.data.list_state_agent[agentIndex])

        # Resolve multi-agent effects
        GhostRules.checkDeath(state, agentIndex)

        # Book keeping
        state.data._agentMoved = agentIndex
        state.data.score += state.data.scoreChange
        GameState.explored.add(self)
        GameState.explored.add(state)
        return state

    def getLegalPacmanActions(self) -> List[Action]:
        return self.getLegalActions(0)

    def generatePacmanSuccessor(self, action):
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
        return self.data.list_state_agent[0].copy()

    def getPacmanPosition(self):
        return self.data.list_state_agent[0].get_position()

    def getGhostStates(self):
        return self.data.list_state_agent[1:]

    def getGhostState(self, agentIndex):
        if agentIndex == 0 or agentIndex >= self.getNumAgents():
            raise Exception("Invalid index passed to getGhostState")
        return self.data.list_state_agent[agentIndex]

    def getGhostPosition(self, agentIndex):
        if agentIndex == 0:
            raise Exception("Pacman's index passed to getGhostPosition")
        return self.data.list_state_agent[agentIndex].get_position()

    def getGhostPositions(self):
        return [s.get_position() for s in self.getGhostStates()]

    def getNumAgents(self):
        return len(self.data.list_state_agent)

    def getScore(self):
        return float(self.data.score)

    def getCapsules(self):
        """
        Returns a list of positions (x,y) of the remaining list_capsule.
        """
        return self.data.list_capsule

    def getNumFood(self):
        return self.data.food.count()

    def getFood(self):
        """
        Returns a Grid of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = game_state.getFood()
        if currentFood[x][y] == True: ...
        """
        return self.data.food

    def getWalls(self):
        """
        Returns a Grid of boolean wall indicator variables.

        Grids can be accessed via list notation, so to check
        if there is a wall at (x,y), just call

        walls = game_state.getWalls()
        if walls[x][y] == True: ...
        """
        return self.data.layout.walls

    def hasFood(self, x, y):
        return self.data.food[x][y]

    def hasWall(self, x, y):
        return self.data.layout.walls[x][y]

    def isLose(self):
        return self.data._lose

    def isWin(self):
        return self.data._win
