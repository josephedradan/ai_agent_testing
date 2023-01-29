# list_agent_ghost.py
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

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from common import util
from pacman.agent.agent import Agent
from pacman.game.directions import Action
from pacman.game.directions import Directions

if TYPE_CHECKING:
    from common.game_state import GameState


class AgentGhost(Agent, ABC):

    def __init__(self, index: int):
        super().__init__(index)

    def getAction(self, game_state: GameState) -> Action:

        dist = self.getDistribution(game_state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    @abstractmethod
    def getDistribution(self, game_state: GameState):
        "Returns a Counter encoding a distribution over actions from the provided game_state."
        pass

