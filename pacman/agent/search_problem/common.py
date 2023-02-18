"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/12/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import List
from typing import Tuple
from typing import Union

from pacman.types_ import TYPE_VECTOR


class HashableGoal:
    # Use less memory
    __slots__ = ["position", "list_tuple_order_traveled"]

    def __init__(self, position: TYPE_VECTOR, list_tuple_order_traveled: List[Union[TYPE_VECTOR, None]]):
        """
        Probably because all of the algorithms inside of search.py prevent you from moving into a _position that you
        already traversed, you can use an additional parameter to act similar to changing universes once you have
        reached a goal.

        Basically, you hash the _position along side the length of the set that contains the goal positions.
        When you reach a goal _position, the set's length is changed because you remove that _position from that set.
        The removal of a goal _position and the creation of the set is done before the creation of this object based
        on the previous HashableGoal object's list_tuple_order_traveled.

        """

        self.position = position
        self.list_tuple_order_traveled = list_tuple_order_traveled.copy()

    def __hash__(self):
        """
        Hash the _position along side the length of the set of goal positions that you haven't reached

        Notes:
            tuple (No Nones)
                with check in isGoalState -> Fail, Search nodes expanded: 149, cost of 26
                No check in isGoalState -> Success, Search nodes expanded: 283, cost of 29
                Can cause different paths to enter the same universe

            len
                with check in isGoalState -> Fail, Search nodes expanded: 88, cost of 26,
                No check in isGoalState -> Success, Search nodes expanded: 105, cost of 31
                Can cause different paths to enter the same universe

            frozenset
                with check in isGoalState -> Fail, Search nodes expanded: 149, cost of 26
                No check in isGoalState -> Success, Search nodes expanded: 283, cost of 29
                Can cause different paths to enter the same universe

            tuple (With Nones) V1
                with check in isGoalState -> Fail, Search nodes expanded: 447, cost of 28
                No check in isGoalState -> Success, Search nodes expanded: 494, cost of 29
                Can probably not cause different paths to enter the same universe because the hash
                is based on the order of tuple corners visited and the tuple corner itself.

             tuple (Just adding the _position of a corner in a list of corners visited, then hashing
             that list as a tuple)
                with check in isGoalState -> Fail, Search nodes expanded: 447, cost of 28
                No check in isGoalState -> Success, Search nodes expanded: 494, cost of 29
                Can probably not cause different paths to enter the same universe because the hash
                is based on the order of tuple corners visited and the tuple corner itself.

        :return:
        """
        return hash((self.position, tuple(self.list_tuple_order_traveled)))

    def __eq__(self, other):
        if isinstance(other, HashableGoal):
            return self.__hash__() == other.__hash__()
        return False

    # V1
    # def is_done(self):
    #     """
    #     If set_position_remaining is empty,it means you reached all goal positions.
    #
    #     :return:
    #     """
    #     if isinstance(self.list_tuple_order_traveled[-1], Tuple):
    #         return True
    #     return False
