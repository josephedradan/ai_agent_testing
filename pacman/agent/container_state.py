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

from typing import Union

from pacman.game.container_position_direction import ContainerPositionDirection
from pacman.game.actiondirection import ActionDirection
from pacman.types_ import TYPE_VECTOR


class ContainerState:
    """
    Holds the state of an player (_container_position_direction, speed, scared, etc).

    NOTES:
        CREATED ONCE IN state_data_pacman

    """
    _container_position_direction: ContainerPositionDirection
    _container_position_direction_start: ContainerPositionDirection

    def __init__(self, container_position_direction: ContainerPositionDirection):
        self._container_position_direction_start = container_position_direction

        # This one will differ on copies
        self._container_position_direction = container_position_direction

        self.time_scared: int = 0

        # state below potentially used for contest only
        self.numCarrying: int = 0
        self.numReturned: int = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self._container_position_direction)

    def __eq__(self, other: Union[ContainerState, None]):
        if isinstance(other, ContainerState):
            return (
                    self._container_position_direction == other._container_position_direction and
                    self.time_scared == other.time_scared and
                    self.numCarrying == other.numCarrying and
                    self.numReturned == other.numReturned
            )
        return False

    def __hash__(self):
        return hash((
            self._container_position_direction,
            self.time_scared
        ))

    def get_copy_deep(self) -> ContainerState:
        container_state_new = ContainerState(self._container_position_direction_start)

        container_state_new._container_position_direction = self._container_position_direction
        container_state_new.time_scared = self.time_scared
        container_state_new.numCarrying = self.numCarrying
        container_state_new.numReturned = self.numReturned

        return container_state_new

    def get_position(self) -> Union[TYPE_VECTOR, None]:
        if self._container_position_direction is None:
            return None

        return self._container_position_direction.get_position()

    def get_direction(self) -> ActionDirection:
        return self._container_position_direction.get_direction()

    def get_container_position_direction(self) -> ContainerPositionDirection:
        return self._container_position_direction

    def get_container_position_direction_start(self) -> ContainerPositionDirection:
        return self._container_position_direction_start
