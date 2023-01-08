"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/30/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
import itertools
from abc import ABC
from functools import lru_cache
from queue import PriorityQueue
from typing import Any
from typing import Hashable
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple
from typing import Union

from pacman import search
from pacman import util
from pacman.game import game
from pacman.game.actions import Actions
from pacman.game.directions import Directions
from pacman.game.gamestate import GameState
from pacman.graphics.graphics import Graphics
from pacman.graphics.graphicsDisplay import PacmanGraphicsReal


class SearchProblem(ABC):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def __init__(self):  # FIXME: THIS IS MISSING game_state
        self.graphics: Union[Graphics, None] = None

        self._expanded = None  # FIXME: NEED THIS

    def set_graphics(self, graphics: Graphics):
        self.graphics = graphics

    def getStartState(self) -> Union[Tuple[int, int], Hashable]:
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state) -> bool:
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state) -> List[Union[tuple, str, int]]:
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions) -> int:
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


class PositionSearchProblem(SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the agent_pacman_ board.

    The state space consists of (x,y) positions in a agent_pacman_ game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn=lambda x: 1, goal=(1, 1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (agent_pacman_.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        super().__init__()
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):  # TODO: COLORER
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)  # TODO: THIS SHOULD BE THE FINAL STATE ADDED BASICALLY
            # import __main__
            # if '_display' in dir(__main__):
            #     if 'drawExpandedCells' in dir(__main__._display):  # @UndefinedVariable
            #         __main__._display.drawExpandedCells(self._visitedlist)  # @UndefinedVariable

            # TODO: JOSEPH CUSTOM HERE

            if isinstance(self.graphics, PacmanGraphicsReal):
                self.graphics.drawExpandedCells(self._visitedlist)

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for display purposes
        self._expanded += 1  # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x, y))
        return cost


def _get_path_distance(position_initial: tuple, permutation: Iterable):
    """
    Given a path_file_test (iterable of position), find the distance for those positions starting from the state.position

    :param position_initial:
    :param permutation:
    :return:
    """

    distance_total_temp = 0

    position_current = position_initial

    for position_corner in permutation:
        distance_total_temp += util.manhattanDistance(position_current, position_corner)
        position_current = position_corner

    return distance_total_temp


def _get_shortest_path_from_permutation(position_initial: Tuple, set_position_remaining: set):
    """
    V4 Solution generalized

    :param position_initial:
    :param set_position_remaining:
    :return:
    """

    list_tuple_path_position_corner = list(itertools.permutations(set_position_remaining))
    distance_path_all_shortest = min([_get_path_distance(position_initial, i) for i in list_tuple_path_position_corner])
    return distance_path_all_shortest


class HashableGoal:
    # Use less memory
    __slots__ = ["position", "list_tuple_order_traveled"]

    def __init__(self, position: Tuple[int, ...], list_tuple_order_traveled: List[Union[Tuple[int, ...], None]]):
        """
        Probably because all of the algorithms inside of search.py prevent you from moving into a position that you
        already traversed, you can use an additional parameter to act similar to changing universes once you have
        reached a goal.

        Basically, you hash the position along side the length of the set that contains the goal positions.
        When you reach a goal position, the set's length is changed because you remove that position from that set.
        The removal of a goal position and the creation of the set is done before the creation of this object based
        on the previous HashableGoal object's list_tuple_order_traveled.

        """

        self.position = position
        self.list_tuple_order_traveled = list_tuple_order_traveled.copy()

    def __hash__(self):
        """
        Hash the position along side the length of the set of goal positions that you haven't reached

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

             tuple (Just adding the position of a corner in a list of corners visited, then hashing
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


class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, agent_pacman_'s starting position and corners.
        """
        super().__init__()
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()

        top, right = self.walls.height - 2, self.walls.width - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))

        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))

        self._expanded = 0  # DO NOT CHANGE; Number of search nodes expanded

        # Please add any code here which you would like to use
        # in initializing the problem
        "*** YOUR CODE HERE ***"

        # Hack V2
        # Dict of the position of the corner where the key is whether or not that position has been reached
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
        Return a HashableGoal object with the starting position and a list 
        """
        return HashableGoal(self.startingPosition, [])

    def _state_modifier(self, state: HashableGoal):
        """
        Due to state being given back, this must be done to state's list_tuple_order_traveled because
        functions that receive state assume that you have traveled to state's position.

        :param state:
        :return:
        """

        set_temp = self.set_position_corner - set(state.list_tuple_order_traveled)
        if state.position in set_temp:
            # V1
            # state.list_tuple_order_traveled[len(self.set_position_corner) - len(set_temp)] = state.position
            state.list_tuple_order_traveled.append(state.position)

    def isGoalState(self, state: HashableGoal) -> bool:
        """
        Returns whether this search state is a goal state of the problem.
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

        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]

            "*** YOUR CODE HERE ***"

            dx: float
            dy: float
            x_next: int
            y_next: int

            dx, dy = Actions.directionToVector(action)
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
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def _euclidean_distance(xy1, xy2):
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


def _get_heuristic_cost_ucs_crude(grid_wall: List[List],
                                  position_start: tuple,
                                  position_goal: tuple,
                                  cost_min_current: Union[int, None]) -> Union[int, None]:
    """
    Simple implementation of Uniform cost search that mimics what is in the search.py

    IMPORTANT NOTE:
        DO NOT USE cost_min_current WHEN YOU ARE USING max() INSTEAD OF mid() BECAUSE YOU WILL CUT OFF SOLUTIONS!
        cost_min_current HELPS WITH CALCULATING LENGTHS TO A GOAL FASTER.

        *THIS ALGORITHM CAN LEAD TO "Heuristic resulted in expansion of 1495 nodes" IN V6 OF THE 6th Problem.
        IT MEANING AT THIS ALGO DOES WORK, BUT IT'S SLOW.

    :param grid_wall:
    :param position_start: Starting position tuple
    :param position_goal: Goal position tuple
    :param cost_min_current: Current smallest cost obtained from another call to _get_heuristic_cost_ucs_crude,
        It is used to prevent this algorithm from calculating lengths to a goal that are longer than cost_min_current.
        Basically, this value is used to decrease computation time ONLY FOR FINDING THE SHORTEST DISTANCE.

    :return:
    """
    queue = PriorityQueue()

    # Simple data container
    position_with_cost_first = (0, position_start)

    # Add the first Simple data container to the queue
    queue.put(position_with_cost_first)

    set_visited: Set[Tuple] = set()

    while not queue.empty():

        position_with_cost = queue.get()

        # Prevent walking back
        if position_with_cost[1] in set_visited:
            continue

        set_visited.add(position_with_cost[1])

        # Prevent calculating a route that is too long
        if cost_min_current is not None:
            if position_with_cost[0] > cost_min_current:
                continue

        # Return cost if this algo has reached its goal position
        if position_with_cost[1] == position_goal:
            return position_with_cost[0]

        # Standard loop over directions to be used to indicate movement
        for tuple_move in ((0, 1), (1, 0), (0, -1), (-1, 0)):

            position_new = (position_with_cost[1][0] + tuple_move[0], position_with_cost[1][1] + tuple_move[1])

            # If wall in the way, then skip
            if grid_wall[position_new[0]][position_new[1]] is True:
                continue

            cost = position_with_cost[0] + 1
            # cost_heuristic = util.manhattanDistance(position_new, position_goal)

            # New simple data container
            position_with_cost_new = (cost, position_new)

            queue.put(position_with_cost_new)

    """
    ** Return None if a path_file_test was not possible therefore a heuristic value cannot be calculated  
    If you return 0 then you will be lying, In reality, you need to return infinity
    """
    return None


def _get_shortest_path_using_ucs_crude(position_initial: Tuple,
                                       set_position_remaining: set,
                                       grid_wall: List[List]):
    """
    V7 Solution generalized

    Uses _get_shortest_path_using_immediate as a base (V5) and
    uses V6's _get_heuristic_cost_ucs_crude to find the distance.

    Notes:
        Obviously, this function looks very similar to _get_shortest_path_using_immediate and can be compressed into
        one function. The cost is that the new function will look ugly plus _get_shortest_path_using_immediate does
        not rely on grid_wall.

    :param position_initial: Initial position
    :param set_position_remaining: Rest of the positions to travel to
    :return:
    """

    distance_path_all_shortest = None
    position_current = position_initial

    # While positions to go to is not empty
    while set_position_remaining:

        distance_path_local_shortest = None
        position_corner_local_shortest = None

        # Loop through positions to go to to find the immediate distance_path_local_shortest
        for position_corner_temp in set_position_remaining:

            distance_local_shortest_temp: Union[int, None] = _get_heuristic_cost_ucs_crude(grid_wall,
                                                                                           position_current,
                                                                                           position_corner_temp,
                                                                                           distance_path_local_shortest)

            # Disallow distance_local_shortest_temp when None is given  (None is equivalent to infinity)
            if distance_local_shortest_temp is not None:
                # Select a position_corner_local_shortest based on distance_path_local_shortest
                if distance_path_local_shortest is None:
                    distance_path_local_shortest = distance_local_shortest_temp
                    position_corner_local_shortest = position_corner_temp
                elif distance_local_shortest_temp < distance_path_local_shortest:
                    distance_path_local_shortest = distance_local_shortest_temp
                    position_corner_local_shortest = position_corner_temp

        # Remove position_corner_local_shortest based on distance_path_local_shortest
        set_position_remaining.remove(position_corner_local_shortest)

        """
        Add distance_path_local_shortest from position_current into the distance_path_all_shortest and 
        replace position_current
        """
        if distance_path_all_shortest is None:
            distance_path_all_shortest = distance_path_local_shortest
            position_current = position_corner_local_shortest
        else:
            distance_path_all_shortest += distance_path_local_shortest
            position_current = position_corner_local_shortest

    return distance_path_all_shortest if distance_path_all_shortest is not None else 0


def _get_shortest_path_using_immediate(position_initial: Tuple,
                                       set_position_remaining: set):
    """
    V5 Solution generalized

    :param position_initial: Initial position
    :param set_position_remaining: Rest of the positions to travel to
    :return:
    """

    distance_path_all_shortest = None
    position_current = position_initial

    # While positions to go to is not empty
    while set_position_remaining:

        distance_path_local_shortest = None
        position_corner_local_shortest = None

        # Loop through positions to go to to find the immediate distance_path_local_shortest
        for position_corner_temp in set_position_remaining:
            distance_local_shortest_temp = util.manhattanDistance(position_current, position_corner_temp)

            # Select a position_corner_local_shortest based on distance_path_local_shortest
            if distance_path_local_shortest is None:
                distance_path_local_shortest = distance_local_shortest_temp
                position_corner_local_shortest = position_corner_temp
            elif distance_local_shortest_temp < distance_path_local_shortest:
                distance_path_local_shortest = distance_local_shortest_temp
                position_corner_local_shortest = position_corner_temp

        # Remove position_corner_local_shortest based on distance_path_local_shortest
        set_position_remaining.remove(position_corner_local_shortest)

        """
        Add distance_path_local_shortest from position_current into the distance_path_all_shortest and 
        replace position_current
        """
        if distance_path_all_shortest is None:
            distance_path_all_shortest = distance_path_local_shortest
            position_current = position_corner_local_shortest
        else:
            distance_path_all_shortest += distance_path_local_shortest
            position_current = position_corner_local_shortest

    return distance_path_all_shortest if distance_path_all_shortest is not None else 0


