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
from queue import PriorityQueue
from typing import Iterable
from typing import List
from typing import Set
from typing import TYPE_CHECKING
from typing import Tuple
from typing import Union

from pacman import util
from pacman.agent.search_problem.common import HashableGoal
from pacman.agent.search_problem.search_problem_corners import CornersProblem

if TYPE_CHECKING:
    from pacman.game.grid import Grid


def _get_path_distance(position_initial: tuple, permutation: Iterable):
    """
    Given a path (iterable of position), find the distance for those positions starting from the state.position

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
    ** Return None if a path was not possible therefore a heuristic value cannot be calculated  
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
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners: tuple = problem.corners  # These are the position_corner_local_shortest coordinates
    walls: Grid = problem.walls  # These are the walls of the maze, as a Grid (game.py)

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
    #     Select the path with shortest distance from the loop, but return the permutation of position corners instead.
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
        Select the path with shortest distance from the loop
        Return path with shortest distance
    Notes:
        Possibly better than V5 because this will get all paths and then select the shortest one at the cost of
        memory and time because you need to calculate all permutations and do the path for each one.

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
    #     ACTUALLY LEADS TO THE DISTANCE SHORTEST FULL (Shortest path distance to all position corners).
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


###############################
