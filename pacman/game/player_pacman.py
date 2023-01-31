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
from pacman.game.player import Player


class PlayerGhost(Player):

    def __init__(self, agent: Agent):
        super().__init__(agent)