def cornersHeuristic(state: HashableGoal, problem: CornersProblem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path_file_test from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners: tuple = problem.corners  # These are the position_corner_local_shortest coordinates
    walls: game.Grid = problem.walls  # These are the walls of the maze, as a Grid (game.py)

    "*** YOUR CODE HERE ***"

    # print(walls.data)

    set_position_corner_remaining = set(corners) - set(state.list_tuple_order_traveled)

    # Use for V2
    dict_k_corner_v_distance_manhattan = {}

    # Use for V1
    distance_total = 0

    for position_corner_local_shortest in set_position_corner_remaining:
        result_manhattan = util.manhattanDistance(state.position, position_corner_local_shortest)
        result_euclidean = _euclidean_distance(state.position, position_corner_local_shortest)
        dict_k_corner_v_distance_manhattan[position_corner_local_shortest] = result_manhattan

        # Use for V1
        distance_total += result_manhattan

    ####################
    # """
    # V1: Sum of all Manhattan Distances
    #
    # Points: 0
    # Notes:
    #     Because of 4 corners, the distance_total will be the same until agent_pacman_ gets one of the corners
    # Result:
    #     *** FAIL: Inadmissible heuristic
    #     *** FAIL: Inadmissible heuristic
    #     *** FAIL: inconsistent heuristic
    #     *** PASS: Heuristic resulted in expansion of 505 nodes  # 890 nodes for euclidean
    # """
    # print("{:<10}{}".format(string_given(distance_total), string_given(dict_k_corner_v_distance_manhattan)))
    # return distance_total

    #####

    #####
    # """
    # V2: Select Min Manhattan Distance from Current position to Corner position
    # Points: 1/3
    # Result:
    #     *** PASS: heuristic value less than true cost at start state
    #     *** PASS: heuristic value less than true cost at start state
    #     *** PASS: heuristic value less than true cost at start state
    #     *** FAIL: Heuristic resulted in expansion of 1760 nodes
    # """
    #
    # distance_position_corner_closest = min(set_position_corner_remaining,
    #                               key=lambda position_corner_given: util.manhattanDistance(state.position,
    #                                                                                        position_corner_given))
    #
    # # print(dict_k_corner_v_distance_manhattan.get(distance_position_corner_closest))
    # return dict_k_corner_v_distance_manhattan.get(distance_position_corner_closest)

    #####

    #####
    # """
    # V3:
    #     Get all permutations traveling to all corners
    #     For all permutations:
    #         Get the manhattan distance starting from state.position traveling in the order of position corners
    #         inside of the the permutation
    #     Select the path_file_test with shortest distance from the loop, but return the permutation of position corners instead.
    #     Return the distance of the 0th index position corner in the permutation
    #
    #
    # Points: 1/3
    # Result:
    #     *** PASS: heuristic value less than true cost at start state
    #     *** PASS: heuristic value less than true cost at start state
    #     *** PASS: heuristic value less than true cost at start state
    #     *** FAIL: Heuristic resulted in expansion of 1743 nodes
    # """
    #
    # list_tuple_path_position_corner = list(itertools.permutations(set_position_corner_remaining))
    #
    # path_position_corner_shortest = min(list_tuple_path_position_corner,
    #                                     key=lambda tuple_path_position_corner: _get_path_distance(
    #                                         state.position,
    #                                         tuple_path_position_corner)
    #                                     )
    #
    # # print("{:<30}{}".format(string_given(state.position),string_given(path_position_corner_shortest)))
    # distance_position_corner_must_go_to = util.manhattanDistance(state.position, path_position_corner_shortest[0])
    #
    # return distance_position_corner_must_go_to

    #####
    """
    V4:
        Get all permutations traveling to all corners
        For all permutations:
            Get the manhattan distance starting from state.position traveling in the order of position corners
            inside of the the permutation
        Select the path_file_test with shortest distance from the loop
        Return path_file_test with shortest distance
    Notes:
        Possibly better than V5 because this will get all paths and then select the shortest one at the cost of
        memory and time because you need to calculate all permutations and do the path_file_test for each one.

    IMPORTANT NOTES:
        ONLY USE FOR SMALL GRIDS OR PERMUTATIONS WILL TAKE FOREVER.

    Points: 3/3
    Result:
        *** PASS: heuristic value less than true cost at start state
        *** PASS: heuristic value less than true cost at start state
        *** PASS: heuristic value less than true cost at start state
        *** PASS: Heuristic resulted in expansion of 954 nodes

    """

    return _get_shortest_path_from_permutation(state.position, set_position_corner_remaining)

    #####
    # """
    # V5:
    #     Assign distance total to 0
    #     Assign position current to state.position
    #     For each position corner in set position corner remaining
    #         Get the Manhattan Distance from position current to position corner
    #     Select the distance shortest from position current to position corner
    #     Add distance shortest to distance total
    #     Assign position current to the position corner with the distance shortest
    #     Remove position current to the position corner with the distance shortest from set position corner remaining
    #     Repeat until no more position corner in from set position corner remaining
    #     Return distance corner
    #
    # IMPORTANT NOTES:
    #     YOU ARE GETTING THE IMMEDIATE DISTANCE SHORTEST AND IT'S POSITION CORNER TO EACH POSITION CORNER FROM YOUR
    #     POSITION CURRENT. THIS IS DIFFERENT FROM V4 BECAUSE YOU DON'T KNOW THAT YOUR IMMEDIATE DISTANCE SHORTEST
    #     ACTUALLY LEADS TO THE DISTANCE SHORTEST FULL (Shortest path_file_test distance to all position corners).
    #
    #     V4 DOES DISTANCE SHORTEST FULL, V5 IS JUST YOLO SELECT THE DISTANCE SHORTEST TO MAKE THE DISTANCE SHORTEST
    #     FULL VIA CALCULATING ALL POSSIBLE PERMUTATIONS OF PATHS AND THEIR DISTANCE SHORTEST FULL.
    #
    # Points: 3/3
    # Result:
    #     *** PASS: heuristic value less than true cost at start state
    #     *** PASS: heuristic value less than true cost at start state
    #     *** PASS: heuristic value less than true cost at start state
    #     *** PASS: Heuristic resulted in expansion of 905 nodes
    # """
    # return _get_shortest_path_using_immediate(state.position, set_position_corner_remaining)

    #####
    # """
    # V6
    #     Uniform Cost Search based on the walls grid to find the exact distance to each position corner
    #     Return the shortest distance to a position corner
    # Points: 2/3
    # Result:
    #     *** PASS: heuristic value less than true cost at start state
    #     *** PASS: heuristic value less than true cost at start state
    #     *** PASS: heuristic value less than true cost at start state
    #     *** FAIL: Heuristic resulted in expansion of 1495 nodes
    # """
    #
    # list_distance = []
    #
    # cost_heuristic_min_current = None
    #
    # # a = time.time()
    # for position_corner_local_shortest in set_position_corner_remaining:
    #     result_ucs: Union[int, None] = _get_heuristic_cost_ucs_crude(walls.data,
    #                                                                  state.position,
    #                                                                  position_corner_local_shortest,
    #                                                                  cost_heuristic_min_current)
    #
    #     # Disallow result_ucs where when None is given (None is equivalent to infinity)
    #     if result_ucs is not None:
    #         if cost_heuristic_min_current is None:
    #             cost_heuristic_min_current = result_ucs
    #         elif result_ucs < cost_heuristic_min_current:
    #             cost_heuristic_min_current = result_ucs
    #         list_distance.append(result_ucs)
    #
    # # b = time.time()
    #
    # # Append more solutions (Because they are not normalized, adding these is a bad idea)
    # # list_distance.extend(dict_k_corner_v_distance_manhattan.values())  # expansion of 1760 nodes
    # # list_distance.append(distance_total)  # expansion of 1513 nodes
    #
    # distance_min = min(list_distance) if list_distance else 0
    #
    # # # print("TIME:", b - a)
    # # print("Remaining Corners:", set_position_corner_remaining)
    # # print("Position Current:", state.position)
    # # print("Cost:", cost_heuristic_min_current)
    # # print("List Distances:", list_distance)
    # # # print(walls)
    # # print()
    #
    # return distance_min

    #####
    # """
    # V7
    #     Uniform Cost Search based on the walls grid to find the exact distance to a position corner and then
    #     find it's distance to another position corner and so on...
    #     Basically do V4 or V5 but using a UCS (V6) instead of Manhattan distance.
    #
    #     Probably use V5 because V4 takes to long if there are too many position corners (making a lot of permutations)
    # Results:
    #     *** PASS: heuristic value less than true cost at start state
    #     *** PASS: heuristic value less than true cost at start state
    #     *** FAIL: inconsistent heuristic
    #     *** PASS: Heuristic resulted in expansion of 131 nodes
    # """
    #
    # return _get_shortest_path_using_ucs_crude(state.position, set_position_corner_remaining, walls.data)

    #####


############


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path_file_test to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState: GameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        super().__init__(gameState)
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x, y = state

        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        self.food: game.Grid
        self.walls: game.Grid

        # Note that self.food is the same a foodGrid from problem 7 and foodGrid CHANGES OVER (foodHeuristic)
        list_position_food_remaining = self.food.asList()

        ####################
        """
        Recall that list_position_food_remaining changes so just check if the state, which is a tuple of the position,
        is in the list_position_food_remaining.

        """

        return state in list_position_food_remaining


@lru_cache(maxsize=None)  # Cache repeated inputs
def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))


