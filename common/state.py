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
# YOUR INTERFACE TO THE PACMAN WORLD: A State #
###################################################
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Set
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from pacman.agent import Agent



class State(ABC):
    """
    A State specifies the full game state, including the food, list_capsule,
    player configurations and score changes.

    GameStates are used by the Game object to capture the actual state of the game and
    can be used by agents to reason about the game.

    Much of the information in a State is stored in a StateDataPacman object.  We
    strongly suggest that you access that data via the accessor methods below rather
    than referring to the StateDataPacman object directly.

    Note that in classic Pacman, Pacman is always player 0.
    """

    #############################################
    #             Helper methods:               #
    # You shouldn't need to call these directly #
    #############################################


    @abstractmethod  # MultiagentTreeState DOES NOT HAVE THIS WHICH IS WHY ITS NOT ABSTRACT
    def get_agent_by_index(self, index: int) -> Union[Agent, None]:
        pass

    @abstractmethod  # MultiagentTreeState DOES NOT HAVE THIS WHICH IS WHY ITS NOT ABSTRACT
    def get_index_by_agent(self, agent: Agent) -> Union[int, None]:
        pass

    @abstractmethod
    def getLegalActions(self, agent: Agent):
        pass

    @abstractmethod
    def generateSuccessor(self, agent: Agent, action):
        pass

    @abstractmethod  # MultiagentTreeState DOES NOT HAVE THIS WHICH IS WHY ITS NOT ABSTRACT
    def get_container_state_GHOST(self, agent: Agent):  # TODO: wtf is a state_container
        pass

    @abstractmethod
    def getNumAgents(self) -> int:
        pass

    @abstractmethod
    def getScore(self):
        pass

    @abstractmethod
    def isLose(self):
        pass

    @abstractmethod
    def isWin(self):
        pass

    # static variable keeps track of which states have had getLegalActions called
    set_state_explored: Set[State] = set()

    @classmethod
    def getAndResetExplored(cls):
        tmp = cls.set_state_explored.copy()
        cls.set_state_explored = set()
        return tmp

