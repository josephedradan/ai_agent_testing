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

from typing import List
from typing import TYPE_CHECKING
from typing import Union

from pacman.agent.state_agent import StateAgent
from pacman.game.actions import Actions
from pacman.game.directions import Action
from pacman.game.directions import Directions
from pacman.game.rules.common import COLLISION_TOLERANCE
from pacman.game.rules.rules_agent import RulesAgent
from common.util import manhattanDistance
from common.util import nearestPoint

if TYPE_CHECKING:
    from common.game_state import GameState


class GhostRules(RulesAgent):
    """
    These functions dictate how list_agent_ghost interact with their environment.
    """
    GHOST_SPEED = 1.0

    @staticmethod
    def getLegalActions(state: GameState, index_agent: Union[int, None] = None) -> List[Directions]:
        """
        Ghosts cannot stop, and cannot turn around unless they
        reach a dead end, but can turn 90 degrees at intersections.
        """
        container_position_vector = state.getGhostState(index_agent).container_position_vector
        possibleActions = Actions.getPossibleActions(
            container_position_vector, state.game_state_data.layout.walls
        )
        reverse = Actions.reverseDirection(container_position_vector.direction)
        if Directions.STOP in possibleActions:
            possibleActions.remove(Directions.STOP)
        if reverse in possibleActions and len(possibleActions) > 1:
            possibleActions.remove(reverse)

        return possibleActions

    @staticmethod
    def applyAction(state: GameState, action: Action, index_agent: Union[int] = None):

        legal = GhostRules.getLegalActions(state, index_agent)
        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))

        ghostState = state.game_state_data.list_state_agent[index_agent]
        speed = GhostRules.GHOST_SPEED
        if ghostState.scaredTimer > 0:
            speed /= 2.0
        vector = Actions.directionToVector(action, speed)
        ghostState.container_position_vector = ghostState.container_position_vector.get_container_position_vector_successor(
            vector)

    @staticmethod
    def decrementTimer(ghostState):
        timer = ghostState.scaredTimer
        if timer == 1:
            ghostState.container_position_vector.position = nearestPoint(
                ghostState.container_position_vector.position)
        ghostState.scaredTimer = max(0, timer - 1)

    @staticmethod
    def checkDeath(state, agentIndex):
        pacmanPosition = state.getPacmanPosition()
        if agentIndex == 0:  # Pacman just moved; Anyone can kill him
            for index in range(1, len(state.game_state_data.list_state_agent)):
                ghostState = state.game_state_data.list_state_agent[index]
                ghostPosition = ghostState.container_position_vector.get_position()
                if GhostRules.canKill(pacmanPosition, ghostPosition):
                    GhostRules.collide(state, ghostState, index)
        else:
            ghostState = state.game_state_data.list_state_agent[agentIndex]
            ghostPosition = ghostState.container_position_vector.get_position()
            if GhostRules.canKill(pacmanPosition, ghostPosition):
                GhostRules.collide(state, ghostState, agentIndex)

    @staticmethod
    def collide(state: GameState, ghostState: StateAgent, agentIndex):
        if ghostState.scaredTimer > 0:
            state.game_state_data.scoreChange += 200
            GhostRules.placeGhost(state, ghostState)
            ghostState.scaredTimer = 0
            # Added for first-person
            state.game_state_data._eaten[agentIndex] = True
        else:
            if not state.game_state_data._win:
                state.game_state_data.scoreChange -= 500
                state.game_state_data._lose = True

    @staticmethod
    def canKill(pacmanPosition, ghostPosition):
        return manhattanDistance(ghostPosition, pacmanPosition) <= COLLISION_TOLERANCE

    @staticmethod
    def placeGhost(state, ghostState):
        ghostState.container_position_vector = ghostState.container_position_vector_start
