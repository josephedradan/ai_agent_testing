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

from common.util import nearestPoint
from pacman.agent.container_state import ContainerState
from pacman.game.action_direction import ActionDirection
from pacman.game.handler_action_direction import HandlerActionDirection
from pacman.game.player_pacman import PlayerPacman
from pacman.game.rules.rules_pacman import RulesPacman

if TYPE_CHECKING:
    from common.state_pacman import StatePacman


class RulesPacmanGhost(RulesPacman):
    """
    These functions dictate how ghosts interact with their environment.
    """
    GHOST_SPEED = 1.0

    @staticmethod
    def getLegalActions(state_pacman: StatePacman, player_pacman: PlayerPacman) -> List[ActionDirection]:
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

        container_position_direction = state_pacman.get_container_state_GHOST(
            player_pacman.get_agent()
        ).get_container_position_direction()

        list_action_direction_possible = HandlerActionDirection.get_list_action_direction_possible(
            container_position_direction,
            state_pacman.state_data_pacman.layout_pacman.walls
        )

        reverse = HandlerActionDirection.reverse_action_direction(
            container_position_direction._direction
        )

        # GHOST DONT STOP SO REMOVE IT
        # if ActionDirection.STOP in list_action_direction_possible:
        #     list_action_direction_possible.remove(ActionDirection.STOP)

        # GHOST DONT STOP SO REMOVE IT (discard removes the item but does not throw if it does not exist)
        # list_action_direction_possible.discard(ActionDirection.STOP)

        # Remove throws if item does not exist
        try:
            # GHOST DONT STOP SO REMOVE IT
            list_action_direction_possible.remove(ActionDirection.STOP)
        except ValueError as e:
            pass

        # DONT REVERSE IF GHOST HAS MORE THAN 1 MOVE
        # if reverse in list_action_direction_possible and len(list_action_direction_possible) > 1:
        #     list_action_direction_possible.remove(reverse)

        # Remove throws if item does not exist
        try:
            # DONT REVERSE IF GHOST HAS MORE THAN 1 MOVE
            if len(list_action_direction_possible) > 1:
                list_action_direction_possible.remove(reverse)
        except ValueError as e:
            pass

        return list_action_direction_possible

    @staticmethod
    def applyAction(state_pacman_current: StatePacman, action: ActionDirection, player_pacman_ghost: PlayerPacman):
        """
        Applies the action to appropriate ContainerState given PlayerPacman (Should be a ghost)

        :param state_pacman_current:
        :param action:
        :param player_pacman_ghost:
        :return:
        """
        list_action_direction_legal = RulesPacmanGhost.getLegalActions(state_pacman_current, player_pacman_ghost)

        # if not isinstance(player_pacman.get_agent(), AgentPacmanGhostRandom):
        #     print("---------ASD")
        #     print(player_pacman)

        # if action in list_action_direction_legal:
        #     print("FFFFFFFFFFFFFFFA")
        #     print(player_pacman, list_action_direction_legal, action)

        if action not in list_action_direction_legal:
            print("Illegal ghost action AAAAA ACTION NOT IN LEGAL",
                  player_pacman_ghost,
                  action,
                  list_action_direction_legal)
            raise Exception("Illegal ghost action " + str(action))

        container_state_ghost = state_pacman_current.state_data_pacman.dict_k_player_v_container_state[
            player_pacman_ghost]

        speed = RulesPacmanGhost.GHOST_SPEED

        # If ghost is scared, decrease their speed
        if container_state_ghost.time_scared > 0:
            speed /= 2.0

        vector = HandlerActionDirection.get_vector_from_action_direction(action, speed)

        container_state_ghost._container_position_direction = (
            container_state_ghost._container_position_direction.get_container_position_direction_successor(vector)
        )

    @staticmethod
    def _decrementTimer(container_state: ContainerState):
        timer = container_state.time_scared

        if timer == 1:
            container_state._container_position_direction.set_position(
                nearestPoint(container_state._container_position_direction.get_vector_position()))
        container_state.time_scared = max(0, timer - 1)

    @staticmethod
    def update_state_pacman_and_player_pacman(state_pacman: StatePacman, player_pacman: PlayerPacman):

        container_state = state_pacman.state_data_pacman.dict_k_player_v_container_state.get(player_pacman)

        RulesPacmanGhost._decrementTimer(container_state)

    @staticmethod
    def process_state_pacman_and_player_position(state_pacman: StatePacman, player_pacman: PlayerPacman):
        """

        Notes:
            Only called in StatePacman generate_successor

        :param state_pacman:
        :param player_pacman:
        :return:
        """
        position_pacman = state_pacman.getPacmanPosition()

        # if player_pacman.get_type_player_pacman() == EnumPlayerPacman.PACMAN:  # Pacman just moved; Anyone can kill him
        #     # for index in range(1, len(state.state_data.dict_k_player_v_container_state)):
        #
        #     list_player_pacman_ghost = (
        #         state_pacman.state_data_pacman.dict_k_enum_type_player_pacman_v_list_player_pacman.get(
        #             EnumPlayerPacman.GHOST)
        #     )
        #
        #     for player_pacman_ghost in list_player_pacman_ghost:
        #
        #         container_state = state_pacman.state_data_pacman.dict_k_player_v_container_state.get(player_pacman_ghost)
        #
        #         position_ghost = container_state._container_position_direction.get_vector_position()
        #
        #         if RulesPacmanGhost._check_collision(position_pacman, position_ghost):
        #             RulesPacmanGhost._process_player_pacman_collision(state_pacman, container_state, player_pacman_ghost)
        # else:
        #     container_state_ghost = state_pacman.state_data_pacman.dict_k_player_v_container_state.get(player_pacman)
        #     position_ghost = container_state_ghost._container_position_direction.get_vector_position()
        #
        #     if RulesPacmanGhost._check_collision(position_pacman, position_ghost):
        #         RulesPacmanGhost._process_player_pacman_collision(state_pacman, container_state_ghost, player_pacman)

        container_state_ghost = state_pacman.state_data_pacman.dict_k_player_v_container_state.get(player_pacman)
        position_ghost = container_state_ghost._container_position_direction.get_vector_position()

        if RulesPacmanGhost._check_collision(position_pacman, position_ghost):
            RulesPacmanGhost._process_player_pacman_collision(state_pacman, container_state_ghost, player_pacman)
