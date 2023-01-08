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
from typing import Union

from pacman.game.container_vector import ContainerVector
from pacman.game.directions import Directions


class StateAgent:
    """
    AgentStates hold the game_state of an agent (container_vector, speed, scared, etc).
    """

    def __init__(self, container_vector: ContainerVector, is_pacman: bool):
        self.container_vector_start: ContainerVector = container_vector
        self.container_vector: ContainerVector = container_vector

        self.is_pacman: bool = is_pacman
        self.scaredTimer: int = 0

        # game_state below potentially used for contest only
        self.numCarrying: int = 0
        self.numReturned: int = 0

    def __str__(self):
        if self.is_pacman:
            return "Pacman: " + str(self.container_vector)
        else:
            return "Ghost: " + str(self.container_vector)

    def __eq__(self, other: Union[StateAgent, None]):
        if other is None:
            return False
        return self.container_vector == other.container_vector and self.scaredTimer == other.scaredTimer

    def __hash__(self):
        return hash(hash(self.container_vector) + 13 * hash(self.scaredTimer))

    def copy(self):
        state = StateAgent(self.container_vector_start, self.is_pacman)
        state.container_vector = self.container_vector
        state.scaredTimer = self.scaredTimer
        state.numCarrying = self.numCarrying
        state.numReturned = self.numReturned
        return state

    def get_position(self) -> Union[Tuple[int, ...], None]:
        if self.container_vector == None:
            return None
        return self.container_vector.get_position()

    def get_direction(self) -> Directions:
        return self.container_vector.get_direction()
