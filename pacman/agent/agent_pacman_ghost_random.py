"""
Date created: 12/27/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Contributors: 
    https://github.com/josephedradan

Reference:

"""
from __future__ import annotations

from typing import Dict
from typing import TYPE_CHECKING

from common import util
from common.action import Action
from pacman.agent.agent_pacman_ghost import AgentPacmanGhost

if TYPE_CHECKING:
    from common.state import State


class AgentPacmanGhostRandom(AgentPacmanGhost) :
    "A ghost that chooses a legal action uniformly at random."

    def getDistribution(self, state: State) -> Dict[Action: float]:
        dist = util.Counter()

        for a in state.getLegalActions(self):
            dist[a] = 1.0
        dist.normalize()

        return dist
