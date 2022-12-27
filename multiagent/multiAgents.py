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
from typing import Tuple, List, Union, Set

import util
from multiagent.agent.agent import Agent
from multiagent.agent.state_agent import AgentState
from multiagent.game import gamestate
from multiagent.game.grid import Grid


def evaluation_function_food_and_ghost(successorGameState: GameState,
                                       function_get_distance: callable = util.manhattanDistance):
    """
    Evaluation function used for question 1

    Notes:
        This algorithm involves the influence of closest:
            active ghosts
            scared ghosts
            food

        which add onto or subtract from score_new.
        score_new is just successorGameState.getScore()

    """

    """
    Because my code deals with fractions and I want to use exponents, you need a bias >= 1 because linear results
    are bigger than exponential results from 0 to 1
    
    Basically, graph x, x^2, and x^3 and notice that line has a greater y value from 0 to 1
    """
    constant_bias = 1

    list_position_capsule: List[Tuple[int, int]] = successorGameState.getCapsules()

    grid_food: Grid = successorGameState.getFood()

    list_position_food: List[Tuple[int, int]] = grid_food.asList()

    agent_state_pacman: AgentState = successorGameState.getPacmanState()

    score_new: float = successorGameState.getScore()

    list_agent_state_ghost: List[AgentState] = successorGameState.getGhostStates()

    list_agent_state_ghost_active: List[AgentState] = []

    list_agent_state_ghost_scared: List[AgentState] = []

    for agent_state_ghost in list_agent_state_ghost:
        if agent_state_ghost.scaredTimer > 0:
            list_agent_state_ghost_scared.append(agent_state_ghost)
        else:
            list_agent_state_ghost_active.append(agent_state_ghost)

    # Used for debugging
    score_capsule_closest = 0
    score_food_closest = 0
    score_ghost_active_closest = 0
    score_ghost_scared_closest = 0

    # # If capsules exist and ghosts
    # if list_position_capsule:
    #     # Get the closest capsule to Pacman
    #     distance_pacman_to_capsule_closest = min(
    #         [function_get_distance(agent_state_pacman.getPosition(), position_capsule) for position_capsule in
    #          list_position_capsule]
    #     )
    #
    #     # Closer a capsule is, better score_food_closest
    #     score_capsule_closest = (
    #         ((1 / distance_pacman_to_capsule_closest) + constant_bias)
    #         if distance_pacman_to_capsule_closest != 0 else 0
    #     )
    #
    #     # print(score_capsule_closest)
    #
    #     # Closer a scared ghost is, score_capsule_closest^POWER (because scared ghost are good money)
    #     score_capsule_closest = score_capsule_closest * 8
    #
    #     # Modify score_new
    #     score_new += score_capsule_closest

    # Check active ghosts exist
    if list_agent_state_ghost_active:
        # Get the closest ghost to Pacman
        distance_pacman_to_ghost_closest = min(
            [function_get_distance(agent_state_pacman.getPosition(), agent_state_ghost_active.getPosition()) for
             agent_state_ghost_active in list_agent_state_ghost_active]
        )

        # Closer a ghost is, worse score_ghost_active_closest
        score_ghost_active_closest = (
            ((1 / distance_pacman_to_ghost_closest) + constant_bias)
            if distance_pacman_to_ghost_closest != 0 else 0
        )

        if function_get_distance is util.manhattanDistance:
            # Closer a ghost is, score_ghost_active_closest^POWER (because ghost is dangerous up close)
            score_ghost_active_closest = score_ghost_active_closest ** 2.675  # 2.675 based on trial and error
        else:
            score_ghost_active_closest = score_ghost_active_closest ** 2.485  # 2.485 based on trial and error

        # Modify score_new
        score_new += score_ghost_active_closest * -1

    # Check scared ghosts exist
    if list_agent_state_ghost_scared:
        # Get the closest scared ghost to Pacman
        distance_pacman_to_ghost_scared_closest = min(
            [function_get_distance(agent_state_pacman.getPosition(), agent_state_ghost_scared.getPosition()) for
             agent_state_ghost_scared in list_agent_state_ghost_scared]
        )

        # Closer a scared ghost is, better score_ghost_scared_closest
        score_ghost_scared_closest = (
            ((1 / distance_pacman_to_ghost_scared_closest) + constant_bias)
            if distance_pacman_to_ghost_scared_closest != 0 else 0
        )

        if function_get_distance is util.manhattanDistance:
            # Closer a scared ghost is, score_ghost_scared_closest^POWER (because scared ghosts are good money)
            score_ghost_scared_closest = score_ghost_scared_closest ** 4  # 4 based on trial and error
        else:
            score_ghost_scared_closest = score_ghost_scared_closest ** 6.7  # 6.7 based on trial and error

        score_new += score_ghost_scared_closest

    # # Check if food exists
    if list_position_food:
        # Get the closest food to Pacman
        distance_pacman_to_food_closest = min(
            [function_get_distance(agent_state_pacman.getPosition(), position_food) for position_food in
             list_position_food]
        )

        # Closer a food is, better score_food_closest
        score_food_closest = (
            ((1 / distance_pacman_to_food_closest) + constant_bias)
            if distance_pacman_to_food_closest != 0 else 0
        )

        if function_get_distance is util.manhattanDistance:
            score_food_closest = score_food_closest ** 2  # 2 based on initial guess
        else:
            score_food_closest = score_food_closest ** 2  # 2 based on initial guess

        # Modify score_new
        score_new += score_food_closest

    # print("{:<8.2f}{:<8.2f}{:<8.2f}{:<8.2f}{:<8.2f}".format(score_new,
    #                                                         score_capsule_closest,
    #                                                         score_food_closest,
    #                                                         score_ghost_active_closest,
    #                                                         score_ghost_scared_closest))

    return score_new


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState) -> str:
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        """
        Notes:
            1.  Calls evaluationFunction for each move and puts the result of the call into a list of max scores
            2.  Select the max score of the list of max scores
            3.  Make a list of indices that represents the action (e.g. index for "North" action is 3) that 
                has the max score
            4.  randomly select a index in list of indices
            5.  Use legalMoves and input the randomly selected index to get an action (e.g "North") and return it
        """

        # print("legalMoves", type(legalMoves), legalMoves)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action) -> float:
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState: GameState = currentGameState.generatePacmanSuccessor(action)
        newPos: Tuple[int, int] = successorGameState.getPacmanPosition()
        newFood: Grid = successorGameState.getFood()
        newGhostStates: List[AgentState] = successorGameState.getGhostStates()
        newScaredTimes: List[float] = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """
        Notes:
            return a number, where higher numbers are better
            
        Run:
            Testing:
                python pacman.py -f -p ReflexAgent -l testClassic
                python36 pacman.py -f -p ReflexAgent -l testClassic
                py -3.6 pacman.py -f -p ReflexAgent -l testClassic  # Use this one
                
            Actual:
                python autograder.py -q q1 --no-graphics
                py -3.6 autograder.py -q q1 --no-graphics  # Use this one
                py -3.6 autograder.py -q q1
        """

        # print("currentGameState", type(currentGameState), currentGameState)
        # print("action", type(action), action)
        #
        # print("successorGameState", type(successorGameState), successorGameState)
        # print("newPos (Pacman new pos after movement)", type(newPos), newPos)
        # print("newFood", type(newFood), newFood)
        # print("newGhostStates", type(newGhostStates), newGhostStates)
        # print("newScaredTimes", type(newScaredTimes), newScaredTimes)
        # print("successorGameState.getScore()", type(successorGameState.getScore()), successorGameState.getScore())
        #
        # print("successorGameState.getPacmanState()",
        #       type(successorGameState.getPacmanState()),
        #       successorGameState.getPacmanState())
        #
        # print("#" * 100)

        ####################
        pacman: AgentState = successorGameState.getPacmanState()

        score_new: float = successorGameState.getScore()

        const_value: float = successorGameState.getScore()
        ####################

        # """
        # V1
        #     Involve the influence of closest food position and closest ghost position onto pacman's score
        #
        # IMPORTANT NOTES:
        #     VALUE PACMAN'S LIFE (AVOID GHOSTS) OVER FOOD
        #
        # Results:
        #     score_ghost_closest, score_food_closest
        #         ==================
        #         Question q1: 3/4
        #         ------------------
        #         Total: 3/4
        #
        #     score_ghost_closest ** 2, score_food_closest
        #         ==================
        #         Question q1: 4/4
        #         ------------------
        #         Total: 4/4
        #
        #     score_ghost_closest ** 2, score_food_closest ** 2
        #         Provisional grades
        #         ==================
        #         Question q1: 3/4
        #         ------------------
        #         Total: 3/4
        #
        #     score_ghost_closest, score_food_closest ** 2
        #         Provisional grades
        #         ==================
        #         Question q1: 2/4
        #         ------------------
        #         Total: 2/4
        # """
        #
        # distance_pacman_to_ghost_closest = None
        #
        # position_ghost: Tuple[int, int]
        #
        # # Handle ghost positions
        # for position_ghost in successorGameState.getGhostPositions():
        #     distance_pacman_to_ghost = util.manhattanDistance(pacman.getPosition(), position_ghost)
        #
        #     # The further away ghosts are, add to score_new
        #     # score_new += distance_pacman_to_ghost
        #
        #     if distance_pacman_to_ghost_closest is None:
        #         distance_pacman_to_ghost_closest = distance_pacman_to_ghost
        #     elif distance_pacman_to_ghost < distance_pacman_to_ghost_closest:
        #         distance_pacman_to_ghost_closest = distance_pacman_to_ghost
        #
        # if distance_pacman_to_ghost_closest:
        #     # Closer a ghost is, better score_ghost_closest
        #     score_ghost_closest = (1 / distance_pacman_to_ghost_closest) if distance_pacman_to_ghost_closest != 0 else 0
        #
        #     # Closer the ghost is, score_ghost_closest^2 (because ghost is dangerous up close)
        #     score_ghost_closest = score_ghost_closest ** 2
        #
        #     score_new -= score_ghost_closest
        #
        # #####
        #
        # position_food: Tuple[int, int]
        #
        # distance_pacman_to_food_closest = None
        #
        # # Handle food positions
        # for position_food in newFood.asList():
        #     distance_pacman_to_food = util.manhattanDistance(pacman.getPosition(), position_food)
        #
        #     # The closer the food is, add to score_new
        #     # score_new += (1 / distance_pacman_to_food)
        #
        #     if distance_pacman_to_food_closest is None:
        #         distance_pacman_to_food_closest = distance_pacman_to_food
        #     elif distance_pacman_to_food < distance_pacman_to_food_closest:
        #         distance_pacman_to_food_closest = distance_pacman_to_food
        #
        # if distance_pacman_to_food_closest:
        #     # Closer a food is, better score_food_closest
        #     score_food_closest = (1 / distance_pacman_to_food_closest) if distance_pacman_to_food_closest != 0 else 0
        #
        #     """
        #     IMPORTANT NOTES:
        #         BASED ON TESTING PACMAN'S LIFE IS MORE VALUABLE THAN FOOD SO ONLY SQUARE score_ghost_closest
        #
        #     """
        #     # # Closer a food is, score_food_closest^2
        #     # score_food_closest = score_food_closest ** 2
        #
        #     score_new += score_food_closest
        #
        # return score_new

        ##########

        r"""
        V2
            Improved version of V1
            
            It involves the influence of closest:
                active ghost (the ghosts that can kill)
                scared ghost (the ghosts that give you points)
                food

        IMPORTANT NOTES:
            VALUE PACMAN'S LIFE (AVOID GHOSTS) OVER FOOD

        Results:
            py -3.6 autograder.py -q q1 --no-graphics
                Question q1
                ===========
                
                Pacman emerges victorious! Score: 1429
                Pacman emerges victorious! Score: 1190
                Pacman emerges victorious! Score: 1245
                Pacman emerges victorious! Score: 1237
                Pacman emerges victorious! Score: 1423
                Pacman emerges victorious! Score: 1254
                Pacman emerges victorious! Score: 1235
                Pacman emerges victorious! Score: 1229
                Pacman emerges victorious! Score: 1411
                Pacman emerges victorious! Score: 1433
                Average Score: 1308.6
                Scores:        1429.0, 1190.0, 1245.0, 1237.0, 1423.0, 1254.0, 1235.0, 1229.0, 1411.0, 1433.0
                Win Rate:      10/10 (1.00)
                Record:        Win, Win, Win, Win, Win, Win, Win, Win, Win, Win
                *** PASS: test_cases\q1\grade-agent.test (4 of 4 points)
                ***     1308.6 average score (2 of 2 points)
                ***         Grading scheme:
                ***          < 500:  0 points
                ***         >= 500:  1 points
                ***         >= 1000:  2 points
                ***     10 games not timed out (0 of 0 points)
                ***         Grading scheme:
                ***          < 10:  fail
                ***         >= 10:  0 points
                ***     10 wins (2 of 2 points)
                ***         Grading scheme:
                ***          < 1:  fail
                ***         >= 1:  0 points
                ***         >= 5:  1 points
                ***         >= 10:  2 points
                
                ### Question q1: 4/4 ###
                
                
                Finished at 12:29:14
                
                Provisional grades
                ==================
                Question q1: 4/4
                ------------------
                Total: 4/4
                
                Your grades are NOT yet registered.  To register your grades, make sure
                to follow your instructor's guidelines to receive credit on your project.
        """

        return evaluation_function_food_and_ghost(successorGameState)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


