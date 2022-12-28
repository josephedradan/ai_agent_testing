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

from yet.game_state import GameState


class Agent(ABC):

    def __init__(self, index=0):
        self.index = index

    @abstractmethod
    def get_action(self, state: GameState):
        pass
