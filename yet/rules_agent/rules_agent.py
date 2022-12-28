"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/23/2022

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

from yet.agent.agent import Agent
from yet.constants import Direction
from yet.game_state import GameState


class RulesAgent(ABC):

    @abstractmethod
    def get_actions_legal(self, game_state: GameState):
        pass

    @abstractmethod
    def do_action(self, game_state: GameState, action: Direction, agent: Agent):
        pass
