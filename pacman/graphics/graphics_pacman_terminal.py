"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/8/2023

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

import time

from typing import TYPE_CHECKING

from pacman.graphics.graphics_pacman import GraphicsPacman
from common.util import nearestPoint

if TYPE_CHECKING:
    from pacman.game.game_state import GameState
    from pacman.game.game_state_data import GameStateData

DRAW_EVERY = 1
SLEEP_TIME = 0  # This can be overwritten by __init__
DISPLAY_MOVES = False
QUIET = False  # Supresses output


class GraphicsPacmanTerminal(GraphicsPacman):


    # def __init__(self, speed=None):
    #     if speed != None:
    #         global SLEEP_TIME
    #         SLEEP_TIME = speed

    def initialize(self, state: GameStateData, isBlue: bool = False):
        self.draw(state)
        self.pause()
        self.turn = 0
        self.agentCounter = 0

    def update(self, state: GameState):
        numAgents = len(state.agentStates)

        self.agentCounter = (self.agentCounter + 1) % numAgents
        if self.agentCounter == 0:
            self.turn += 1
            if DISPLAY_MOVES:
                ghosts = [nearestPoint(state.getGhostPosition(i)) for i in range(1, numAgents)]
                print("%4d) P: %-8s" % (self.turn, str(nearestPoint(state.getPacmanPosition()))),
                      '| Score: %-5d' % state.score, '| Ghosts:', ghosts)
            if self.turn % DRAW_EVERY == 0:
                self.draw(state)
                self.pause()
        if state._win or state._lose:
            self.draw(state)

    def pause(self):
        time.sleep(self.time_sleep)

    def draw(self, state):
        print(state)

    def finish(self):
        pass
