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

from typing import Union

from pacman.game.handleractiondirection import HandlerActionDirection
from pacman.game.actiondirection import ActionDirection

from pacman.types_ import TYPE_VECTOR


class ContainerPositionDirection:
    __slots__ = ("_position", "_direction")

    _position: TYPE_VECTOR
    _direction: ActionDirection

    def __init__(self, position: TYPE_VECTOR, direction: ActionDirection):
        """

        :param position:
        :param direction:
        """

        """
        Use the below if __setattr__ does not assign anything (The below will make reassignment of instance 
        variables not possible)
        """
        # super(ContainerPositionDirection, self).__setattr__("_position", _position)
        # super(ContainerPositionDirection, self).__setattr__("_direction", _direction)

        self._position = position
        self._direction = direction

        #####

    def get_vector_position(self) -> TYPE_VECTOR:
        return self._position

    def set_position(self, vector: TYPE_VECTOR):
        self._position = vector

    def get_direction(self) -> ActionDirection:
        return self._direction

    def set_direction(self, directions: ActionDirection):
        self._direction = directions

    def __eq__(self, container_position_direction_possible: Union[ContainerPositionDirection, None]):
        if isinstance(container_position_direction_possible, ContainerPositionDirection):
            return (self._position == container_position_direction_possible._position and
                    self._direction == container_position_direction_possible._direction)
        return False

    def __hash__(self):
        return hash((self._position, self._direction))

    def __str__(self):
        return "(Position: {} Direction: {})".format(self._position, self._direction)

    def get_container_position_direction_successor(self,
                                                   vector: TYPE_VECTOR) -> ContainerPositionDirection:
        """
        Add self._position and the vector together to get a new vector and then
        """

        # Vector addition
        vector_new = tuple(e1 + e2 for e1, e2 in zip(self._position, vector))

        direction_new = HandlerActionDirection.get_action_direction_from_vector(vector)

        if direction_new == ActionDirection.STOP:
            direction_new = self._direction

        return ContainerPositionDirection(vector_new, direction_new)

    # def __setattr__(self, key, value):
    #     raise Exception('Cannot reassign "{}" to "{}"'.format(key, value))
