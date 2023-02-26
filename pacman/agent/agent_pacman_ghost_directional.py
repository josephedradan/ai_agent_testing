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

from common.action import Action
from common import util
from common.util import manhattanDistance
from pacman.agent.agent_pacman_ghost import AgentPacmanGhost
from pacman.game.handler_action_direction import HandlerActionDirection

if TYPE_CHECKING:
    from common.state import State
    from common.state_pacman import StatePacman


class AgentPacmanGhostDirectional(AgentPacmanGhost):
    """
    A ghost that prefers to rush Pacman, or flee when scared.

    """

    def __init__(self, prob_attack: float = 0.8, prob_flee_scared: float = 0.8, **kwargs):
        super().__init__(**kwargs)

        self.prob_attack: float = prob_attack
        self.prob_flee_scared: float = prob_flee_scared

    def getDistribution(self, state: StatePacman) -> Dict[Action, float]:

        # Read variables from state
        ghostState = state.get_container_state_GHOST(self)
        legalActions = state.getLegalActions(self)
        pos = state.get_position_of_agent(self)
        isScared = ghostState.time_scared > 0

        speed = 1
        if isScared:
            speed = 0.5

        actionVectors = [HandlerActionDirection.get_vector_from_action_direction(
            a, speed) for a in legalActions]
        newPositions = [(pos[0] + a[0], pos[1] + a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance(
            pos, pacmanPosition) for pos in newPositions]
        if isScared:
            bestScore = max(distancesToPacman)
            bestProb = self.prob_flee_scared
        else:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip(
            legalActions, distancesToPacman) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += (1 - bestProb) / len(legalActions)
        dist.normalize()
        return dist
