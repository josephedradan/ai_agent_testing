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
from pacman.util import nearestPoint, manhattanDistance

if TYPE_CHECKING:
    from pacman.game.game_state import GameState


class PacmanRules(RulesAgent):
    """
    These functions govern how agent_pacman_ interacts with his environment under
    the classic game rules.
    """
    PACMAN_SPEED = 1

    @staticmethod
    def getLegalActions(state: GameState, index_agent: Union[int, None] = None) -> List[Directions]:
        return Actions.getPossibleActions(
            state.getPacmanState().container_vector,
            state.data.layout.walls
        )

    @staticmethod
    def applyAction(state: GameState, action: Action, index_agent: Union[int, None] = None):

        legal = PacmanRules.getLegalActions(state)
        if action not in legal:
            raise Exception("Illegal action " + str(action))

        pacmanState = state.data.list_state_agent[0]

        # Update ContainerVector
        vector = Actions.directionToVector(action, PacmanRules.PACMAN_SPEED)
        pacmanState.container_vector = pacmanState.container_vector.get_container_vector_successor(
            vector)

        # Eat
        next = pacmanState.container_vector.get_position()
        nearest = nearestPoint(next)
        if manhattanDistance(nearest, next) <= 0.5:
            # Remove food
            PacmanRules.consume(nearest, state)

    @staticmethod
    def consume(position:Tuple[int,int], game_state: GameState):
        x, y = position
        # Eat food
        if game_state.data.food[x][y]:
            game_state.data.scoreChange += 10
            game_state.data.food = game_state.data.food.copy()
            game_state.data.food[x][y] = False
            game_state.data._foodEaten = position
            # TODO: cache numFood?
            numFood = game_state.getNumFood()
            if numFood == 0 and not game_state.data._lose:
                game_state.data.scoreChange += 500
                game_state.data._win = True
        # Eat capsule
        if (position in game_state.getCapsules()):
            game_state.data.list_capsule.remove(position)
            game_state.data._capsuleEaten = position
            # Reset all list_agent_ghost' scared timers
            for index in range(1, len(game_state.data.list_state_agent)):
                game_state.data.list_state_agent[index].scaredTimer = SCARED_TIME
