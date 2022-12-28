"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/27/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from multiagent import util
from multiagent.agent.agent_ghost import GhostAgent
from multiagent.game.gamestate import GameState


class RandomGhost(GhostAgent):
    "A ghost that chooses a legal action uniformly at random."

    def getDistribution(self, state: GameState):
        dist = util.Counter()
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist
