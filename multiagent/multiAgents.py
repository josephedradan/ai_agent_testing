# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import random
from functools import lru_cache
from queue import PriorityQueue
from typing import List
from typing import Set
from typing import Tuple
from typing import Union

import util
from multiagent.agent.agent import Agent
from multiagent.agent.state_agent import AgentState
from multiagent.game.gamestate import GameState
from multiagent.game.grid import Grid


# def evaluation_function_food_and_ghost(successorGameState: GameState,
#                                        function_get_distance: callable = util.manhattanDistance):
#     """
#     Evaluation function used for question 1
#
#     Notes:
#         This algorithm involves the influence of closest:
#             active ghosts
#             scared ghosts
#             food
#
#         which add onto or subtract from score_new.
#         score_new is just successorGameState.getScore()
#
#     """
#
#     """
#     Because my code deals with fractions and I want to use exponents, you need a bias >= 1 because linear results
#     are bigger than exponential results from 0 to 1
#
#     Basically, graph x, x^2, and x^3 and notice that line has a greater y value from 0 to 1
#     """
#     constant_bias = 1
#
#     list_position_capsule: List[Tuple[int, int]] = successorGameState.getCapsules()
#
#     grid_food: Grid = successorGameState.getFood()
#
#     list_position_food: List[Tuple[int, int]] = grid_food.asList()
#
#     agent_state_pacman: AgentState = successorGameState.getPacmanState()
#
#     score_new: float = successorGameState.getScore()
#
#     list_agent_state_ghost: List[AgentState] = successorGameState.getGhostStates()
#
#     list_agent_state_ghost_active: List[AgentState] = []
#
#     list_agent_state_ghost_scared: List[AgentState] = []
#
#     for agent_state_ghost in list_agent_state_ghost:
#         if agent_state_ghost.scaredTimer > 0:
#             list_agent_state_ghost_scared.append(agent_state_ghost)
#         else:
#             list_agent_state_ghost_active.append(agent_state_ghost)
#
#     # Used for debugging
#     score_capsule_closest = 0
#     score_food_closest = 0
#     score_ghost_active_closest = 0
#     score_ghost_scared_closest = 0
#
#     # # If capsules exist and ghosts
#     # if list_position_capsule:
#     #     # Get the closest capsule to Pacman
#     #     distance_pacman_to_capsule_closest = min(
#     #         [function_get_distance(agent_state_pacman.getPosition(), position_capsule) for position_capsule in
#     #          list_position_capsule]
#     #     )
#     #
#     #     # Closer a capsule is, better score_food_closest
#     #     score_capsule_closest = (
#     #         ((1 / distance_pacman_to_capsule_closest) + constant_bias)
#     #         if distance_pacman_to_capsule_closest != 0 else 0
#     #     )
#     #
#     #     # print(score_capsule_closest)
#     #
#     #     # Closer a scared ghost is, score_capsule_closest^POWER (because scared ghost are good money)
#     #     score_capsule_closest = score_capsule_closest * 8
#     #
#     #     # Modify score_new
#     #     score_new += score_capsule_closest
#
#     # Check active ghosts exist
#     if list_agent_state_ghost_active:
#         # Get the closest ghost to Pacman
#         distance_pacman_to_ghost_closest = min(
#             [function_get_distance(agent_state_pacman.getPosition(), agent_state_ghost_active.getPosition()) for
#              agent_state_ghost_active in list_agent_state_ghost_active]
#         )
#
#         # Closer a ghost is, worse score_ghost_active_closest
#         score_ghost_active_closest = (
#             ((1 / distance_pacman_to_ghost_closest) + constant_bias)
#             if distance_pacman_to_ghost_closest != 0 else 0
#         )
#
#         if function_get_distance is util.manhattanDistance:
#             # Closer a ghost is, score_ghost_active_closest^POWER (because ghost is dangerous up close)
#             score_ghost_active_closest = score_ghost_active_closest ** 2.675  # 2.675 based on trial and error
#         else:
#             score_ghost_active_closest = score_ghost_active_closest ** 2.485  # 2.485 based on trial and error
#
#         # Modify score_new
#         score_new += score_ghost_active_closest * -1
#
#     # Check scared ghosts exist
#     if list_agent_state_ghost_scared:
#         # Get the closest scared ghost to Pacman
#         distance_pacman_to_ghost_scared_closest = min(
#             [function_get_distance(agent_state_pacman.getPosition(), agent_state_ghost_scared.getPosition()) for
#              agent_state_ghost_scared in list_agent_state_ghost_scared]
#         )
#
#         # Closer a scared ghost is, better score_ghost_scared_closest
#         score_ghost_scared_closest = (
#             ((1 / distance_pacman_to_ghost_scared_closest) + constant_bias)
#             if distance_pacman_to_ghost_scared_closest != 0 else 0
#         )
#
#         if function_get_distance is util.manhattanDistance:
#             # Closer a scared ghost is, score_ghost_scared_closest^POWER (because scared ghosts are good money)
#             score_ghost_scared_closest = score_ghost_scared_closest ** 4  # 4 based on trial and error
#         else:
#             score_ghost_scared_closest = score_ghost_scared_closest ** 6.7  # 6.7 based on trial and error
#
#         score_new += score_ghost_scared_closest
#
#     # # Check if food exists
#     if list_position_food:
#         # Get the closest food to Pacman
#         distance_pacman_to_food_closest = min(
#             [function_get_distance(agent_state_pacman.getPosition(), position_food) for position_food in
#              list_position_food]
#         )
#
#         # Closer a food is, better score_food_closest
#         score_food_closest = (
#             ((1 / distance_pacman_to_food_closest) + constant_bias)
#             if distance_pacman_to_food_closest != 0 else 0
#         )
#
#         if function_get_distance is util.manhattanDistance:
#             score_food_closest = score_food_closest ** 2  # 2 based on initial guess
#         else:
#             score_food_closest = score_food_closest ** 2  # 2 based on initial guess
#
#         # Modify score_new
#         score_new += score_food_closest
#
#     # print("{:<8.2f}{:<8.2f}{:<8.2f}{:<8.2f}{:<8.2f}".format(score_new,
#     #                                                         score_capsule_closest,
#     #                                                         score_food_closest,
#     #                                                         score_ghost_active_closest,
#     #                                                         score_ghost_scared_closest))
#
#     return score_new
#
#
# class AgentPacmanReflex(Agent):
#     """
#     A reflex agent chooses an action at each choice point by examining
#     its alternatives via a game_state evaluation function.
#
#     The code below is provided as a guide.  You are welcome to change
#     it in any way you see fit, so long as you don't touch our method
#     headers.
#     """
#
#     def getAction(self, game_state: GameState) -> str:
#         """
#         You do not need to change this method, but you're welcome to.
#
#         getAction chooses among the best options according to the evaluation function.
#
#         Just like in the previous project, getAction takes a GameState and returns
#         some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
#         """
#         # Collect legal moves and successor states
#         legalMoves = game_state.getLegalActions()
#
#         # Choose one of the best actions
#         scores = [self.evaluationFunction(game_state, action) for action in legalMoves]
#         bestScore = max(scores)
#         bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
#         chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
#
#         "Add more of your code here if you want to"
#
#         """
#         Notes:
#             1.  Calls evaluationFunction for each move and puts the result of the call into a list of max scores
#             2.  Select the max score of the list of max scores
#             3.  Make a list of indices that represents the action (e.g. index for "North" action is 3) that
#                 has the max score
#             4.  randomly select a index in list of indices
#             5.  Use legalMoves and input the randomly selected index to get an action (e.g "North") and return it
#         """
#
#         # print("legalMoves", type(legalMoves), legalMoves)
#
#         return legalMoves[chosenIndex]
#
#     def evaluationFunction(self, game_state_current: GameState, action) -> float:
#         """
#         Design a better evaluation function here.
#
#         The evaluation function takes in the current and proposed successor
#         GameStates (pacman.py) and returns a number, where higher numbers are better.
#
#         The code below extracts some useful information from the game_state, like the
#         remaining food (newFood) and Pacman position after moving (newPos).
#         newScaredTimes holds the number of moves that each ghost will remain
#         scared because of Pacman having eaten a power pellet.
#
#         Print out these variables to see what you're getting, then combine them
#         to create a masterful evaluation function.
#         """
#         # Useful information you can extract from a GameState (pacman.py)
#         successorGameState: GameState = game_state_current.generatePacmanSuccessor(action)
#         newPos: Tuple[int, int] = successorGameState.getPacmanPosition()
#         newFood: Grid = successorGameState.getFood()
#         newGhostStates: List[AgentState] = successorGameState.getGhostStates()
#         newScaredTimes: List[float] = [ghostState.scaredTimer for ghostState in newGhostStates]
#
#         "*** YOUR CODE HERE ***"
#         """
#         Notes:
#             return a number, where higher numbers are better
#
#         Run:
#             Testing:
#                 python pacman.py -f -p AgentPacmanReflex -l testClassic
#                 python36 pacman.py -f -p AgentPacmanReflex -l testClassic
#                 py -3.6 pacman.py -f -p AgentPacmanReflex -l testClassic  # Use this one
#
#             Actual:
#                 python autograder.py -q q1 --no-graphics
#                 py -3.6 autograder.py -q q1 --no-graphics  # Use this one
#                 py -3.6 autograder.py -q q1
#         """
#
#         # print("game_state_current", type(game_state_current), game_state_current)
#         # print("action", type(action), action)
#         #
#         # print("successorGameState", type(successorGameState), successorGameState)
#         # print("newPos (Pacman new pos after movement)", type(newPos), newPos)
#         # print("newFood", type(newFood), newFood)
#         # print("newGhostStates", type(newGhostStates), newGhostStates)
#         # print("newScaredTimes", type(newScaredTimes), newScaredTimes)
#         # print("successorGameState.getScore()", type(successorGameState.getScore()), successorGameState.getScore())
#         #
#         # print("successorGameState.getPacmanState()",
#         #       type(successorGameState.getPacmanState()),
#         #       successorGameState.getPacmanState())
#         #
#         # print("#" * 100)
#
#         ####################
#         pacman: AgentState = successorGameState.getPacmanState()
#
#         score_new: float = successorGameState.getScore()
#
#         const_value: float = successorGameState.getScore()
#         ####################
#
#         # """
#         # V1
#         #     Involve the influence of closest food position and closest ghost position onto pacman's score
#         #
#         # IMPORTANT NOTES:
#         #     VALUE PACMAN'S LIFE (AVOID GHOSTS) OVER FOOD
#         #
#         # Results:
#         #     score_ghost_closest, score_food_closest
#         #         ==================
#         #         Question q1: 3/4
#         #         ------------------
#         #         Total: 3/4
#         #
#         #     score_ghost_closest ** 2, score_food_closest
#         #         ==================
#         #         Question q1: 4/4
#         #         ------------------
#         #         Total: 4/4
#         #
#         #     score_ghost_closest ** 2, score_food_closest ** 2
#         #         Provisional grades
#         #         ==================
#         #         Question q1: 3/4
#         #         ------------------
#         #         Total: 3/4
#         #
#         #     score_ghost_closest, score_food_closest ** 2
#         #         Provisional grades
#         #         ==================
#         #         Question q1: 2/4
#         #         ------------------
#         #         Total: 2/4
#         # """
#         #
#         # distance_pacman_to_ghost_closest = None
#         #
#         # position_ghost: Tuple[int, int]
#         #
#         # # Handle ghost positions
#         # for position_ghost in successorGameState.getGhostPositions():
#         #     distance_pacman_to_ghost = util.manhattanDistance(pacman.getPosition(), position_ghost)
#         #
#         #     # The further away ghosts are, add to score_new
#         #     # score_new += distance_pacman_to_ghost
#         #
#         #     if distance_pacman_to_ghost_closest is None:
#         #         distance_pacman_to_ghost_closest = distance_pacman_to_ghost
#         #     elif distance_pacman_to_ghost < distance_pacman_to_ghost_closest:
#         #         distance_pacman_to_ghost_closest = distance_pacman_to_ghost
#         #
#         # if distance_pacman_to_ghost_closest:
#         #     # Closer a ghost is, better score_ghost_closest
#         #     score_ghost_closest = (1 / distance_pacman_to_ghost_closest) if distance_pacman_to_ghost_closest != 0 else 0
#         #
#         #     # Closer the ghost is, score_ghost_closest^2 (because ghost is dangerous up close)
#         #     score_ghost_closest = score_ghost_closest ** 2
#         #
#         #     score_new -= score_ghost_closest
#         #
#         # #####
#         #
#         # position_food: Tuple[int, int]
#         #
#         # distance_pacman_to_food_closest = None
#         #
#         # # Handle food positions
#         # for position_food in newFood.asList():
#         #     distance_pacman_to_food = util.manhattanDistance(pacman.getPosition(), position_food)
#         #
#         #     # The closer the food is, add to score_new
#         #     # score_new += (1 / distance_pacman_to_food)
#         #
#         #     if distance_pacman_to_food_closest is None:
#         #         distance_pacman_to_food_closest = distance_pacman_to_food
#         #     elif distance_pacman_to_food < distance_pacman_to_food_closest:
#         #         distance_pacman_to_food_closest = distance_pacman_to_food
#         #
#         # if distance_pacman_to_food_closest:
#         #     # Closer a food is, better score_food_closest
#         #     score_food_closest = (1 / distance_pacman_to_food_closest) if distance_pacman_to_food_closest != 0 else 0
#         #
#         #     """
#         #     IMPORTANT NOTES:
#         #         BASED ON TESTING PACMAN'S LIFE IS MORE VALUABLE THAN FOOD SO ONLY SQUARE score_ghost_closest
#         #
#         #     """
#         #     # # Closer a food is, score_food_closest^2
#         #     # score_food_closest = score_food_closest ** 2
#         #
#         #     score_new += score_food_closest
#         #
#         # return score_new
#
#         ##########
#
#         r"""
#         V2
#             Improved version of V1
#
#             It involves the influence of closest:
#                 active ghost (the ghosts that can kill)
#                 scared ghost (the ghosts that give you points)
#                 food
#
#         IMPORTANT NOTES:
#             VALUE PACMAN'S LIFE (AVOID GHOSTS) OVER FOOD
#
#         Results:
#             py -3.6 autograder.py -q q1 --no-graphics
#                 Question q1
#                 ===========
#
#                 Pacman emerges victorious! Score: 1429
#                 Pacman emerges victorious! Score: 1190
#                 Pacman emerges victorious! Score: 1245
#                 Pacman emerges victorious! Score: 1237
#                 Pacman emerges victorious! Score: 1423
#                 Pacman emerges victorious! Score: 1254
#                 Pacman emerges victorious! Score: 1235
#                 Pacman emerges victorious! Score: 1229
#                 Pacman emerges victorious! Score: 1411
#                 Pacman emerges victorious! Score: 1433
#                 Average Score: 1308.6
#                 Scores:        1429.0, 1190.0, 1245.0, 1237.0, 1423.0, 1254.0, 1235.0, 1229.0, 1411.0, 1433.0
#                 Win Rate:      10/10 (1.00)
#                 Record:        Win, Win, Win, Win, Win, Win, Win, Win, Win, Win
#                 *** PASS: test_cases\q1\grade-agent.test (4 of 4 points)
#                 ***     1308.6 average score (2 of 2 points)
#                 ***         Grading scheme:
#                 ***          < 500:  0 points
#                 ***         >= 500:  1 points
#                 ***         >= 1000:  2 points
#                 ***     10 games not timed out (0 of 0 points)
#                 ***         Grading scheme:
#                 ***          < 10:  fail
#                 ***         >= 10:  0 points
#                 ***     10 wins (2 of 2 points)
#                 ***         Grading scheme:
#                 ***          < 1:  fail
#                 ***         >= 1:  0 points
#                 ***         >= 5:  1 points
#                 ***         >= 10:  2 points
#
#                 ### Question q1: 4/4 ###
#
#
#                 Finished at 12:29:14
#
#                 Provisional grades
#                 ==================
#                 Question q1: 4/4
#                 ------------------
#                 Total: 4/4
#
#                 Your grades are NOT yet registered.  To register your grades, make sure
#                 to follow your instructor's guidelines to receive credit on your project.
#         """
#
#         return evaluation_function_food_and_ghost(successorGameState)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the game_state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()




##############################################################################################################








##############################################################################################################



##############################################################################################################

# Cache inputs to prevent repeat calculations
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


def betterEvaluationFunction(currentGameState: GameState) -> float:
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

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
    #         Provisional grades
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
            
            Provisional grades
            ==================
            Question q5: 6/6
            ------------------
            Total: 6/6
            
            Your grades are NOT yet registered.  To register your grades, make sure
            to follow your instructor's guidelines to receive credit on your project.
            
            
            Process finished with exit code 0

    """
    grid_wall: Grid = game_state_successor_pacman.getWalls()

    def evaluation_function_heuristic_cost_ucs_crude(position_1, position_2):
        return _get_heuristic_cost_ucs_crude(grid_wall, position_1, position_2, None)

    result = evaluation_function_partial_food_and_ghost(game_state_successor_pacman,
                                                evaluation_function_heuristic_cost_ucs_crude)

    return result


# Abbreviation
better = betterEvaluationFunction
