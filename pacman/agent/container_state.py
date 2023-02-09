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

from pacman.game.container_position_vector import ContainerPositionVector
from pacman.game.directions import Directions


class ContainerState:
    """
    AgentStates hold the state_pacman of an player (container_position_vector, speed, scared, etc).

    NOTES:
        CREATED ONCE IN state_data_pacman

    """

    def __init__(self, container_position_vector: ContainerPositionVector):
        self.container_position_vector_start: ContainerPositionVector = container_position_vector
        self.container_position_vector: ContainerPositionVector = container_position_vector

        self.scaredTimer: int = 0

        # state_pacman below potentially used for contest only
        self.numCarrying: int = 0
        self.numReturned: int = 0

    def __str__(self):
        # if self.is_pacman:
        #     return "Pacman: " + str(self.container_position_vector)
        # else:
        #     return "Ghost: " + str(self.container_position_vector)

        return str(self.container_position_vector)

    def __eq__(self, other: Union[ContainerState, None]):
        if other is None:
            return False
        return (
                self.container_position_vector == other.container_position_vector and
                self.scaredTimer == other.scaredTimer
        )

    def __hash__(self):
        # return hash(hash(self.container_position_vector) + 13 * hash(self.scaredTimer))
        return hash((hash(self.container_position_vector), hash(self.scaredTimer)))

    def copy(self) -> ContainerState:
        state = ContainerState(self.container_position_vector_start)
        state.container_position_vector = self.container_position_vector
        state.scaredTimer = self.scaredTimer
        state.numCarrying = self.numCarrying
        state.numReturned = self.numReturned
        return state

    def get_position(self) -> Union[Tuple[int, ...], None]:
        if self.container_position_vector == None:
            return None
        return self.container_position_vector.get_position()

    def get_direction(self) -> Directions:
        return self.container_position_vector.get_direction()
