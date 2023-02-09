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
from typing import Tuple
from typing import Union

from common.util import manhattanDistance
from common.util import nearestPoint
from pacman.game.actions import Actions
from pacman.game.directions import Action
from pacman.game.directions import Directions
from pacman.game.player import Player
from pacman.game.type_player import TypePlayer
from pacman.game.rules.common import SCARED_TIME
from pacman.game.rules.rules_agent import RulesAgent

if TYPE_CHECKING:
    from common.state_pacman import StatePacman


class PacmanRules(RulesAgent):
    """
    These functions govern how pacman interacts with his environment under
    the classic game rules.
    """
    PACMAN_SPEED = 1

    @staticmethod
    def getLegalActions(state_pacman: StatePacman, player: Player) -> List[Directions]:

        container_position_vector = state_pacman.get_state_container_GHOST(player).container_position_vector

        return Actions.getPossibleActions(
            container_position_vector,
            state_pacman.state_data.layout.walls
        )

    @staticmethod
    def applyAction(state_pacman: StatePacman, action: Action, player: Player):

        actions_legal = PacmanRules.getLegalActions(state_pacman, player)

        if action not in actions_legal:
            raise Exception("Illegal action " + str(action))

        pacmanState = state_pacman.get_state_container_GHOST(player)

        # Update ContainerVector
        vector = Actions.directionToVector(action, PacmanRules.PACMAN_SPEED)
        pacmanState.container_position_vector = pacmanState.container_position_vector.get_container_position_vector_successor(
            vector)

        # Eat
        next = pacmanState.container_position_vector.get_position()
        nearest = nearestPoint(next)
        if manhattanDistance(nearest, next) <= 0.5:
            # Remove food
            PacmanRules._consume(nearest, state_pacman)

    @staticmethod
    def _consume(position: Tuple[int, int], state_pacman: StatePacman):
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
            # for index in range(1, len(state_pacman.state_data.dict_k_player_v_container_state)):
            #     state_pacman.state_data.dict_k_player_v_container_state[index].scaredTimer = SCARED_TIME

            # Reset all ghosts' scared timers
            for player in state_pacman.state_data.dict_k_player_v_container_state:

                if player.type_player == TypePlayer.GHOST:
                    state_pacman.state_data.dict_k_player_v_container_state.get(player).scaredTimer = SCARED_TIME
