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

from typing import Dict
from typing import TYPE_CHECKING

from common import util
from common.action import Action
from pacman.agent.agent_ghost import AgentGhost

if TYPE_CHECKING:
    from common.game_state import GameState


class AgentGhostRandom(AgentGhost) :
    "A ghost that chooses a legal action uniformly at random."

    def getDistribution(self, game_state: GameState) -> Dict[Action: float]:
        dist = util.Counter()

        for a in game_state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()

        return dist
