# textDisplay.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from pacman.graphics.graphics_pacman import GraphicsPacman

if TYPE_CHECKING:
    from common.state import State
    from common.state_data_pacman import StateDataPacman


class GraphicsPacmanNull(GraphicsPacman):


    def initialize(self, state: StateDataPacman, isBlue=False):
        pass

    def update(self, state: State):
        pass

    # def checkNullDisplay(self):
    #     return True

    def pause(self):
        time.sleep(self.time_sleep)

    def draw(self, state):
        print(state)

    def updateDistributions(self, dist):
        pass

    def finish(self):
        pass

    def drawExpandedCells(self, cells):
        pass