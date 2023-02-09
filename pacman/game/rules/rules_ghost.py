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

from pprint import pprint
from typing import List
from typing import TYPE_CHECKING

from common.util import manhattanDistance
from common.util import nearestPoint
from pacman.agent.container_state import ContainerState
from pacman.game.actions import Actions
from pacman.game.common import TYPE_POSITION
from pacman.game.directions import Action
from pacman.game.directions import Directions
from pacman.game.player import Player
from pacman.game.type_player import TypePlayer
from pacman.game.rules.common import COLLISION_TOLERANCE
from pacman.game.rules.rules_agent import RulesAgent

if TYPE_CHECKING:
    from common.state_pacman import StatePacman


class GhostRules(RulesAgent):
    """
    These functions dictate how ghosts interact with their environment.
    """
    GHOST_SPEED = 1.0

    @staticmethod
    def getLegalActions(state_pacman: StatePacman, player: Player) -> List[Directions]:
        """
        Ghosts cannot stop, and cannot turn around unless they
        reach a dead end, but can turn 90 degrees at intersections.

        JOSEPH NOTES:
            1. GHOST DONT STOP SO IT IS REMOVED
            2. DONT REVERSE IF GHOST HAS MORE THAN 1 MOVE

        """

        # TODO: JOSEPH COMMENT JOSEPH JUMP
        # print('----------------------', player)
        # pprint(state_pacman.state_data.dict_k_player_v_container_state)

        #
        # for a, b in state_pacman.state_data.dict_k_player_v_container_state.items():
        #     print(hash(a), hash(b))

        # print("---- player", player)
        # print("state_pacman.state_data.dict_k_player_v_container_state",
        #       state_pacman.state_data.dict_k_player_v_container_state)
        # print("state_pacman.get_state_container_GHOST(player)",
        #       state_pacman.get_state_container_GHOST(player))

        container_position_vector = state_pacman.get_state_container_GHOST(player).container_position_vector

        possibleActions = Actions.getPossibleActions(
            container_position_vector,
            state_pacman.state_data.layout.walls
        )

        reverse = Actions.reverseDirection(container_position_vector.direction)

        # GHOST DONT STOP SO REMOVE IT
        if Directions.STOP in possibleActions:
            possibleActions.remove(Directions.STOP)

        # DONT REVERSE IF GHOST HAS MORE THAN 1 MOVE
        if reverse in possibleActions and len(possibleActions) > 1:
            possibleActions.remove(reverse)

        return possibleActions

    @staticmethod
    def applyAction(state_pacman: StatePacman, action: Action, player: Player):

        legal = GhostRules.getLegalActions(state_pacman, player)
        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))

        container_ghost_state = state_pacman.state_data.dict_k_player_v_container_state[player]

        speed = GhostRules.GHOST_SPEED
        if container_ghost_state.scaredTimer > 0:
            speed /= 2.0
        vector = Actions.directionToVector(action, speed)
        container_ghost_state.container_position_vector = container_ghost_state.container_position_vector.get_container_position_vector_successor(
            vector)

    @staticmethod
    def decrementTimer(container_state: ContainerState):
        timer = container_state.scaredTimer

        if timer == 1:
            container_state.container_position_vector.position = nearestPoint(
                container_state.container_position_vector.position)
        container_state.scaredTimer = max(0, timer - 1)

    @staticmethod
    def checkDeath(state_pacman: StatePacman, player: Player):

        position_pacman = state_pacman.getPacmanPosition()

        if player.get_type_player() == TypePlayer.PACMAN:  # Pacman just moved; Anyone can kill him
            # for index in range(1, len(state.state_data.dict_k_player_v_container_state)):

            for player_inner, container_state in state_pacman.state_data.dict_k_player_v_container_state.items():

                if player_inner.get_type_player() == TypePlayer.GHOST:
                    position_ghost = container_state.container_position_vector.get_position()

                    if GhostRules.canKill(position_pacman, position_ghost):
                        GhostRules.collide(state_pacman, container_state, player_inner)
        else:
            container_state_ghost = state_pacman.state_data.dict_k_player_v_container_state.get(player)
            position_ghost = container_state_ghost.container_position_vector.get_position()

            if GhostRules.canKill(position_pacman, position_ghost):
                GhostRules.collide(state_pacman, container_state_ghost, player)

    @staticmethod
    def collide(state_pacman: StatePacman, container_ghost_state: ContainerState, player: Player):
        if container_ghost_state.scaredTimer > 0:
            state_pacman.state_data.scoreChange += 200
            GhostRules.placeGhost(state_pacman, container_ghost_state)
            container_ghost_state.scaredTimer = 0

            # Added for first-person
            state_pacman.state_data._dict_k_player_v_bool_eaten[player] = True
        else:
            if not state_pacman.state_data._win:
                state_pacman.state_data.scoreChange -= 500
                state_pacman.state_data._lose = True

    @staticmethod
    def canKill(pacmanPosition: TYPE_POSITION, ghostPosition: TYPE_POSITION):
        return manhattanDistance(ghostPosition, pacmanPosition) <= COLLISION_TOLERANCE

    @staticmethod
    def placeGhost(state_pacman: StatePacman, container_ghost_state: ContainerState):
        container_ghost_state.container_position_vector = container_ghost_state.container_position_vector_start