##############################################################################################################

class AgentContainer:
    __slots__ = ["index_agent", "action", "score"]

    def __init__(self, index_agent, action):
        self.index_agent = index_agent
        self.action = action
        self.score = None

    def __str__(self):
        return "({} {} {})".format(self.index_agent, self.action, self.score)


# @callgraph(use_list_index_args=[1, 3, 4], display_callable_name=False, )
def dfs_recursive_minimax_v1(game_state: GameState,
                             depth: int,
                             function_evaluation: callable,
                             index_agent: int = 0,
                             agent_container_previous: AgentContainer = None,
                             ) -> [float, AgentContainer]:
    """
    Does dfs recursive minimax

    Notes:
        Does not work because you are stacking multiple min agents on top of each other which causes min of min

        Basically, you want
            max -> min -> max -> min -> max -> etc...
            not
            max -> min -> min -> max -> min -> min

        because you will propagate multiple min values which is wrong

    IMPORTANT NOTES:
        THE ASSUMPTION MADE in "Notes" IS WRONG, LOOK AT dfs_recursive_minimax_v3 FOR CORRECT SOLUTION

        DO NOT USE THIS CODE, IT IS NOT CORRECT AND THE ASSUMPTIONS ARE WRONG

    Reference:
        Algorithms Explained – minimax and alpha-beta pruning
            Reference:
                https://www.youtube.com/watch?v=l-hh51ncgDI
    """

    # print("index_agent", index_agent, "depth", depth)

    # List of legal movements ("North")
    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # Check if game is over via pacman dead or pacman got all food and survived
    if game_state.isWin() or game_state.isLose() or depth == 0:
        score = function_evaluation(game_state)
        agent_container_previous.score = score

        # Return the score
        return score, agent_container_previous

    # If Pacman (Maximizer)
    if index_agent == 0:

        score_max: Union[float, None] = None
        agent_container_final_score_max: Union[AgentContainer, None] = None

        # _LIST_TEMP = []

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            agent_container_current = AgentContainer(index_agent, action)

            # Agent selection (Select next agent for the next call)
            index_agent_new = index_agent + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v1(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  )

            # _LIST_TEMP.append(score_calculated)

            if score_max is None or score_calculated > score_max:
                score_max = score_calculated

                """
                *** INCORRECT TO ASSIGN agent_container_current TO agent_container_final_score_max
                LOOK AT dfs_recursive_minimax_v3 FOR THE CORRECT SOLUTION
                """
                agent_container_final_score_max = agent_container_current

        # print("P Depth", depth)
        # print("P MOVE", list_str_move_legal)
        # print("P ACTION", agent_container_final_score_max.action)
        # print("P CALCULATED", _LIST_TEMP)
        # print("P Score: {} Action: {} ".format(score_max, agent_container_final_score_max.action))
        # print()
        return score_max, agent_container_final_score_max

    # If a Ghost (Minimizer)
    else:
        score_min: Union[float, None] = None
        agent_container_final_score_min: Union[AgentContainer, None] = None

        # _LIST_TEMP = []

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            agent_container_current = AgentContainer(index_agent, action)

            # Agent selection (Select next agent for the next call)
            if index_agent >= game_state.getNumAgents() - 1:
                index_agent_new = 0
                depth -= 1  # Depth is only decremented when all agents have moved

            else:
                index_agent_new = index_agent + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v1(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  )

            # _LIST_TEMP.append(score_calculated)

            if score_min is None or score_calculated < score_min:
                score_min = score_calculated
                """
                *** INCORRECT TO ASSIGN agent_container_current TO agent_container_final_score_min
                LOOK AT dfs_recursive_minimax_v3 FOR THE CORRECT SOLUTION
                """
                agent_container_final_score_min = agent_container_current  # *** WRONG TO ASSIGN agent_container_current

        # print(f"G{index_agent} Depth", depth)
        # print(f"G{index_agent} MOVE", list_str_move_legal)
        # print(f"G{index_agent} ACTION", agent_container_final_score_min.action)
        # print(f"G{index_agent} CALCULATED", _LIST_TEMP)
        # print("G{} Score: {} Action: {} ".format(index_agent, score_min, agent_container_final_score_min.action))
        # print()

        return score_min, agent_container_final_score_min


