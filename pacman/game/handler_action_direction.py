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

from common.action import Action
from common.grid import Grid
from pacman.game.action_direction import ActionDirection

if TYPE_CHECKING:
    from pacman.types_ import TYPE_VECTOR
    from pacman.game.container_position_direction import ContainerPositionDirection


class HandlerActionDirection:
    """
    A collection of static methods for manipulating move actions.
    """
    # ActionDirection
    dict_k_direction_v_type_vector = {ActionDirection.WEST: (-1, 0),
                                      ActionDirection.STOP: (0, 0),
                                      ActionDirection.EAST: (1, 0),
                                      ActionDirection.NORTH: (0, 1),
                                      ActionDirection.SOUTH: (0, -1)}

    # IMPORTANT: DO NOT CHANGE THIS ORDER OR ELSE TESTCASES WILL FAIL
    _list_tuple__action_direction__type_vector: List[Tuple[ActionDirection, TYPE_VECTOR]] = [
        (ActionDirection.WEST, (-1, 0)),
        (ActionDirection.STOP, (0, 0)),
        (ActionDirection.EAST, (1, 0)),
        (ActionDirection.NORTH, (0, 1)),
        (ActionDirection.SOUTH, (0, -1))
    ]

    dict_action_direction_reverse = {
        ActionDirection.NORTH: ActionDirection.SOUTH,
        ActionDirection.SOUTH: ActionDirection.NORTH,
        ActionDirection.WEST: ActionDirection.EAST,
        ActionDirection.EAST: ActionDirection.WEST
    }

    TOLERANCE = .001

    @staticmethod
    def reverse_action_direction(action: ActionDirection) -> ActionDirection:
        return HandlerActionDirection.dict_action_direction_reverse.get(action, action)

    @staticmethod
    def get_action_direction_from_vector(vector: TYPE_VECTOR) -> ActionDirection:

        dx, dy = vector

        if dy > 0:
            return ActionDirection.NORTH
        if dy < 0:
            return ActionDirection.SOUTH
        if dx < 0:
            return ActionDirection.WEST
        if dx > 0:
            return ActionDirection.EAST
        return ActionDirection.STOP

    @staticmethod
    def get_vector_from_action_direction(action: Action, speed: float = 1.0) -> TYPE_VECTOR:
        dx, dy = HandlerActionDirection.dict_k_direction_v_type_vector[action]
        return (dx * speed, dy * speed)

    @staticmethod
    def get_list_action_direction_possible(container_position_direction: ContainerPositionDirection,
                                           walls: Grid) -> List[ActionDirection]:
        """

        Notes:
            Cannot use set because it will break some functionality

        :param container_position_direction:
        :param walls:
        :return:
        """
        list_action_direction_possible = []

        x, y = container_position_direction.get_vector_position()

        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int) > HandlerActionDirection.TOLERANCE):
            return [container_position_direction.get_direction()]

        for action_direction, vector in HandlerActionDirection._list_tuple__action_direction__type_vector:
            dx, dy = vector

            y_next = y_int + dy
            x_next = x_int + dx

            # If the next vector position is not a wall then its action direction is a possible action
            if not walls[x_next][y_next]:
                list_action_direction_possible.append(action_direction)

        return list_action_direction_possible

    @staticmethod
    def get_list_action_direction_legal(vector_position: TYPE_VECTOR, grid: Grid) -> List[TYPE_VECTOR]:
        # TODO FUNCTION NEEDS TO BE GENERALIZED
        # TODO USE NUMPY

        x, y = vector_position
        x_int_shifted, y_int_shifted = int(x + 0.5), int(y + 0.5)

        list_type_vector = []

        for action_direction, type_vector in HandlerActionDirection._list_tuple__action_direction__type_vector:
            dx, dy = type_vector
            next_x = x_int_shifted + dx

            if next_x < 0 or next_x >= grid.width:
                continue

            next_y = y_int_shifted + dy

            if next_y < 0 or next_y >= grid.height:
                continue

            if not grid[next_x][next_y]:
                list_type_vector.append((next_x, next_y))

        return list_type_vector

    @staticmethod
    def get_type_vector_successor(position: TYPE_VECTOR,
                                  action: ActionDirection) -> TYPE_VECTOR:  # TODO FUNCTION NEEDS TO BE GENERALIZED
        dx, dy = HandlerActionDirection.get_vector_from_action_direction(action)
        x, y = position
        return (x + dx, y + dy)
