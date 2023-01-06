"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/3/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""


# Cache inputs to prevent repeat calculations
from functools import lru_cache
from queue import PriorityQueue
from typing import Set
from typing import Tuple
from typing import Union

from multiagent.agent.evaluation_function.evaluation_function_food_and_ghost import \
    evaluation_function_food_and_ghost_helper
from multiagent.game.directions import Action
from multiagent.game.gamestate import GameState
from multiagent.game.grid import Grid


@lru_cache(maxsize=None)
def _get_heuristic_cost_ucs_crude(grid_wall: Grid,
                                  position_start: tuple,
                                  position_goal: tuple,
                                  cost_min_current: Union[int, None]) -> Union[int, None]:
    """
    Simple implementation of Uniform cost search that mimics what is in the search.py

    Notes:
        If no cost_min_current given, then it's a BFS

    :param grid_wall:
    :param position_start: Starting position tuple
    :param position_goal: Goal position tuple
    :param cost_min_current: Current smallest cost obtained from another call to _get_heuristic_cost_ucs_crude,
        It is used to prevent this algorithm from calculating lengths to a goal that are longer than cost_min_current.
        Basically, this value is used to decrease computation time ONLY FOR FINDING THE SHORTEST DISTANCE.

    :return:
    """
    # print(position_goal, position_start)

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

            # New simple data container
            position_with_cost_new = (cost, position_new)

            queue.put(position_with_cost_new)

    """
    ** Return None if a path was not possible therefore a heuristic value cannot be calculated  
    If you return 0 then you will be lying, In reality, you need to return infinity
    """
    return 0  # Return 0 to imply no path


