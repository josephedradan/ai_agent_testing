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
from functools import lru_cache
from typing import TYPE_CHECKING
from typing import Tuple

from pacman.agent.search import search
from pacman.agent.search_problem import FoodSearchProblem
from pacman.agent.search_problem.search_problem_position import PositionSearchProblem

if TYPE_CHECKING:
    from pacman.game.grid_pacman import GridPacman


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


def foodHeuristic(state: Tuple, problem: FoodSearchProblem) -> float:
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a GridPacman
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, list_capsule, etc., you can query the
    problem.  For example, problem.walls gives you a GridPacman of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    foodGrid: GridPacman
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
    #     path to each position corner by making your corner
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
    #     Returning the longest distance (Big Heuristic Cost) is like saying that the path you will
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
        Returning the longest distance (Big Heuristic Cost) is like saying that the path you will 
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
