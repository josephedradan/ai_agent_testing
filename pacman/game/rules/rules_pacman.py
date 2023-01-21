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

from typing import Tuple
from typing import Union, TYPE_CHECKING, List

from pacman.game.actions import Actions
from pacman.game.directions import Action, Directions
from pacman.game.rules.common import SCARED_TIME
from pacman.game.rules.rules_agent import RulesAgent
from common.util import nearestPoint, manhattanDistance

if TYPE_CHECKING:
    from pacman.game.game_state import GameState


class PacmanRules(RulesAgent):
    """
    These functions govern how agent_pacman_ interacts with his environment under
    the classic game rules.
    """
    PACMAN_SPEED = 1

    @staticmethod
    def getLegalActions(game_state: GameState, index_agent: Union[int, None] = None) -> List[Directions]:
        return Actions.getPossibleActions(
            game_state.getPacmanState().container_vector,
            game_state.game_state_data.layout.walls
        )

    @staticmethod
    def applyAction(game_state: GameState, action: Action, index_agent: Union[int, None] = None):

        legal = PacmanRules.getLegalActions(game_state)
        if action not in legal:
            raise Exception("Illegal action " + str(action))

        pacmanState = game_state.game_state_data.list_state_agent[0]

        # Update ContainerVector
        vector = Actions.directionToVector(action, PacmanRules.PACMAN_SPEED)
        pacmanState.container_vector = pacmanState.container_vector.get_container_vector_successor(
            vector)

        # Eat
        next = pacmanState.container_vector.get_position()
        nearest = nearestPoint(next)
        if manhattanDistance(nearest, next) <= 0.5:
            # Remove food
            PacmanRules._consume(nearest, game_state)

    @staticmethod
    def _consume(position:Tuple[int, int], game_state: GameState):
        x, y = position
        # Eat food
        if game_state.game_state_data.grid_food[x][y]:
            game_state.game_state_data.scoreChange += 10
            game_state.game_state_data.grid_food = game_state.game_state_data.grid_food.copy()
            game_state.game_state_data.grid_food[x][y] = False
            game_state.game_state_data._foodEaten = position
            # TODO: cache numFood?
            numFood = game_state.getNumFood()
            if numFood == 0 and not game_state.game_state_data._lose:
                game_state.game_state_data.scoreChange += 500
                game_state.game_state_data._win = True
        # Eat capsule
        if (position in game_state.getCapsules()):
            game_state.game_state_data.list_capsule.remove(position)
            game_state.game_state_data._capsuleEaten = position
            # Reset all list_agent_ghost' scared timers
            for index in range(1, len(game_state.game_state_data.list_state_agent)):
                game_state.game_state_data.list_state_agent[index].scaredTimer = SCARED_TIME