###############################


class FoodSearchProblem:
    """
    A search problem associated with finding the a path_file_test that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """

    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0  # DO NOT CHANGE
        self.heuristicInfo = {}  # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1  # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append((((nextx, nexty), nextFood), direction, 1))
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x, y = self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost


def foodHeuristic(state: Tuple, problem: FoodSearchProblem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    foodGrid: game.Grid
    position: tuple

    position, foodGrid = state
    "*** YOUR CODE HERE ***"

    position_start = position

    # List of food remaining on the grid
    list_position_food_remaining = foodGrid.asList()

    # All food remaining on the grid (foodGrid.asList() CHANGES IF YOU GOT A FOOD ALREADY)
    set_position_food_location = set(foodGrid.asList())

    ###
    # THE COMMENTED OUT BELOW IS NOT NECESSARY ANYMORE
    # if problem.heuristicInfo.get("set_position_food_location_visited") is None:
    #     set_position_food_location_temp = set()
    #     problem.heuristicInfo["set_position_food_location_visited"] = set_position_food_location_temp
    #
    # # Set of visited food
    # set_position_food_location_visited = problem.heuristicInfo.get("set_position_food_location_visited")
    #
    # """
    # Set of remaining food
    #
    # IMPORTANT NOTES:
    #     state is not a HashableGoal but a tuple, therefore it is not possible to transfer information about where
    #     the agent_pacman_ has legitimately traveled to.
    #
    # """
    # set_position_food_location_remaining = set_position_food_location - set_position_food_location_visited
    ###

    set_position_food_location_remaining = set_position_food_location

    ####################
    # r"""
    # V1
    #     Solve problem using V4 or V5 from the previous problem (Problem 6) which were to do the full
    #     path_file_test to each position corner by making your corner
    #
    # Notes:
    #     Both V4 and V5 from Problem 6 have problems here...
    #
    # IMPORTANT NOTES:
    #     V5 SHOULD HAV
    # Result:
    #     _get_shortest_path_using_immediate  # V5 solution from problem 6
    #         Notes:
    #             On case 15 it needs to go (down, up, up, uo, uo) not (up, down, up, up, up) which is longer
    #
    #         Result:
    #             *** PASS: test_cases\q7\food_heuristic_1.test
    #             *** PASS: test_cases\q7\food_heuristic_10.test
    #             *** PASS: test_cases\q7\food_heuristic_11.test
    #             *** PASS: test_cases\q7\food_heuristic_12.test
    #             *** PASS: test_cases\q7\food_heuristic_13.test
    #             *** PASS: test_cases\q7\food_heuristic_14.test
    #             *** FAIL: test_cases\q7\food_heuristic_15.test
    #             *** Heuristic failed admissibility test
    #             *** Tests failed.
    #
    #     _get_shortest_path_from_permutation  # V4 solution from problem 6
    #         Notes:
    #             TOO MUCH FOOD LOCATIONS -> TOO MANY PERMUTATIONS
    #
    #         Result:
    #             *** PASS: test_cases\q7\food_heuristic_1.test
    #             *** PASS: test_cases\q7\food_heuristic_10.test
    #             *** PASS: test_cases\q7\food_heuristic_11.test
    #             *** PASS: test_cases\q7\food_heuristic_12.test
    #             *** PASS: test_cases\q7\food_heuristic_13.test
    # """
    #
    # if position_start in set_position_food_location_remaining:
    #     set_position_food_location_remaining.add(position_start)
    #
    # # Can't solve test 15 (Failed admissibility test)
    # # distance = _get_shortest_path_using_immediate(position_start, set_position_food_location_remaining)
    #
    # # Can't Solve test 14 (Too many permutations, load time takes to long (Probably))
    # distance = _get_shortest_path_from_permutation(position_start, set_position_food_location_remaining)
    #
    # print(problem.walls)
    # print("Food:", foodGrid.asList())
    # print("Position Current:", position_start)
    # print("Heuristic Cost:", distance)
    # print()
    #
    # return distance

    #####
    # r"""
    # V2
    #     Solve the problem using the idea from V6 of problem 6 which used UCS to get the heuristic cost.
    #
    # Result:
    #     *** PASS: test_cases\q7\food_heuristic_1.test
    #     *** PASS: test_cases\q7\food_heuristic_10.test
    #     *** PASS: test_cases\q7\food_heuristic_11.test
    #     *** PASS: test_cases\q7\food_heuristic_12.test
    #     *** PASS: test_cases\q7\food_heuristic_13.test
    #     *** PASS: test_cases\q7\food_heuristic_14.test
    #     *** FAIL: test_cases\q7\food_heuristic_15.test
    #     *** Heuristic failed admissibility test
    #     *** Tests failed.
    # """
    #
    # distance_shortest = _get_shortest_path_using_ucs_crude(position_start,
    #                                                        set_position_food_location_remaining,
    #                                                        problem.walls)
    #
    # return distance_shortest

    #####
    # r"""
    # V3
    #     Use a modified version of V6 from the previous problem (Problem 6)
    #         "Uniform Cost Search based on the walls grid to find the exact distance to each position corner
    #         Return the shortest distance to a position corner"
    #     The modification is to support both min() and max() distance selection.
    #
    # Notes:
    #     This algorithm takes time to calculate.
    #
    #     In _get_heuristic_cost_ucs_crude the 4th parameter needs to be None because that parameter is used reduce
    #     computation time for finding the shortest distance.
    #
    #     Code can be one lined, but it would look ugly.
    #
    # IMPORTANT NOTES:
    #     Using the max distance instead of min distance is essentially equivalent to returning the longest distance
    #     for the priority queue algorithm to then select the best of the (Big Heuristic Cost + Node Cost distance).
    #     Returning the longest distance (Big Heuristic Cost) is like saying that the path_file_test you will
    #     make to that node is the worst. For the Priority queue, it will select the shortest of the longest
    #     distance sums (Node Cost + Heuristic Cost). The series of big Heuristic Costs in the PQ will give you a
    #     solution that expands the least amount of nodes. Longer distances are more influential than short
    #     distances meaning Heuristic Cost > Node Cost most of the time so the PQ will select mainly based
    #     on Heuristic Cost.
    #
    #     If you were to use min then you would select the shortest distance to a node and so
    #     Heuristic Cost < Node Cost most of the time for the priority queue. So the PQ would be mostly
    #     selecting based on Node Cost which is close to/is a pure BFS or UCS depending on implementation.
    #
    # Result:
    #     Using min()
    #         *** PASS: test_cases\q7\food_heuristic_1.test
    #         *** PASS: test_cases\q7\food_heuristic_10.test
    #         *** PASS: test_cases\q7\food_heuristic_11.test
    #         *** PASS: test_cases\q7\food_heuristic_12.test
    #         *** PASS: test_cases\q7\food_heuristic_13.test
    #         *** PASS: test_cases\q7\food_heuristic_14.test
    #         *** PASS: test_cases\q7\food_heuristic_15.test
    #         *** PASS: test_cases\q7\food_heuristic_16.test
    #         *** PASS: test_cases\q7\food_heuristic_17.test
    #         *** PASS: test_cases\q7\food_heuristic_2.test
    #         *** PASS: test_cases\q7\food_heuristic_3.test
    #         *** PASS: test_cases\q7\food_heuristic_4.test
    #         *** PASS: test_cases\q7\food_heuristic_5.test
    #         *** PASS: test_cases\q7\food_heuristic_6.test
    #         *** PASS: test_cases\q7\food_heuristic_7.test
    #         *** PASS: test_cases\q7\food_heuristic_8.test
    #         *** PASS: test_cases\q7\food_heuristic_9.test
    #         *** FAIL: test_cases\q7\food_heuristic_grade_tricky.test
    #         *** 	expanded nodes: 12372
    #         *** 	thresholds: [15000, 12000, 9000, 7000]
    #
    #     Using max()
    #         *** PASS: test_cases\q7\food_heuristic_1.test
    #         *** PASS: test_cases\q7\food_heuristic_10.test
    #         *** PASS: test_cases\q7\food_heuristic_11.test
    #         *** PASS: test_cases\q7\food_heuristic_12.test
    #         *** PASS: test_cases\q7\food_heuristic_13.test
    #         *** PASS: test_cases\q7\food_heuristic_14.test
    #         *** PASS: test_cases\q7\food_heuristic_15.test
    #         *** PASS: test_cases\q7\food_heuristic_16.test
    #         *** PASS: test_cases\q7\food_heuristic_17.test
    #         *** PASS: test_cases\q7\food_heuristic_2.test
    #         *** PASS: test_cases\q7\food_heuristic_3.test
    #         *** PASS: test_cases\q7\food_heuristic_4.test
    #         *** PASS: test_cases\q7\food_heuristic_5.test
    #         *** PASS: test_cases\q7\food_heuristic_6.test
    #         *** PASS: test_cases\q7\food_heuristic_7.test
    #         *** PASS: test_cases\q7\food_heuristic_8.test
    #         *** PASS: test_cases\q7\food_heuristic_9.test
    #         *** PASS: test_cases\q7\food_heuristic_grade_tricky.test
    #         *** 	expanded nodes: 4137
    #         *** 	thresholds: [15000, 12000, 9000, 7000]
    # """
    # list_distance = []
    #
    # for position_corner_local_shortest in list_position_food_remaining:
    #     result_ucs: Union[int, None] = _get_heuristic_cost_ucs_crude(problem.startingGameState.getWalls(),
    #                                                                  position_start,
    #                                                                  position_corner_local_shortest,
    #                                                                  None)
    #
    #     # Disallow result_ucs where when None is given (None is equivalent to infinity)
    #     if result_ucs is not None:
    #         list_distance.append(result_ucs)
    #
    # distance_delta = max(list_distance) if list_distance else 0
    # return distance_delta

    #####
    r"""
    V4
        Use the mazeDistance at the bottom of this file which is literally doing V3 of this 
        problem but better, but this time you have gameState because it's an instance variable WITHIN the 
        object which is required for mazeDistance.

    Notes:
        I Selected V4 because mazeDistance can be CACHED so the problem can be solved fast.

    IMPORTANT NOTES:

        This is the same important note from V3:

        "Using the max distance instead of min distance is essentially equivalent to returning the longest distance
        for the priority queue algorithm to then select the best of the (Big Heuristic Cost + Node Cost distance). 
        Returning the longest distance (Big Heuristic Cost) is like saying that the path_file_test you will 
        make to that node is the worst. For the Priority queue, it will select the shortest of the longest 
        distance sums (Node Cost + Heuristic Cost). The series of big Heuristic Costs in the PQ will give you a 
        solution that expands the least amount of nodes. Longer distances are more influential than short 
        distances meaning Heuristic Cost > Node Cost most of the time so the PQ will select mainly based
        on Heuristic Cost.

        If you were to use min then you would select the shortest distance to a node and so 
        Heuristic Cost < Node Cost most of the time for the priority queue. So the PQ would be mostly 
        selecting based on Node Cost which is close to/is a pure BFS or UCS depending on implementation."

    Result:
        Using min()
            *** PASS: test_cases\q7\food_heuristic_1.test
            *** PASS: test_cases\q7\food_heuristic_10.test
            *** PASS: test_cases\q7\food_heuristic_11.test
            *** PASS: test_cases\q7\food_heuristic_12.test
            *** PASS: test_cases\q7\food_heuristic_13.test
            *** PASS: test_cases\q7\food_heuristic_14.test
            *** PASS: test_cases\q7\food_heuristic_15.test
            *** PASS: test_cases\q7\food_heuristic_16.test
            *** PASS: test_cases\q7\food_heuristic_17.test
            *** PASS: test_cases\q7\food_heuristic_2.test
            *** PASS: test_cases\q7\food_heuristic_3.test
            *** PASS: test_cases\q7\food_heuristic_4.test
            *** PASS: test_cases\q7\food_heuristic_5.test
            *** PASS: test_cases\q7\food_heuristic_6.test
            *** PASS: test_cases\q7\food_heuristic_7.test
            *** PASS: test_cases\q7\food_heuristic_8.test
            *** PASS: test_cases\q7\food_heuristic_9.test
            *** FAIL: test_cases\q7\food_heuristic_grade_tricky.test
            *** 	expanded nodes: 12372
            *** 	thresholds: [15000, 12000, 9000, 7000]

        Using max()
            *** PASS: test_cases\q7\food_heuristic_1.test
            *** PASS: test_cases\q7\food_heuristic_10.test
            *** PASS: test_cases\q7\food_heuristic_11.test
            *** PASS: test_cases\q7\food_heuristic_12.test
            *** PASS: test_cases\q7\food_heuristic_13.test
            *** PASS: test_cases\q7\food_heuristic_14.test
            *** PASS: test_cases\q7\food_heuristic_15.test
            *** PASS: test_cases\q7\food_heuristic_16.test
            *** PASS: test_cases\q7\food_heuristic_17.test
            *** PASS: test_cases\q7\food_heuristic_2.test
            *** PASS: test_cases\q7\food_heuristic_3.test
            *** PASS: test_cases\q7\food_heuristic_4.test
            *** PASS: test_cases\q7\food_heuristic_5.test
            *** PASS: test_cases\q7\food_heuristic_6.test
            *** PASS: test_cases\q7\food_heuristic_7.test
            *** PASS: test_cases\q7\food_heuristic_8.test
            *** PASS: test_cases\q7\food_heuristic_9.test
            *** PASS: test_cases\q7\food_heuristic_grade_tricky.test
            *** 	expanded nodes: 4137
            *** 	thresholds: [15000, 12000, 9000, 7000]
    """

    list_distance = [mazeDistance(position_start,
                                  position_corner_temp,
                                  problem.startingGameState) for
                     position_corner_temp in
                     list_position_food_remaining]

    distance_shortest = max(list_distance) if list_distance else 0

    return distance_shortest

    #####
