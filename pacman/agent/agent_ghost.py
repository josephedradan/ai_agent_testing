# ghosts.py
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
from typing import Dict
from typing import TYPE_CHECKING

from common import util
from pacman.agent.agent import Agent
from pacman.game.directions import Action
from pacman.game.directions import Directions

if TYPE_CHECKING:
    from common.state import State


class AgentGhost(Agent, ABC):

    def __init__(self, **kwargs):
        super(AgentGhost, self).__init__(**kwargs)

    def getAction(self, state: State) -> Action:

        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    @abstractmethod
    def getDistribution(self, state: State) -> Dict[Action, float]:
        "Returns a Counter encoding a distribution over actions from the provided state_pacman."
        pass

    # def get_legal_actions(self, state: StatePacman):
    #
    #
    #     legalActions = state.getLegalActions(self)
    #
    #     reverse = Actions.reverseDirection(container_position_vector.direction)
    #
    #     # GHOST DONT STOP SO REMOVE IT
    #     if Directions.STOP in possibleActions:
    #         possibleActions.remove(Directions.STOP)
    #
    #     # DONT REVERSE IF GHOST HAS MORE THAN 1 MOVE
    #     if reverse in possibleActions and len(possibleActions) > 1:
    #         possibleActions.remove(reverse)
