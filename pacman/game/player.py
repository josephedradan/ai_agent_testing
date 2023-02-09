"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/30/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""

from pacman.agent import Agent
from pacman.game.type_player import TypePlayer


class Player:
    __counter = 1

    def __init__(self, agent: Agent, type_player: TypePlayer):
        self.agent = agent
        self.type_player = type_player

        # DIRTY COLORING TRICK

        self.index = Player.__counter
        Player.__counter += 1

    def get_agent(self) -> Agent:
        return self.agent

    def __hash__(self):
        """
        Use the agent's hash because it is unique and this object is just a wrapper over it
        """
        return self.agent.__hash__()

    def __eq__(self, other):
        return self.agent.__eq__(other)

    def set_type_player(self, type_player: TypePlayer):
        self.type_player = type_player

    def get_type_player(self) -> TypePlayer:
        return self.type_player