##############################################################################################################

class AgentGhostContainer:

    def __init__(self, game_state: GameState, index_agent: int, action: str,
                 game_state_previous: GameState):
        self.game_state = game_state
        self.index_agent = index_agent
        self.action = action
        self.game_state_previous = game_state_previous


def get_list_last_ghost_agent_game_state(game_state: GameState,
                                         index_agent: int,
                                         game_state_previous: GameState,
                                         list_game_state: List[float] = None
                                         ) -> List[AgentGhostContainer]:
    """
    This gets the gameState based on the last ghost before it becomes pacman's turn to move

    Notes:
        Needs the first of the ghosts -> returns list of game_state that are the last game_state
        before pacman's turn

    """
    if list_game_state is None:
        list_game_state = []

    if index_agent == 0:
        print("YOUR INPUT IS WRONG")
        return get_list_last_ghost_agent_game_state(game_state, index_agent + 1, game_state_previous)

    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # print(list_str_move_legal)

    for action in list_str_move_legal:

        game_state_new = game_state.generateSuccessor(index_agent, action)

        index_agent_new = index_agent + 1
        # print(index_agent_new)

        if index_agent >= game_state.getNumAgents() - 1:

            # print("ADD TO LIST", index_agent, action, game_state.getGhostPosition(index_agent))
            # if index_agent == 2:
            #     print(game_state.getGhostPosition(index_agent - 1))
            # print()

            agent_ghost_container = AgentGhostContainer(game_state,
                                                        index_agent,
                                                        action,
                                                        game_state_previous)

            list_game_state.append(agent_ghost_container)
        else:
            # print("RECURSIVE CALL", index_agent, action, game_state.getGhostPosition(index_agent))
            # if index_agent == 2:
            #     print(game_state.getGhostPosition(index_agent - 1))

            if game_state.isWin() or game_state.isLose():
                agent_ghost_container = AgentGhostContainer(game_state,
                                                            index_agent,
                                                            action,
                                                            game_state_previous)
                return [agent_ghost_container]

            get_list_last_ghost_agent_game_state(game_state_new,
                                                 index_agent_new,
                                                 game_state,
                                                 list_game_state)

    return list_game_state


