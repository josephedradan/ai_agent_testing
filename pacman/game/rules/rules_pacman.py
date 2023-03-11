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
from typing import Set
from typing import TYPE_CHECKING
from typing import Tuple
from typing import Union

from common.util import manhattanDistance
from common.util import nearestPoint
from pacman.game.handler_action_direction import HandlerActionDirection
from pacman.game.action_direction import Action
from pacman.game.action_direction import ActionDirection
from pacman.game.player_pacman import PlayerPacman
from pacman.game.type_player_pacman import EnumPlayerPacman
from pacman.game.rules.common import SCARED_TIME
from pacman.game.rules.rules_agent import RulesPacman
from pacman.types_ import TYPE_VECTOR

if TYPE_CHECKING:
    from common.state_pacman import StatePacman


class RulesPacmanPacman(RulesPacman):
    """
    These functions govern how pacman interacts with his environment under
    the classic game rules.
    """
    PACMAN_SPEED = 1

    @staticmethod
    def getLegalActions(state_pacman: StatePacman, player_pacman: PlayerPacman) -> List[ActionDirection]:

        container_position_direction = state_pacman.get_container_state_GHOST(
            player_pacman.get_agent()).get_container_position_direction()

        return HandlerActionDirection.get_list_action_direction_possible(
            container_position_direction,
            state_pacman.state_data.layout_pacman.walls
        )

    @staticmethod
    def applyAction(state_pacman_current: StatePacman, action: ActionDirection, player_pacman: PlayerPacman):
        """
        Applies the action to appropriate ContainerState given PlayerPacman

        :param state_pacman_current:
        :param action:
        :param player_pacman:
        :return:
        """
        list_action_direction_legal = RulesPacmanPacman.getLegalActions(state_pacman_current, player_pacman)

        if action not in list_action_direction_legal:
            raise Exception("Illegal action " + str(action))

        pacmanState = state_pacman_current.get_container_state_GHOST(player_pacman.get_agent())

        # Update ContainerVector
        vector = HandlerActionDirection.get_vector_from_action_direction(action, RulesPacmanPacman.PACMAN_SPEED)
        pacmanState._container_position_direction = pacmanState._container_position_direction.get_container_position_direction_successor(
            vector
        )

        # Eat
        next = pacmanState._container_position_direction.get_vector_position()
        nearest = nearestPoint(next)
        if manhattanDistance(nearest, next) <= 0.5:
            # Remove food
            RulesPacmanPacman._consume(nearest, state_pacman_current)

    @staticmethod
    def _consume(position: TYPE_VECTOR, state_pacman: StatePacman):
        x, y = position

        # Eat food
        if state_pacman.state_data.grid_food[x][y]:
            state_pacman.state_data.scoreChange += 10
            state_pacman.state_data.grid_food = state_pacman.state_data.grid_food.copy()
            state_pacman.state_data.grid_food[x][y] = False
            state_pacman.state_data._foodEaten = position
            # TODO: cache numFood?
            numFood = state_pacman.getNumFood()
            if numFood == 0 and not state_pacman.state_data._lose:
                state_pacman.state_data.scoreChange += 500
                state_pacman.state_data._win = True

        # Eat capsule
        if (position in state_pacman.getCapsules()):
            state_pacman.state_data.list_capsule.remove(position)
            state_pacman.state_data._capsuleEaten = position

            # Reset all ghosts' scared timers
            # for index in range(1, len(state.state_data.dict_k_player_v_container_state)):
            #     state.state_data.dict_k_player_v_container_state[index].time_scared = SCARED_TIME

            # Reset all ghosts' scared timers
            for player in state_pacman.state_data.dict_k_player_v_container_state:

                if player.type_player == EnumPlayerPacman.GHOST:
                    state_pacman.state_data.dict_k_player_v_container_state.get(player).time_scared = SCARED_TIME
