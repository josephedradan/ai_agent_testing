# ghostAgents.py
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
from abc import abstractmethod

from multiagent import util
from multiagent.agent.agent import Agent
from multiagent.game.directions import Directions
from multiagent.game import gamestate
from multiagent.game.gamestate import GameState


class GhostAgent(Agent):

    def __init__(self, index):
        super().__init__(index)

    def getAction(self, state: GameState):

        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    @abstractmethod
    def getDistribution(self, state: GameState):
        "Returns a Counter encoding a distribution over actions from the provided state."
        pass