# @callgraph(use_list_index_args=[1, 3, 4], display_callable_name=False, )
def dfs_recursive_minimax_v2(game_state: GameState,
                             depth: int,
                             function_evaluation: callable,
                             index_agent: int = 0,
                             agent_container_previous: AgentContainer = None,
                             game_state_previous: GameState = None,
                             ) -> [float, AgentContainer]:
    """
    This function tries to compress all ghost agents together, the problem is that not all ghosts need to move in order
    for the game to end.

    Basically, the game can end when one of the ghosts moves so compressing all ghost agent moves together passes the
    point when the game ends, so it's suboptimal to do this.

    This means that dfs_recursive_minimax_v1 is more correct than this solution.

    IMPORTANT NOTE:
        *** THIS CODE DOES NOT WORK AND THE ASSUMPTIONS ABOUT SKIPPING TO THE LAST GHOST BEFORE PACMAN'S TURN IS WRONG

    """

    # print("index_agent", index_agent)

    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # Check if game is over via pacman dead or pacman got all food and survived
    if game_state.isWin() or game_state.isLose() or depth == 0:
        score = function_evaluation(game_state)
        agent_container_previous.score = score

        # Return the score
        return score, agent_container_previous

    # If Pacman (Maximizer)
    if index_agent == 0:

        score_max: Union[float, None] = None
        agent_container_final_score_max: Union[AgentContainer, None] = None

        list_temp = []

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            agent_container_current = AgentContainer(index_agent, action)

            # Agent selection (Select next agent for the next call)
            index_agent_new = index_agent + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v2(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  game_state,
                                                                                  )

            list_temp.append(score_calculated)

            if score_max is None or score_calculated > score_max:
                score_max = score_calculated
                agent_container_final_score_max = agent_container_current

        # print("depth", depth)
        # print("PACMAN SCORES", list_temp)
        # print()
        return score_max, agent_container_final_score_max

    # If a Ghost (Minimizer)
    else:

        list_last_ghost_agent_game_state = get_list_last_ghost_agent_game_state(game_state,
                                                                                index_agent,
                                                                                game_state_previous)

        # print("list_last_ghost_agent_game_state", list_last_ghost_agent_game_state)

        score_min: Union[float, None] = None
        agent_container_final_score_min: Union[AgentContainer, None] = None

        _LIST_TEMP = []

        for last_ghost_agent_game_state in list_last_ghost_agent_game_state:

            index_agent_last = last_ghost_agent_game_state.index_agent

            action = list_last_ghost_agent_game_state

            game_state_new = last_ghost_agent_game_state.game_state

            agent_container_current = AgentContainer(index_agent_last, action)

            # Agent selection (Select next agent for the next call)
            if index_agent_last >= game_state.getNumAgents() - 1:
                index_agent_new = 0
                depth -= 1  # Depth is only decremented when all agents have moved
            else:
                index_agent_new = index_agent_last + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v2(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  game_state,
                                                                                  )

            _LIST_TEMP.append(score_calculated)

            if score_min is None or score_calculated < score_min:
                score_min = score_calculated
                agent_container_final_score_min = agent_container_current

        # THE BELOW WILL BASICALLY ADDS REPEAT CALLS WHICH IS WRONG.
        # for action in list_str_move_legal:
        #
        #     for last_ghost_agent_game_state in list_last_ghost_agent_game_state:
        #
        #         game_state_last = last_ghost_agent_game_state.game_state
        #         # print("last_ghost_agent_game_state.index_agent", last_ghost_agent_game_state.index_agent)
        #
        #         index_agent_last = last_ghost_agent_game_state.index_agent
        #         game_state_new = game_state_last.generateSuccessor(index_agent_last, action)
        #
        #         agent_container_current = AgentContainer(index_agent_last, action)
        #
        #         # Agent selection (Select next agent for the next call)
        #         if index_agent_last >= game_state.getNumAgents() - 1:
        #             index_agent_new = 0
        #             depth -= 1  # Depth is only decremented when all agents have moved
        #         else:
        #             index_agent_new = index_agent_last + 1
        #
        #         score_calculated, agent_container_returned = dfs_recursive_minimax_v2(game_state_new,
        #                                                                               depth,
        #                                                                               function_evaluation,
        #                                                                               index_agent_new,
        #                                                                               agent_container_current,
        #                                                                               game_state,
        #                                                                               )
        #
        #         _LIST_TEMP.append(score_calculated)
        #
        #         if score_min is None or score_calculated < score_min:
        #             score_min = score_calculated
        #             agent_container_final_score_min = agent_container_current

        # print("depth", depth)
        # print(_LIST_TEMP)
        # print()
        return score_min, agent_container_final_score_min


##############################################################################################################

# @callgraph(use_list_index_args=[1, 3, 4], display_callable_name=False, )
def dfs_recursive_minimax_v3(game_state: GameState,
                             depth: int,
                             function_evaluation: callable,
                             index_agent: int = 0,
                             agent_container_previous: AgentContainer = None,
                             ) -> [float, AgentContainer]:
    """
    DFS Recursive Minimax algorithm almost correctly implemented

    *** THIS CODE IS STILL WRONG, IT ASSUMES THAT THE FIRST CHILDREN OF THE ROOT ARE MINIMIZERS.
        THE CORRECT IMPLEMENTATION IS dfs_recursive_minimax_v4

    IMPORTANT NOTES:
        THE ONLY DIFFERENCE BETWEEN dfs_recursive_minimax_v3 and dfs_recursive_minimax_v1 IS THAT
        THE CORRECT AgentContainer agent_container_returned IS RETURNED FOR
        agent_container_final_score_min
        AND
        agent_container_final_score_max

        *** THE REASON WHY YOU NEED TO RETURN agent_container_returned INSTEAD IS BECAUSE
        YOU HAVE TO REMEMBER THAT YOU ARE SELECTING THE AgentContainer FROM THE FOLLOWING CALL. SO
        agent_container_current IS NOT CORRECT BECAUSE THE FOLLOWING RECURSIVE CALL MAY HAVE FOUND THAT
        agent_container_current MAY NOT BE THE
        agent_container_final_score_min or agent_container_final_score_max

        BECAUSE OF MINOR CODE CHANGE, dfs_recursive_minimax_v3 MUST EXIST SO THAT FUTURE ME WILL NOTICE MY MISTAKE
        AND WILL NOT HAVE TO REPEAT THIS DEBUGGING PROCESS.

    Reference:
        Algorithms Explained – minimax and alpha-beta pruning
            Reference:
                https://www.youtube.com/watch?v=l-hh51ncgDI
    """

    # List of legal movements ("North")
    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # Check if game is over via pacman dead or pacman got all food and survived
    if game_state.isWin() or game_state.isLose() or depth == 0:
        score = function_evaluation(game_state)
        agent_container_previous.score = score
        # Return the score
        return score, agent_container_previous

    # If Pacman (Maximizer)
    if index_agent == 0:

        score_max: Union[float, None] = None
        agent_container_final_score_max: Union[AgentContainer, None] = None

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            agent_container_current = AgentContainer(index_agent, action)

            # Agent selection (Select next agent for the next call)
            index_agent_new = index_agent + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v3(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  )

            if score_max is None or score_calculated > score_max:
                score_max = score_calculated

                """
                *** ASSIGN agent_container_returned TO 
                agent_container_final_score_max
                INSTEAD OF 
                agent_container_current
                BECAUSE THE FOLLOWING CALL MUST SELECT THE AgentContainer
                """
                agent_container_final_score_max = agent_container_returned

        return score_max, agent_container_final_score_max

    # If a Ghost (Minimizer)
    else:
        score_min: Union[float, None] = None
        agent_container_final_score_min: Union[AgentContainer, None] = None

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            agent_container_current = AgentContainer(index_agent, action)

            # Agent selection (Select next agent for the next call)
            if index_agent >= game_state.getNumAgents() - 1:
                index_agent_new = 0
                depth -= 1  # Depth is only decremented when all agents have moved

            else:
                index_agent_new = index_agent + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v3(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  )

            if score_min is None or score_calculated < score_min:
                score_min = score_calculated

                """
                *** ASSIGN agent_container_returned TO 
                agent_container_final_score_min 
                INSTEAD OF 
                agent_container_current
                BECAUSE THE FOLLOWING CALL MUST SELECT THE AgentContainer
                """
                agent_container_final_score_min = agent_container_returned

        return score_min, agent_container_final_score_min


##############################################################################################################

# @callgraph(use_list_index_args=[1, 5, 7], display_callable_name=False, )
def _dfs_recursive_minimax_v4_handler(game_state: GameState,
                                      depth: int,
                                      alpha: Union[None, float],
                                      beta: Union[None, float],
                                      function_evaluation: callable,
                                      index_agent: int = 0,
                                      alpha_beta_pruning: bool = False,
                                      # _callgraph_special: Any = None
                                      ) -> float:
    """
    This is the actual DFS Recursive Minimax algorithm's main body.

    Notes:
        This is the correct implementation of the algorithm needed to get all the points for autograder.py's
        Q2 and Q3

    Reference:
        Algorithms Explained – minimax and alpha-beta pruning
            Reference:
                https://www.youtube.com/watch?v=l-hh51ncgDI
    """

    # Check if game is over via pacman dead or pacman got all food and survived
    if game_state.isWin() or game_state.isLose() or depth <= 0:
        score = function_evaluation(game_state)

        # Return the score
        return score

    # List of legal movements ("North")
    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # If Pacman (Maximizer)
    if index_agent == 0:

        score_max: Union[float, None] = None

        # _LIST_SCORE_DEBUG = []

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            # Agent selection (Select next agent for the next call)
            index_agent_new = index_agent + 1

            score_calculated = _dfs_recursive_minimax_v4_handler(game_state_new,
                                                                 depth,
                                                                 alpha,
                                                                 beta,
                                                                 function_evaluation,
                                                                 index_agent_new,
                                                                 alpha_beta_pruning,
                                                                 # str((depth, index_agent, action))
                                                                 )

            # _LIST_SCORE_DEBUG.append(score_calculated)

            if score_max is None or score_calculated > score_max:
                score_max = score_calculated

            if alpha_beta_pruning:

                if alpha is None or score_calculated > alpha:
                    alpha = score_calculated

                r"""
                Notes:
                    Do not use <= on the minimizer, use < because <= will break test_cases\q3\6-tied-root.test 
                    because it will cut off a branch that may have a low score. Because the code
                    for the minimizer is the same for the maximizer, then the maximizer should have the same
                    logic as the minimizer.

                IMPORTANT NOTES:
                    YOU MUST USE
                        if beta is not None and alpha is not None and beta < alpha
                    AND NOT
                        if beta and alpha and beta < alpha
                    BECAUSE beta AND alpha MIGHT BE 0.0 WHICH WOULD RESULT IN False
                """
                if beta is not None and alpha is not None and beta < alpha:
                    # Cut off branch
                    break

        # print("P Depth", depth)
        # print("P MOVE", list_str_move_legal)
        # print("P CALCULATED", _LIST_SCORE_DEBUG)
        # print("P Score: {} ".format(score_max))
        # print()

        return score_max

    # If a Ghost (Minimizer)
    else:
        score_min: Union[float, None] = None

        # _LIST_SCORE_DEBUG = []

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            # Agent selection (Select next agent for the next call)
            if index_agent >= game_state.getNumAgents() - 1:
                index_agent_new = 0
                depth_new = depth - 1  # *** DEPTH IS ONLY CHANGED WHEN ALL AGENTS HAVE MOVED
            else:
                index_agent_new = index_agent + 1
                depth_new = depth

            score_calculated = _dfs_recursive_minimax_v4_handler(game_state_new,
                                                                 depth_new,
                                                                 alpha,
                                                                 beta,
                                                                 function_evaluation,
                                                                 index_agent_new,
                                                                 alpha_beta_pruning,
                                                                 # str((depth, index_agent, action))
                                                                 )

            # _LIST_SCORE_DEBUG.append(score_calculated)

            if score_min is None or score_calculated < score_min:
                score_min = score_calculated

            if alpha_beta_pruning:

                if beta is None or score_calculated < beta:
                    beta = score_calculated

                r"""
                Notes:
                    Do not use <= on the minimizer, use < because <= will break test_cases\q3\6-tied-root.test 
                    because it will cut off a branch that may have a low score. Because the code
                    for the minimizer is the same for the maximizer, then the maximizer should have the same
                    logic as the minimizer.

                IMPORTANT NOTES:
                    YOU MUST USE
                        if beta is not None and alpha is not None and beta < alpha
                    AND NOT
                        if beta and alpha and beta < alpha
                    BECAUSE beta AND alpha MIGHT BE 0.0 WHICH WOULD RESULT IN False
                """
                if beta is not None and alpha is not None and beta < alpha:
                    # Cut off branch
                    break

        # print(f"G{index_agent} Depth", depth)
        # print(f"G{index_agent} MOVE", list_str_move_legal)
        # print(f"G{index_agent} CALCULATED", _LIST_SCORE_DEBUG)
        # print("G{} Score: {}".format(index_agent, score_min))
        # print()

        return score_min


# @callgraph(use_list_index_args=[1, 3], display_callable_name=False,)
def dfs_recursive_minimax_v4(game_state: GameState,
                             depth: int,
                             function_evaluation: callable,
                             index_agent: int = 0,
                             alpha_beta_pruning: bool = False,
                             ) -> Union[str, None]:
    """
    DFS Recursive Minimax algorithm correctly implemented (With alpha beta pruning support)

    Notes:
        This is the header for DFS Recursive Minimax algorithm, the reason why it's the header is because
        the root is pacman and its children should be its actions and you want to select the action based on the
        score. If this header was not hear like with the previous versions of this code, then you would need to
        look at children of the root again to know which move was associated with the score returned to the root.

        Basically, the code would look uglier if you didn't have this header.

    Reference:
        Algorithms Explained – minimax and alpha-beta pruning
            Reference:
                https://www.youtube.com/watch?v=l-hh51ncgDI
    """
    # List of legal movements ("North")
    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # List that contains tuples where each tuple has (score, action) as its elements
    list_pair: List[Tuple[float, str]] = []

    # alpha and beta for alpha beta pruning
    alpha: Union[None, float] = None
    beta: Union[None, float] = None

    for action in list_str_move_legal:

        game_state_new = game_state.generateSuccessor(index_agent, action)

        # Agent selection (Select next agent for the next call)
        index_agent_new = index_agent + 1

        score_calculated = _dfs_recursive_minimax_v4_handler(game_state_new,
                                                             depth,
                                                             alpha,
                                                             beta,
                                                             function_evaluation,
                                                             index_agent_new,
                                                             alpha_beta_pruning,
                                                             # str((depth, index_agent, action))
                                                             )

        if alpha_beta_pruning:

            if alpha is None or score_calculated > alpha:
                alpha = score_calculated

            r"""
            Notes:
                Do not use <= on the minimizer, use < because <= will break test_cases\q3\6-tied-root.test 
                because it will cut off a branch that may have a low score. Because the code
                for the minimizer is the same for the maximizer, then the maximizer should have the same
                logic as the minimizer.
                
            IMPORTANT NOTES:
                YOU MUST USE
                    if beta is not None and alpha is not None and beta < alpha
                AND NOT
                    if beta and alpha and beta < alpha
                BECAUSE beta AND alpha MIGHT BE 0.0 WHICH WOULD RESULT IN False
            """
            if beta is not None and alpha is not None and beta < alpha:
                # Cut off branch
                break

        list_pair.append((score_calculated, action))

        # print("-" * 50)

    # If there are pairs, select the action with the max cost and return the action.
    if list_pair:
        result = max(list_pair, key=lambda item: item[0])

        score_max = result[0]
        action_score_max = result[1]

        # print(list_pair)
        # print(action_score_max)
        # print("#" * 100)

        # create_callgraph(type_output="png")

        return action_score_max

    return None


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState) -> str:
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """
        
        Notes:
            In this function, we need to select a direction of movement that is the best to make.
            Basically, do a DFS Minimax, write that here pls.
            
            Recall that evaluationFunction does the score stuff related to direction and food
             
            self.evaluationFunction(gameState) returns a score (float)
            
            Use getAction From ReflexAgent as a reference too
        Run:
            Testing:
                python pacman.py -f -p MinimaxAgent -l trappedClassic -a depth=3
                py -3.6 pacman.py -f -p MinimaxAgent -l trappedClassic -a depth=3
                py -3.6 pacman.py -f -p MinimaxAgent -l trappedClassic -a depth=3  # Use this one
                
            Actual:
                python autograder.py -q q2
                python autograder.py -q q2 --no-graphics  
                
                py -3.6 autograder.py -q q2
                py -3.6 autograder.py -q q2 --no-graphics  # Use this one

        """

        ####################

        # print('gameState.getLegalActions(0)',
        #       type(gameState.getLegalActions(0)),
        #       gameState.getLegalActions(0))
        # print('gameState.generateSuccessor(0, "North")',
        #       type(gameState.generateSuccessor(0, "North")),
        #       gameState.generateSuccessor(0, "North"))
        # print('gameState.getNumAgents()',
        #       type(gameState.getNumAgents()),
        #       gameState.getNumAgents())
        # print('gameState.isWin()', type(gameState.isWin()), gameState.isWin())
        # print('gameState.isLose()', type(gameState.isLose()), gameState.isLose())
        #
        # print("#" * 100)

        ####################
        # """
        # V1
        #     Standard minimax that should technically work for 1 vs 1 (Wrong assumption, Read "IMPORTANT NOTES")
        #
        # Notes:
        #     This algorithm stacks multiple min calls on top of each other which causes a small value to always
        #     propagate back.
        #
        # IMPORTANT NOTES:
        #     BOTH "Notes" and the description for V1 are WRONG. The actual reason for why this code is wrong,
        #     is because of a mistake I made in the code. Look at V3 for the actual answer.
        #
        # Result:
        #     py -3.6 pacman.py -f -p MinimaxAgent -l trappedClassic -a depth=3
        #         Result:
        #             Pacman died! Score: -501
        #             Average Score: -501.0
        #             Scores:        -501.0
        #             Win Rate:      0/1 (0.00)
        #             Record:        Loss
        # """
        # result = dfs_recursive_minimax_v1(gameState, self.depth, self.evaluationFunction)
        #
        # score_final: float = result[0]
        #
        # agent_container_final: AgentContainer = result[1]
        #
        # # print("SCORE: {} PLAYER INDEX: {} PLAYER ACTION: {}".format(score_final,
        # #                                                             agent_container_final.index_agent,
        # #                                                             agent_container_final.action))
        # # create_callgraph(type_output="png")
        #
        # return agent_container_final.action

        ##########
        # """
        # V2
        #     Like v1 (standard minimax algorithm) but tries to compress all ghost agent actions together
        #     based on the assumption that all ghost actions must be made before a win or loss game state is reached.
        #
        # Notes:
        #     I generated the call graph and my assumption is wrong. The game can end even when not all ghost actions
        #     have been processed. This means you need to constantly check gameState if the game is a win or a loss.
        #
        # Results:
        #     Crashes because dfs_recursive_minimax_v2 runs all ghost agent actions and during that process the game
        #     may have ended via pacman win or loss (most likely loss because only ghosts move at this time).
        #     So any further gameState past the winning/losing gameState DOES NOT RETURN A SCORE which is needed
        #     to determine the action for pacman.
        #
        #     Basically, it crashes because None is returned when selecting the score and a score needs to be a number
        #
        # """
        #
        # result = dfs_recursive_minimax_v2(gameState, self.depth, self.evaluationFunction)
        #
        # score_final: float = result[0]
        #
        # agent_container_final: AgentContainer = result[1]
        #
        # # print("SCORE: {} PLAYER INDEX: {} PLAYER ACTION: {}".format(score_final,
        # #                                                             agent_container_final.index_agent,
        # #                                                             agent_container_final.action))
        # # create_callgraph(type_output="png")
        #
        # return agent_container_final.action

        ##########
        # r"""
        # V3
        #     DFS Recursive Minimax algorithm almost correctly implemented
        #
        # Notes:
        #     This is just V1 with a minor code fix that gets the correct answer
        #
        # Result:
        #     py -3.6 pacman.py -f -p MinimaxAgent -l trappedClassic -a depth=3
        #         Result:
        #             Pacman emerges victorious! Score: 532
        #             Average Score: 532.0
        #             Scores:        532.0
        #             Win Rate:      1/1 (1.00)
        #             Record:        Win
        #      py -3.6 autograder.py -q q2
        #         Result:
        #             *** PASS: test_cases\q2\0-eval-function-lose-states-1.test
        #             *** PASS: test_cases\q2\0-eval-function-lose-states-2.test
        #             *** PASS: test_cases\q2\0-eval-function-win-states-1.test
        #             *** PASS: test_cases\q2\0-eval-function-win-states-2.test
        #             *** PASS: test_cases\q2\0-lecture-6-tree.test
        #             *** FAIL: test_cases\q2\0-small-tree.test
        #             *** PASS: test_cases\q2\1-1-minmax.test
        #             *** FAIL: test_cases\q2\1-2-minmax.test
        #             *** FAIL: test_cases\q2\1-3-minmax.test
        #             *** FAIL: test_cases\q2\1-4-minmax.test
        #             *** FAIL: test_cases\q2\1-5-minmax.test
        #             *** FAIL: test_cases\q2\1-6-minmax.test
        #             *** FAIL: test_cases\q2\1-7-minmax.test
        #             *** FAIL: test_cases\q2\1-7-minmax.test
        #             *** PASS: test_cases\q2\1-8-minmax.test
        #             *** FAIL: test_cases\q2\2-1a-vary-depth.test
        #             *** FAIL: test_cases\q2\2-1b-vary-depth.test
        #             *** FAIL: test_cases\q2\2-2a-vary-depth.test
        #             *** FAIL: test_cases\q2\2-2b-vary-depth.test
        #             *** FAIL: test_cases\q2\2-3a-vary-depth.test
        #             *** FAIL: test_cases\q2\2-3b-vary-depth.test
        #             *** FAIL: test_cases\q2\2-4a-vary-depth.test
        #             *** FAIL: test_cases\q2\2-4b-vary-depth.test
        #             *** FAIL: test_cases\q2\2-one-ghost-3level.test
        #             *** PASS: test_cases\q2\3-one-ghost-4level.test
        #             *** PASS: test_cases\q2\4-two-ghosts-3level.test
        #             *** FAIL: test_cases\q2\5-two-ghosts-4level.test
        #             *** FAIL: test_cases\q2\6-tied-root.test
        #             *** FAIL: test_cases\q2\7-1a-check-depth-one-ghost.test
        #             *** PASS: test_cases\q2\7-1b-check-depth-one-ghost.test
        #             *** FAIL: test_cases\q2\7-1c-check-depth-one-ghost.test
        #             *** FAIL: test_cases\q2\7-2a-check-depth-two-ghosts.test
        #             *** PASS: test_cases\q2\7-2b-check-depth-two-ghosts.test
        #             *** FAIL: test_cases\q2\7-2c-check-depth-two-ghosts.test
        #             ...
        #             RecursionError: maximum recursion depth exceeded in comparison
        # """
        #
        # result = dfs_recursive_minimax_v3(gameState, self.depth, self.evaluationFunction)
        #
        # score_final: float = result[0]
        #
        # agent_container_final: AgentContainer = result[1]
        #
        # # print("SCORE: {} PLAYER INDEX: {} PLAYER ACTION: {}".format(score_final,
        # #                                                             agent_container_final.index_agent,
        # #                                                             agent_container_final.action))
        # # create_callgraph(type_output="png")
        #
        # return agent_container_final.action

        ##########
        r"""
        V4
            DFS Recursive Minimax algorithm correctly implemented (With alpha beta pruning support)

        Notes:
            This is the only version that I have that works correctly
            
        Result:
            py -3.6 autograder.py -q q2 --no-graphics
                Question q2
                ===========
                
                *** PASS: test_cases\q2\0-eval-function-lose-states-1.test
                *** PASS: test_cases\q2\0-eval-function-lose-states-2.test
                *** PASS: test_cases\q2\0-eval-function-win-states-1.test
                *** PASS: test_cases\q2\0-eval-function-win-states-2.test
                *** PASS: test_cases\q2\0-lecture-6-tree.test
                *** PASS: test_cases\q2\0-small-tree.test
                *** PASS: test_cases\q2\1-1-minmax.test
                *** PASS: test_cases\q2\1-2-minmax.test
                *** PASS: test_cases\q2\1-3-minmax.test
                *** PASS: test_cases\q2\1-4-minmax.test
                *** PASS: test_cases\q2\1-5-minmax.test
                *** PASS: test_cases\q2\1-6-minmax.test
                *** PASS: test_cases\q2\1-7-minmax.test
                *** PASS: test_cases\q2\1-8-minmax.test
                *** PASS: test_cases\q2\2-1a-vary-depth.test
                *** PASS: test_cases\q2\2-1b-vary-depth.test
                *** PASS: test_cases\q2\2-2a-vary-depth.test
                *** PASS: test_cases\q2\2-2b-vary-depth.test
                *** PASS: test_cases\q2\2-3a-vary-depth.test
                *** PASS: test_cases\q2\2-3b-vary-depth.test
                *** PASS: test_cases\q2\2-4a-vary-depth.test
                *** PASS: test_cases\q2\2-4b-vary-depth.test
                *** PASS: test_cases\q2\2-one-ghost-3level.test
                *** PASS: test_cases\q2\3-one-ghost-4level.test
                *** PASS: test_cases\q2\4-two-ghosts-3level.test
                *** PASS: test_cases\q2\5-two-ghosts-4level.test
                *** PASS: test_cases\q2\6-tied-root.test
                *** PASS: test_cases\q2\7-1a-check-depth-one-ghost.test
                *** PASS: test_cases\q2\7-1b-check-depth-one-ghost.test
                *** PASS: test_cases\q2\7-1c-check-depth-one-ghost.test
                *** PASS: test_cases\q2\7-2a-check-depth-two-ghosts.test
                *** PASS: test_cases\q2\7-2b-check-depth-two-ghosts.test
                *** PASS: test_cases\q2\7-2c-check-depth-two-ghosts.test
                *** Running MinimaxAgent on smallClassic 1 time(s).
                Pacman died! Score: 84
                Average Score: 84.0
                Scores:        84.0
                Win Rate:      0/1 (0.00)
                Record:        Loss
                *** Finished running MinimaxAgent on smallClassic after 0 seconds.
                *** Won 0 out of 1 games. Average score: 84.000000 ***
                *** PASS: test_cases\q2\8-pacman-game.test
                
                ### Question q2: 5/5 ###
                
                
                Finished at 12:56:39
                
                Provisional grades
                ==================
                Question q2: 5/5
                ------------------
                Total: 5/5
                
                Your grades are NOT yet registered.  To register your grades, make sure
                to follow your instructor's guidelines to receive credit on your project.
        """
        action = dfs_recursive_minimax_v4(gameState, self.depth, self.evaluationFunction)

        # create_callgraph(type_output="png")

        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        """
        
        Run:
            Testing:
                python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
                py -3.6 pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic  # Use this one
                
                py -3.6 autograder.py -q q3 --no-graphics  # Use this one

                                
            Actual:
                python autograder.py -q q3
                python autograder.py -q q3 --no-graphics  
                
                py -3.6 autograder.py -q q3
                py -3.6 autograder.py -q q3 --no-graphics  # Use this one
        """

        ####################

        r"""
        V1
            DFS Recursive Minimax algorithm correctly implemented (With alpha beta pruning support)
        
        Notes:
            It's just dfs_recursive_minimax_v4 with the kwarg alpha_beta_pruning=True
        
        Result:
            py -3.6 autograder.py -q q3 --no-graphics 
                Question q3
                ===========
                
                *** PASS: test_cases\q3\0-eval-function-lose-states-1.test
                *** PASS: test_cases\q3\0-eval-function-lose-states-2.test
                *** PASS: test_cases\q3\0-eval-function-win-states-1.test
                *** PASS: test_cases\q3\0-eval-function-win-states-2.test
                *** PASS: test_cases\q3\0-lecture-6-tree.test
                *** PASS: test_cases\q3\0-small-tree.test
                *** PASS: test_cases\q3\1-1-minmax.test
                *** PASS: test_cases\q3\1-2-minmax.test
                *** PASS: test_cases\q3\1-3-minmax.test
                *** PASS: test_cases\q3\1-4-minmax.test
                *** PASS: test_cases\q3\1-5-minmax.test
                *** PASS: test_cases\q3\1-6-minmax.test
                *** PASS: test_cases\q3\1-7-minmax.test
                *** PASS: test_cases\q3\1-8-minmax.test
                *** PASS: test_cases\q3\2-1a-vary-depth.test
                *** PASS: test_cases\q3\2-1b-vary-depth.test
                *** PASS: test_cases\q3\2-2a-vary-depth.test
                *** PASS: test_cases\q3\2-2b-vary-depth.test
                *** PASS: test_cases\q3\2-3a-vary-depth.test
                *** PASS: test_cases\q3\2-3b-vary-depth.test
                *** PASS: test_cases\q3\2-4a-vary-depth.test
                *** PASS: test_cases\q3\2-4b-vary-depth.test
                *** PASS: test_cases\q3\2-one-ghost-3level.test
                *** PASS: test_cases\q3\3-one-ghost-4level.test
                *** PASS: test_cases\q3\4-two-ghosts-3level.test
                *** PASS: test_cases\q3\5-two-ghosts-4level.test
                *** PASS: test_cases\q3\6-tied-root.test
                *** PASS: test_cases\q3\7-1a-check-depth-one-ghost.test
                *** PASS: test_cases\q3\7-1b-check-depth-one-ghost.test
                *** PASS: test_cases\q3\7-1c-check-depth-one-ghost.test
                *** PASS: test_cases\q3\7-2a-check-depth-two-ghosts.test
                *** PASS: test_cases\q3\7-2b-check-depth-two-ghosts.test
                *** PASS: test_cases\q3\7-2c-check-depth-two-ghosts.test
                *** Running AlphaBetaAgent on smallClassic 1 time(s).
                Pacman died! Score: 84
                Average Score: 84.0
                Scores:        84.0
                Win Rate:      0/1 (0.00)
                Record:        Loss
                *** Finished running AlphaBetaAgent on smallClassic after 0 seconds.
                *** Won 0 out of 1 games. Average score: 84.000000 ***
                *** PASS: test_cases\q3\8-pacman-game.test
                
                ### Question q3: 5/5 ###
                
                
                Finished at 12:54:45
                
                Provisional grades
                ==================
                Question q3: 5/5
                ------------------
                Total: 5/5
                
                Your grades are NOT yet registered.  To register your grades, make sure
                to follow your instructor's guidelines to receive credit on your project.
        """
        action = dfs_recursive_minimax_v4(gameState, self.depth, self.evaluationFunction, alpha_beta_pruning=True)

        return action


##############################################################################################################

def _dfs_recursive_expectimax_v1_handler(game_state: GameState,
                                         depth: int,
                                         function_evaluation: callable,
                                         index_agent: int = 0,
                                         ) -> float:
    """
    This is the actual DFS Recursive Expectimax algorithm's main body.

    Notes:
        This does not have probably for the summation part of the algorithm

    Reference:
        Lecture 7: Expectimax
            Notes:
                How to do it
            Reference:
                https://youtu.be/jaFRyzp7yWw?t=707
    """

    # Check if game is over via pacman dead or pacman got all food and survived
    if game_state.isWin() or game_state.isLose() or depth <= 0:
        score = function_evaluation(game_state)

        # Return the score
        return score

    # List of legal movements ("North")
    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # If Pacman (Maximizer)
    if index_agent == 0:

        score_max: Union[float, None] = None

        for action in list_str_move_legal:
            game_state_new = game_state.generateSuccessor(index_agent, action)

            # Agent selection (Select next agent for the next call)
            index_agent_new = index_agent + 1

            score_calculated = _dfs_recursive_expectimax_v1_handler(game_state_new,
                                                                    depth,
                                                                    function_evaluation,
                                                                    index_agent_new,
                                                                    )

            if score_max is None or score_calculated > score_max:
                score_max = score_calculated

        return score_max

    else:
        """
        If a Ghost (Avg of Summation or Avg of Summation of Expected values)
        Notes:
            In this example, there is no probability so no expected values
        """

        score_sum: Union[float, None] = 0

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            # Agent selection (Select next agent for the next call)
            if index_agent >= game_state.getNumAgents() - 1:
                index_agent_new = 0
                depth_new = depth - 1  # *** DEPTH IS ONLY CHANGED WHEN ALL AGENTS HAVE MOVED
            else:
                index_agent_new = index_agent + 1
                depth_new = depth

            score_calculated = _dfs_recursive_expectimax_v1_handler(game_state_new,
                                                                    depth_new,
                                                                    function_evaluation,
                                                                    index_agent_new,
                                                                    )

            score_sum += score_calculated

        score_avg = score_sum / len(list_str_move_legal)
        return score_avg


def dfs_recursive_expectimax_v1(game_state: GameState,
                                depth: int,
                                function_evaluation: callable,
                                index_agent: int = 0,
                                ) -> Union[str, None]:
    """
    DFS Recursive Expectimax algorithm algorithm's header

    Notes:
        The header is needed to make selection of the action easier

    Reference:
        Lecture 7: Expectimax
            Notes:
                How to do it
            Reference:
                https://youtu.be/jaFRyzp7yWw?t=707

    """
    # List of legal movements ("North")
    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # List that contains tuples where each tuple has (score, action) as its elements
    list_pair: List[Tuple[float, str]] = []

    for action in list_str_move_legal:
        game_state_new = game_state.generateSuccessor(index_agent, action)

        # Agent selection (Select next agent for the next call)
        index_agent_new = index_agent + 1

        score_calculated = _dfs_recursive_expectimax_v1_handler(game_state_new,
                                                                depth,
                                                                function_evaluation,
                                                                index_agent_new,
                                                                )

        list_pair.append((score_calculated, action))

    # If there are pairs, select the action with the max cost and return the action.
    if list_pair:
        result = max(list_pair, key=lambda item: item[0])

        # print(list_pair)
        score_max = result[0]
        action_score_max = result[1]

        return action_score_max

    return None


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        """
        Notes:
            Just take dfs_recursive_minimax_v4 and modify it by changing the the Minimizer to an
            Avg of the Summation of expected values
            
        Run:
            Testing:
                python autograder.py -q q4
                python autograder.py -q q4 --no-graphics  
                
                py -3.6 autograder.py -q q4
                py -3.6 autograder.py -q q4 --no-graphics  # Use this one
                                
            Actual:
                python autograder.py -q q4
                python autograder.py -q q4 --no-graphics  
                
                py -3.6 autograder.py -q q4
                py -3.6 autograder.py -q q4 --no-graphics  # Use this one
        """

        ####################

        r"""
        V1
            The correct expectimax algorithm based on the body of dfs_recursive_minimax_v4
        
        Notes:
            It's just a modified dfs_recursive_minimax_v4 to use only a Maximizer and a Avg of Summation Expected
            values
        
        Result:
            py -3.6 autograder.py -q q4 --no-graphics
                Question q4
                ===========
                
                *** PASS: test_cases\q4\0-eval-function-lose-states-1.test
                *** PASS: test_cases\q4\0-eval-function-lose-states-2.test
                *** PASS: test_cases\q4\0-eval-function-win-states-1.test
                *** PASS: test_cases\q4\0-eval-function-win-states-2.test
                *** PASS: test_cases\q4\0-expectimax1.test
                *** PASS: test_cases\q4\1-expectimax2.test
                *** PASS: test_cases\q4\2-one-ghost-3level.test
                *** PASS: test_cases\q4\3-one-ghost-4level.test
                *** PASS: test_cases\q4\4-two-ghosts-3level.test
                *** PASS: test_cases\q4\5-two-ghosts-4level.test
                *** PASS: test_cases\q4\6-1a-check-depth-one-ghost.test
                *** PASS: test_cases\q4\6-1b-check-depth-one-ghost.test
                *** PASS: test_cases\q4\6-1c-check-depth-one-ghost.test
                *** PASS: test_cases\q4\6-2a-check-depth-two-ghosts.test
                *** PASS: test_cases\q4\6-2b-check-depth-two-ghosts.test
                *** PASS: test_cases\q4\6-2c-check-depth-two-ghosts.test
                *** Running ExpectimaxAgent on smallClassic 1 time(s).
                Pacman died! Score: 84
                Average Score: 84.0
                Scores:        84.0
                Win Rate:      0/1 (0.00)
                Record:        Loss
                *** Finished running ExpectimaxAgent on smallClassic after 0 seconds.
                *** Won 0 out of 1 games. Average score: 84.000000 ***
                *** PASS: test_cases\q4\7-pacman-game.test
                
                ### Question q4: 5/5 ###
                
                
                Finished at 12:53:27
                
                Provisional grades
                ==================
                Question q4: 5/5
                ------------------
                Total: 5/5
                
                Your grades are NOT yet registered.  To register your grades, make sure
                to follow your instructor's guidelines to receive credit on your project.
        """
        result = dfs_recursive_expectimax_v1(gameState, self.depth, self.evaluationFunction)

        return result


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

    # print("currentGameState", type(currentGameState), currentGameState)
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
            Pacman emerges victorious! Score: 1171
            Pacman emerges victorious! Score: 1356
            Pacman emerges victorious! Score: 1361
            Pacman emerges victorious! Score: 1141
            Pacman emerges victorious! Score: 1366
            Pacman emerges victorious! Score: 1164
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

    result = evaluation_function_food_and_ghost(game_state_successor_pacman,
                                                evaluation_function_heuristic_cost_ucs_crude)

    return result


# Abbreviation
better = betterEvaluationFunction
