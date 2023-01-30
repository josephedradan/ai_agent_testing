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

from common import util
from pacman.agent.agent_ghost import AgentGhost
from pacman.game.actions import Actions
from common.util import manhattanDistance

if TYPE_CHECKING:
    from common.game_state import GameState


class AgentGhostDirectional(AgentGhost):
    """
    A ghost that prefers to rush Pacman, or flee when scared.

    """

    def __init__(self, index: int, prob_attack: float = 0.8, prob_scaredFlee: float = 0.8):
        super().__init__(index)

        self.prob_attack: float = prob_attack
        self.prob_scaredFlee: float = prob_scaredFlee

    def getDistribution(self, game_state: GameState) -> Dict[Action: float]:

        # Read variables from game_state
        ghostState = game_state.getGhostState(self.index)
        legalActions = game_state.getLegalActions(self.index)
        pos = game_state.getGhostPosition(self.index)
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared:
            speed = 0.5

        actionVectors = [Actions.directionToVector(
            a, speed) for a in legalActions]
        newPositions = [(pos[0] + a[0], pos[1] + a[1]) for a in actionVectors]
        pacmanPosition = game_state.getPacmanPosition()

        # Select best actions given the game_state
        distancesToPacman = [manhattanDistance(
            pos, pacmanPosition) for pos in newPositions]
        if isScared:
            bestScore = max(distancesToPacman)
            bestProb = self.prob_scaredFlee
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
