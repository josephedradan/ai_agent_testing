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

from abc import ABC, abstractmethod

from multiagent.game import gamestate
# index_agent:Union[int, None] = None
from multiagent.game.gamestate import GameState


class RulesAgent(ABC):

    @abstractmethod
    @staticmethod
    def getLegalActions(state: GameState):
        pass

    @abstractmethod
    @staticmethod
    def applyAction(state: GameState, action):
        pass
