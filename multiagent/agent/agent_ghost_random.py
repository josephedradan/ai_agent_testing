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
from __future__ import annotations

from typing import TYPE_CHECKING

from multiagent import util
from multiagent.agent.agent_ghost import AgentGhost

if TYPE_CHECKING:
    from multiagent.game.gamestate import GameState


class AgentGhostRandom(AgentGhost):
    "A ghost that chooses a legal action uniformly at random."

    def getDistribution(self, game_state: GameState):
        dist = util.Counter()
        for a in game_state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist
