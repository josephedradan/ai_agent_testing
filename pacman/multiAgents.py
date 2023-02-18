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


# def evaluation_function_food_and_ghost(successorGameState: State,
#                                        function_get_distance: callable = util.manhattanDistance):
#     """
#     Evaluation function used for str_question 1
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
#     grid_food: GridPacman = successorGameState.getFood()
#
#     list_position_food: List[Tuple[int, int]] = grid_food.asList()
#
#     agent_state_pacman: ContainerState = successorGameState.getPacmanState()
#
#     score_new: float = successorGameState.getScore()
#
#     list_agent_state_ghost: List[ContainerState] = successorGameState.getGhostStates()
#
#     list_agent_state_ghost_active: List[ContainerState] = []
#
#     list_agent_state_ghost_scared: List[ContainerState] = []
#
#     for agent_state_ghost in list_agent_state_ghost:
#         if agent_state_ghost.time_scared > 0:
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
#     # # If list_capsule exist and ghosts
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
#     A reflex player chooses an action at each choice point by examining
#     its alternatives via a state evaluation function.
#
#     The code below is provided as a guide.  You are welcome to change
#     it in any way you see fit, so long as you don't touch our method
#     headers.
#     """
#
#     def getAction(self, state: State) -> string_given:
#         """
#         You do not need to change this method, but you're welcome to.
#
#         getAction chooses among the best options according to the evaluation function.
#
#         Just like in the previous name_project, getAction takes a State and returns
#         some ActionDirection.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
#         """
#         # Collect legal moves and successor states
#         legalMoves = state.getLegalActions()
#
#         # Choose one of the best actions
#         scores = [self.evaluationFunction(state, action) for action in legalMoves]
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
#     def evaluationFunction(self, state_current: State, action) -> float:
#         """
#         Design a better evaluation function here.
#
#         The evaluation function takes in the current and proposed successor
#         GameStates (pacman.py) and returns a number, where higher numbers are better.
#
#         The code below extracts some useful information from the state, like the
#         remaining food (newFood) and Pacman _position after moving (newPos).
#         newScaredTimes holds the number of moves that each ghost will remain
#         scared because of Pacman having eaten a power pellet.
#
#         Print out these variables to see what you're getting, then combine them
#         to create a masterful evaluation function.
#         """
#         # Useful information you can extract from a State (pacman.py)
#         successorGameState: State = state_current.generatePacmanSuccessor(action)
#         newPos: Tuple[int, int] = successorGameState.getPacmanPosition()
#         newFood: GridPacman = successorGameState.getFood()
#         newGhostStates: List[ContainerState] = successorGameState.getGhostStates()
#         newScaredTimes: List[float] = [container_state.time_scared for container_state in newGhostStates]
#
#         "*** YOUR CODE HERE ***"
#         """
#         Notes:
#             return a number, where higher numbers are better
#
#         Run:
#             Testing:
#                 python pacman.py -f -ap AgentPacmanReflex -l testClassic
#                 python36 pacman.py -f -ap AgentPacmanReflex -l testClassic
#                 py -3.6 pacman.py -f -ap AgentPacmanReflex -l testClassic  # Use this one
#
#             Actual:
#                 python autograder.py -q q1 --no-graphics
#                 py -3.6 autograder.py -q q1 --no-graphics  # Use this one
#                 py -3.6 autograder.py -q q1
#         """
#
#         # print("state_current", type(state_current), state_current)
#         # print("action", type(action), action)
#         #
#         # print("successorGameState", type(successorGameState), successorGameState)
#         # print("newPos (Pacman new _position after movement)", type(newPos), newPos)
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
#         pacman: ContainerState = successorGameState.getPacmanState()
#
#         score_new: float = successorGameState.getScore()
#
#         const_value: float = successorGameState.getScore()
#         ####################
#
#         # """
#         # V1
#         #     Involve the influence of closest food _position and closest ghost _position onto pacman's score
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
#         #         Provisional grader
#         #         ==================
#         #         Question q1: 3/4
#         #         ------------------
#         #         Total: 3/4
#         #
#         #     score_ghost_closest, score_food_closest ** 2
#         #         Provisional grader
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
#                 *** PASS: test_cases\q1\grade-player.test (4 of 4 points)
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
#                 Provisional grader
#                 ==================
#                 Question q1: 4/4
#                 ------------------
#                 Total: 4/4
#
#                 Your grader are NOT yet registered.  To register your grader, make sure
#                 to follow your instructor's guidelines to receive credit on your name_project.
#         """
#
#         return evaluation_function_food_and_ghost(successorGameState)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()




##############################################################################################################








##############################################################################################################



##############################################################################################################

