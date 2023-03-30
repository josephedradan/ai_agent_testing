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

from abc import ABC
from abc import abstractmethod
from typing import List
from typing import TYPE_CHECKING

from common.util import manhattanDistance
from pacman.agent.container_state import ContainerState
from pacman.game.handler_action_direction import HandlerActionDirection
from pacman.game.rules.common import COLLISION_TOLERANCE
from pacman.types_ import TYPE_VECTOR

if TYPE_CHECKING:
    from common.state_pacman import StatePacman
    from pacman.game.player_pacman import PlayerPacman
    from pacman.game.action_direction import ActionDirection
    from pacman.game.action_direction import Action


class RulesPacman(ABC):

    @staticmethod
    @abstractmethod
    def getLegalActions(state_pacman: StatePacman, player_pacman: PlayerPacman) -> List[ActionDirection]:
        """
        Returns a list of possible actions.
        """
        pass

        container_position_direction = state_pacman.get_container_state_GHOST(
            player_pacman.get_agent()).get_container_position_direction()

        return HandlerActionDirection.get_list_action_direction_possible(
            container_position_direction,
            state_pacman.state_data_pacman.layout_pacman.walls
        )

    @staticmethod
    @abstractmethod
    def applyAction(state_pacman: StatePacman, action: Action, player_pacman: PlayerPacman):
        """
        Edits the state to reflect the results of the action.
        """
        ...

    @staticmethod
    @abstractmethod
    def update_state_pacman_and_player_pacman(state_pacman: StatePacman, player_pacman: PlayerPacman):
        """
        Updates the player

        :param state_pacman:
        :param player_pacman:
        :return:
        """
        ...


    @staticmethod
    @abstractmethod
    def process_state_pacman_and_player_position(state_pacman: StatePacman, player_pacman: PlayerPacman):
        ...


    @staticmethod
    def _process_player_pacman_collision(state_pacman: StatePacman, container_state: ContainerState, player: PlayerPacman):
        """



        Handle collision between ghost and pacman

        :param state_pacman:
        :param container_state:
        :param player:
        :return:
        """

        # If ghost is scared
        if container_state.time_scared > 0:
            state_pacman.state_data_pacman.scoreChange += 200  # Add points to pacman
            RulesPacman.move_container_state(state_pacman, container_state)  # Move ghost to spawn
            container_state.time_scared = 0  # Make ghost not scared

            # Added for first-person
            state_pacman.state_data_pacman._dict_k_player_v_bool_eaten[player] = True

        # Ghost not scared
        else:
            if not state_pacman.state_data_pacman._win:
                state_pacman.state_data_pacman.scoreChange -= 500
                state_pacman.state_data_pacman._lose = True


    @staticmethod
    def _check_collision(pacmanPosition: TYPE_VECTOR, ghostPosition: TYPE_VECTOR):
        """
        Check if to vectors

        :param pacmanPosition:
        :param ghostPosition:
        :return:
        """
        # print(ghostPosition, pacmanPosition, manhattanDistance(ghostPosition, pacmanPosition))
        return manhattanDistance(ghostPosition, pacmanPosition) <= COLLISION_TOLERANCE  # Must have tolerance else crash
        # return manhattanDistance(ghostPosition, pacmanPosition)


    @staticmethod
    def move_container_state(state_pacman: StatePacman, container_state: ContainerState):
        container_state._container_position_direction = container_state._container_position_direction_start
