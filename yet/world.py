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
from collections import Set

from yet.game_state import GameState


class World:

    def __init__(self):
        self.set_game_state: Set[GameState] = set()

    def get_and_reset_world(self):
        set_game_state_old = self.set_game_state.copy()
        self.set_game_state = set()
        return set_game_state_old