def evaluation_function_better(currentGameState: GameState, action: Action) -> float:
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (name_question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    """
    Run:
        Testing:
            python autograder.py -q q5
            python autograder.py -q q5 --no-graphics 
            py -3.6 autograder.py -q q5 --no-graphics  # Use this one

        Actual:
            python autograder.py -q q5
            python autograder.py -q q5 --no-graphics  

            py -3.6 autograder.py -q q5
            py -3.6 autograder.py -q q5 --no-graphics  # Use this one
    """

    game_state_successor_pacman: GameState = currentGameState

    # position_pacman_new: Tuple[int, int] = game_state_successor_pacman.getPacmanPosition()
    # position_food_new: Grid = game_state_successor_pacman.getFood()
    #
    # list_agent_state_ghost_new: List[AgentState] = game_state_successor_pacman.getGhostStates()
    # list_agent_state_ghost_scared_time: List[float] = [ghostState.scaredTimer for ghostState in
    #                                                    list_agent_state_ghost_new]

    # print("game_state_current", type(game_state_current), game_state_current)
    #
    # print("game_state_successor_pacman",
    #       type(game_state_successor_pacman),
    #       game_state_successor_pacman)
    #
    # print("position_pacman_new (Pacman new pos after movement)",
    #       type(position_pacman_new),
    #       position_pacman_new)
    #
    # print("position_food_new",
    #       type(position_food_new),
    #       position_food_new)
    #
    # print("list_agent_state_ghost_new",
    #       type(list_agent_state_ghost_new),
    #       list_agent_state_ghost_new)
    #
    # print("list_agent_state_ghost_scared_time",
    #       type(list_agent_state_ghost_scared_time),
    #       list_agent_state_ghost_scared_time)
    #
    # print("game_state_successor_pacman.getScore()",
    #       type(game_state_successor_pacman.getScore()),
    #       game_state_successor_pacman.getScore())
    #
    # print("game_state_successor_pacman.getPacmanState()",
    #       type(game_state_successor_pacman.getPacmanState()),
    #       game_state_successor_pacman.getPacmanState())
    #
    # print("#" * 100)

    ####################

    # util.raiseNotDefined()

    # r"""
    # V1
    #     Evaluation function from Q1 using Manhattan distance
    #
    # Result:
    #     py -3.6 autograder.py -q q5 --no-graphics
    #         Question
    #         q5
    #         == == == == == =
    #
    #         Pacman emerges victorious! Score: 1162
    #         Pacman emerges victorious! Score: 1330
    #         Pacman emerges victorious! Score: 1343
    #         Pacman emerges victorious! Score: 1253
    #         Pacman emerges victorious! Score: 1137
    #         Pacman emerges victorious! Score: 1173
    #         Pacman emerges victorious! Score: 1159
    #         Pacman emerges victorious! Score: 1158
    #         Pacman emerges victorious! Score: 1344
    #         Pacman emerges victorious! Score: 1367
    #         Average Score: 1242.6
    #         Scores:        1162.0, 1330.0, 1343.0, 1253.0, 1137.0, 1173.0, 1159.0, 1158.0, 1344.0, 1367.0
    #         Win Rate:      10/10 (1.00)
    #         Record:        Win, Win, Win, Win, Win, Win, Win, Win, Win, Win
    #         *** PASS: test_cases\q5\grade-agent.test (6 of 6 points)
    #         ***     1242.6 average score (2 of 2 points)
    #         ***         Grading scheme:
    #         ***          < 500:  0 points
    #         ***         >= 500:  1 points
    #         ***         >= 1000:  2 points
    #         ***     10 games not timed out (1 of 1 points)
    #         ***         Grading scheme:
    #         ***          < 0:  fail
    #         ***         >= 0:  0 points
    #         ***         >= 10:  1 points
    #         ***     10 wins (3 of 3 points)
    #         ***         Grading scheme:
    #         ***          < 1:  fail
    #         ***         >= 1:  1 points
    #         ***         >= 5:  2 points
    #         ***         >= 10:  3 points
    #
    #         ### Question q5: 6/6 ###
    #
    #
    #         Finished at 11:37:45
    #
    #         Provisional grader
    #         ==================
    #         Question q5: 6/6
    #         ------------------
    #         Total: 6/6
    # """
    #
    # result = evaluation_function_food_and_ghost(game_state_successor_pacman)
    #
    # return result

    ##########

    r"""
    V2
        Evaluation function from Q1 using heuristic_cost_ucs_crude from assignment 1

    Notes:
        it's actually a BFS not UCS because None is given to _get_heuristic_cost_ucs_crude

    Results:
        py -3.6 autograder.py -q q5 --no-graphics
            Question q5
            ===========

            Pacman emerges victorious! Score: 1367
            Pacman emerges victorious! Score: 1365
            Pacman emerges victorious! Score: 1368
            Pacman emerges victorious! Score: 1167
            AgentPacman emerges victorious! Score: 1171
            AgentPacman emerges victorious! Score: 1356
            AgentPacman emerges victorious! Score: 1361
            AgentPacman emerges victorious! Score: 1141
            AgentPacman emerges victorious! Score: 1366
            AgentPacman emerges victorious! Score: 1164
            Average Score: 1282.6
            Scores:        1367.0, 1365.0, 1368.0, 1167.0, 1171.0, 1356.0, 1361.0, 1141.0, 1366.0, 1164.0
            Win Rate:      10/10 (1.00)
            Record:        Win, Win, Win, Win, Win, Win, Win, Win, Win, Win
            *** PASS: test_cases\q5\grade-agent.test (6 of 6 points)
            ***     1282.6 average score (2 of 2 points)
            ***         Grading scheme:
            ***          < 500:  0 points
            ***         >= 500:  1 points
            ***         >= 1000:  2 points
            ***     10 games not timed out (1 of 1 points)
            ***         Grading scheme:
            ***          < 0:  fail
            ***         >= 0:  0 points
            ***         >= 10:  1 points
            ***     10 wins (3 of 3 points)
            ***         Grading scheme:
            ***          < 1:  fail
            ***         >= 1:  1 points
            ***         >= 5:  2 points
            ***         >= 10:  3 points

            ### Question q5: 6/6 ###


            Finished at 12:21:15

            Provisional grader
            ==================
            Question q5: 6/6
            ------------------
            Total: 6/6

            Your grader are NOT yet registered.  To register your grader, make sure
            to follow your instructor's guidelines to receive credit on your name_project.


            Process finished with exit code 0

    """
    grid_wall: Grid = game_state_successor_pacman.getWalls()

    def evaluation_function_heuristic_cost_ucs_crude(position_1, position_2):
        return _get_heuristic_cost_ucs_crude(grid_wall, position_1, position_2, None)

    result = evaluation_function_food_and_ghost_helper(game_state_successor_pacman,
                                                        evaluation_function_heuristic_cost_ucs_crude)

    return result


# Abbreviation
# better = better_evaluation_function
