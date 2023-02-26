"""
Date created: 1/12/2023

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

from typing import Any
from typing import List
from typing import TYPE_CHECKING
from typing import Tuple
from typing import Union

from pacman.agent import Agent
from pacman.agent.search_problem import SearchProblem
from pacman.agent.search_problem.common import HashableGoal
from pacman.game.handler_action_direction import HandlerActionDirection
from pacman.game.action_direction import ActionDirection

if TYPE_CHECKING:
    pass
    from common.state_pacman import StatePacman


class CornersProblem(SearchProblem):
    """
    This search problem_multi_agent_tree finds paths through all four corners of a str_path_layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, agent: Agent, state_pacman_starting: StatePacman):  # TODO: SHOULD AGENT BE GIVEN HERE???
        """
        Stores the walls, pacman's starting _position and corners.
        """
        super().__init__()

        self.agent = agent

        self.walls = state_pacman_starting.getWalls()

        self.startingPosition = state_pacman_starting.getPacmanPosition(self.agent)

        top, right = self.walls.height - 2, self.walls.width - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))

        for corner in self.corners:
            if not state_pacman_starting.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))

        self._expanded = 0  # DO NOT CHANGE; Number of search nodes expanded

        # Please add any code here which you would like to use
        # in initializing the problem_multi_agent_tree
        "*** YOUR CODE HERE ***"

        # Hack V2
        # Dict of the _position of the corner where the key is whether or not that _position has been reached
        # self.dict_k_position_corner_v_bool_reached = {k: False for k in self.corners}
        #
        #
        # self.list_corner = self._get_list_path_consecutive_shortest()
        # self.corner_current = self._get_corner_current_new()

        # Simple set of all the corner positions
        self.set_position_corner = set(self.corners)

    # Hack v2
    # def _get_corner_current_new(self) -> Union[Tuple[int, int], None]:
    #
    #     if self.list_corner:
    #         return self.list_corner.pop()
    #     return None
    #
    # def _get_list_path_consecutive_shortest(self) -> List[Tuple[int, int]]:
    #
    #     list_corner_permutations = itertools.permutations(self.corners)
    #
    #     def get_list(iterable_position: Sequence):
    #         distance = 0
    #
    #         for i in range(len(iterable_position) - 1):
    #             distance += util.manhattanDistance(iterable_position[i], iterable_position[i + 1])
    #
    #         return distance
    #
    #     return list(reversed(min(list(list_corner_permutations), key=lambda _list: get_list(_list))))

    # Hack v2
    # def is_goal_state_all(self):
    #     return all(self.dict_k_position_corner_v_bool_reached.values())

    def getStartState(self) -> Union[HashableGoal, Tuple[int, int]]:
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """
        Return a HashableGoal object with the starting _position and a list 
        """
        return HashableGoal(self.startingPosition, [])

    def _state_modifier(self, state: HashableGoal):
        """
        Due to state being given back, this must be done to state's list_tuple_order_traveled because
        functions that receive state assume that you have traveled to state's _position.

        :param state:
        :return:
        """

        set_temp = self.set_position_corner - set(state.list_tuple_order_traveled)
        if state.position in set_temp:
            # V1
            # state.list_tuple_order_traveled[len(self.set_position_corner) - len(set_temp)] = state._position
            state.list_tuple_order_traveled.append(state.position)

    def isGoalState(self, state: HashableGoal) -> bool:
        """
        Returns whether this search state is a goal state of the problem_multi_agent_tree.
        """
        "*** YOUR CODE HERE ***"

        # util.raiseNotDefined()

        # Hack v1
        # if state in self.dict_k_position_corner_v_bool_reached:
        #
        #     if self.dict_k_position_corner_v_bool_reached[state] is False:
        #         self.dict_k_position_corner_v_bool_reached[state] = True
        #         return True
        #     else:
        #         return False
        #
        # return False
        #
        # Hack v2
        # if state == self.corner_current:
        #     if self.dict_k_position_corner_v_bool_reached[state] is False:
        #         self.dict_k_position_corner_v_bool_reached[state] = True
        #         self.corner_current = self._get_corner_current_new()
        #         return True
        #     else:
        #         return False
        # return False
        #
        #
        # return self.is_goal_state_all()

        self._state_modifier(state)

        # V1
        # Is of HashableGoal type then return it's method is_done()
        # return state.is_done()

        """
        Return True if the length of the corners that you need to travel to is equal to the size of the list 
        of corners that you traveled to.
        """
        return len(self.set_position_corner) == len(state.list_tuple_order_traveled)

    def getSuccessors(self, state: HashableGoal) -> List[Tuple[HashableGoal, Any, int]]:
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """

        successors: List[Tuple[HashableGoal, Any, int]] = []

        x: int
        y: int
        x, y = state.position

        self._state_modifier(state)

        for action in [ActionDirection.NORTH, ActionDirection.SOUTH, ActionDirection.EAST, ActionDirection.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new _position hits a wall:
            #   x,y = currentPosition
            #   dx, dy = HandlerActionDirection.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]

            "*** YOUR CODE HERE ***"

            dx: float
            dy: float
            x_next: int
            y_next: int

            dx, dy = HandlerActionDirection.get_vector_from_action_direction(action)
            x_next, y_next = int(x + dx), int(y + dy)
            bool_hit_wall: bool = self.walls[x_next][y_next]

            # Wall is True and you want valid movement so you want False
            if not bool_hit_wall:
                # Make a new HashableGoal object as a container
                hashable_goal = HashableGoal((x_next, y_next), state.list_tuple_order_traveled)

                successors.append((hashable_goal, action, 1))

        self._expanded += 1  # DO NOT CHANGE (OK BOSS)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = HandlerActionDirection.get_vector_from_action_direction(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)
