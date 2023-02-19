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

from typing import List
from typing import TYPE_CHECKING

from common.util import manhattanDistance
from common.util import nearestPoint
from pacman.agent.container_state import ContainerState
from pacman.game.handleractiondirection import HandlerActionDirection
from pacman.game.actiondirection import Action
from pacman.game.actiondirection import ActionDirection
from pacman.game.player_pacman import PlayerPacman
from pacman.game.rules.common import COLLISION_TOLERANCE
from pacman.game.rules.rules_agent import RulesAgent
from pacman.game.type_player_pacman import TypePlayerPacman
from pacman.types_ import TYPE_VECTOR

if TYPE_CHECKING:
    from common.state_pacman import StatePacman


class GhostRules(RulesAgent):
    """
    These functions dictate how ghosts interact with their environment.
    """
    GHOST_SPEED = 1.0

    @staticmethod
    def getLegalActions(state_pacman: StatePacman, player: PlayerPacman) -> List[ActionDirection]:
        """
        Ghosts cannot stop, and cannot turn around unless they
        reach a dead end, but can turn 90 degrees at intersections.

        JOSEPH NOTES:
            1. GHOST DONT STOP SO IT IS REMOVED
            2. DONT REVERSE IF GHOST HAS MORE THAN 1 MOVE

        """

        # TODO: JOSEPH COMMENT JOSEPH JUMP
        # print('----------------------', player)
        # pprint(state.state_data.dict_k_player_v_container_state)

        #
        # for a, b in state.state_data.dict_k_player_v_container_state.items():
        #     print(hash(a), hash(b))

        # print("---- player", player)
        # print("state.state_data.dict_k_player_v_container_state",
        #       state.state_data.dict_k_player_v_container_state)
        # print("state.get_state_container_GHOST(player)",
        #       state.get_state_container_GHOST(player))

        agent = player.get_agent()

        container_position_direction = state_pacman.get_container_state_GHOST(agent)._container_position_direction

        possibleActions = HandlerActionDirection.getPossibleActions(
            container_position_direction,
            state_pacman.state_data.layout_pacman.walls
        )

        reverse = HandlerActionDirection.reverse_action_direction(container_position_direction._direction)

        # GHOST DONT STOP SO REMOVE IT
        if ActionDirection.STOP in possibleActions:
            possibleActions.remove(ActionDirection.STOP)

        # DONT REVERSE IF GHOST HAS MORE THAN 1 MOVE
        if reverse in possibleActions and len(possibleActions) > 1:
            possibleActions.remove(reverse)

        return possibleActions

    @staticmethod
    def applyAction(state_pacman: StatePacman, action: Action, player: PlayerPacman):

        legal = GhostRules.getLegalActions(state_pacman, player)
        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))

        container_ghost_state = state_pacman.state_data.dict_k_player_v_container_state[player]

        speed = GhostRules.GHOST_SPEED

        if container_ghost_state.time_scared > 0:
            speed /= 2.0

        vector = HandlerActionDirection.get_vector_from_action_direction(action, speed)

        container_ghost_state._container_position_direction = (
            container_ghost_state._container_position_direction.get_container_position_direction_successor(vector)
        )

    @staticmethod
    def decrementTimer(container_state: ContainerState):
        timer = container_state.time_scared

        if timer == 1:
            container_state._container_position_direction.set_position(
                nearestPoint(container_state._container_position_direction.get_position()))
        container_state.time_scared = max(0, timer - 1)

    @staticmethod
    def checkDeath(state_pacman: StatePacman, player: PlayerPacman):

        position_pacman = state_pacman.getPacmanPosition()

        if player.get_type_player_pacman() == TypePlayerPacman.PACMAN:  # Pacman just moved; Anyone can kill him
            # for index in range(1, len(state.state_data.dict_k_player_v_container_state)):

            for player_inner, container_state in state_pacman.state_data.dict_k_player_v_container_state.items():

                if player_inner.get_type_player_pacman() == TypePlayerPacman.GHOST:
                    position_ghost = container_state._container_position_direction.get_position()

                    if GhostRules.canKill(position_pacman, position_ghost):
                        GhostRules.collide(state_pacman, container_state, player_inner)
        else:
            container_state_ghost = state_pacman.state_data.dict_k_player_v_container_state.get(player)
            position_ghost = container_state_ghost._container_position_direction.get_position()

            if GhostRules.canKill(position_pacman, position_ghost):
                GhostRules.collide(state_pacman, container_state_ghost, player)

    @staticmethod
    def collide(state_pacman: StatePacman, container_ghost_state: ContainerState, player: PlayerPacman):
        if container_ghost_state.time_scared > 0:
            state_pacman.state_data.scoreChange += 200
            GhostRules.placeGhost(state_pacman, container_ghost_state)
            container_ghost_state.time_scared = 0

            # Added for first-person
            state_pacman.state_data._dict_k_player_v_bool_eaten[player] = True
        else:
            if not state_pacman.state_data._win:
                state_pacman.state_data.scoreChange -= 500
                state_pacman.state_data._lose = True

    @staticmethod
    def canKill(pacmanPosition: TYPE_VECTOR, ghostPosition: TYPE_VECTOR):
        return manhattanDistance(ghostPosition, pacmanPosition) <= COLLISION_TOLERANCE

    @staticmethod
    def placeGhost(state_pacman: StatePacman, container_ghost_state: ContainerState):
        container_ghost_state._container_position_direction = container_ghost_state._container_position_direction_start
