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

from abc import ABC
from abc import abstractmethod
from typing import Set
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class GameState(ABC):
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

    @abstractmethod
    def getLegalActions(self, agentIndex=0):
        pass

    @abstractmethod
    def generateSuccessor(self, agentIndex, action):
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
    set_game_state_explored: Set[GameState] = set()

    @classmethod
    def getAndResetExplored(cls):
        tmp = cls.set_game_state_explored.copy()
        cls.set_game_state_explored = set()
        return tmp

