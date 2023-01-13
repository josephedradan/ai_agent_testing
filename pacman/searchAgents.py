# searchAgents.py
# ---------------
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


"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running agent_pacman_.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python agent_pacman_.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the name_project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the name_project
description for details.

Good luck and happy searching!
"""

# import game
# import agent_pacman_
# import search
# import util
from pacman.agent import Agent
from pacman.game.directions import Directions


class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in agent_pacman_.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

# class SearchAgent(Agent):
#     """
#     This very general search agent finds a path using a supplied search
#     algorithm for a supplied search problem, then returns actions to follow that
#     path.
#
#     As a default, this agent runs DFS on a PositionSearchProblem to find
#     location (1,1)
#
#     Options for fn include:
#       depthFirstSearch or dfs
#       breadthFirstSearch or bfs
#
#
#     Note: You should NOT change any code in SearchAgent
#     """
#
#     def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
#         # Warning: some advanced Python magic is employed below to find the right functions and problems
#
#         # Get the search function from the test_case_object and heuristic
#         if fn not in dir(search):
#             raise AttributeError(fn + ' is not a search function in search.py.')
#         func = getattr(search, fn)
#         if 'heuristic' not in func.__code__.co_varnames:
#             print('[SearchAgent] using function ' + fn)
#             self.searchFunction = func
#         else:
#             if heuristic in globals().keys():
#                 heur = globals()[heuristic]
#             elif heuristic in dir(search):
#                 heur = getattr(search, heuristic)
#             else:
#                 raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
#             print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
#             # Note: this bit of Python trickery combines the search algorithm and the heuristic
#             self.searchFunction = lambda x: func(x, heuristic=heur)
#
#         # Get the search problem type from the test_case_object
#         if prob not in globals().keys() or not prob.endswith('Problem'):
#             raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
#         self.searchType = globals()[prob]
#         print('[SearchAgent] using problem type ' + prob)
#
#     def registerInitialState(self, state):
#         """
#         This is the first time that the agent sees the layout of the game
#         board. Here, we choose a path to the goal. In this phase, the agent
#         should compute the path to the goal and store it in a local variable.
#         All of the work is done in this method!
#
#         state: a GameState object (agent_pacman_.py)
#         """
#         if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
#         starttime = time.time()
#         problem = self.searchType(state)  # Makes a new search problem
#         self.actions = self.searchFunction(problem)  # Find a path
#         totalCost = problem.getCostOfActions(self.actions)
#         print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
#         if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)
#
#     def getAction(self, state):
#         """
#         Returns the next action in the path chosen earlier (in
#         registerInitialState).  Return Directions.STOP if there is no further
#         action to take.
#
#         state: a GameState object (agent_pacman_.py)
#         """
#         if 'actionIndex' not in dir(self):
#             self.actionIndex = 0
#
#         i = self.actionIndex
#         self.actionIndex += 1
#         if i < len(self.actions):
#             return self.actions[i]
#         else:
#             return Directions.STOP


# def manhattanHeuristic(position, problem, info={}):
#     "The Manhattan distance heuristic for a PositionSearchProblem"
#     xy1 = position
#     xy2 = problem.goal
#     return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
#
#
# def euclideanHeuristic(position, problem, info={}):
#     "The Euclidean distance heuristic for a PositionSearchProblem"
#     xy1 = position
#     xy2 = problem.goal
#     return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################


# class HashableGoal:
#     # Use less memory
#     __slots__ = ["position", "list_tuple_order_traveled"]
#
#     def __init__(self, position: Tuple[int, ...], list_tuple_order_traveled: List[Union[Tuple[int, ...], None]]):
#         """
#         Probably because all of the algorithms inside of search.py prevent you from moving into a position that you
#         already traversed, you can use an additional parameter to act similar to changing universes once you have
#         reached a goal.
#
#         Basically, you hash the position along side the length of the set that contains the goal positions.
#         When you reach a goal position, the set's length is changed because you remove that position from that set.
#         The removal of a goal position and the creation of the set is done before the creation of this object based
#         on the previous HashableGoal object's list_tuple_order_traveled.
#
#         """
#
#         self.position = position
#         self.list_tuple_order_traveled = list_tuple_order_traveled.copy()
#
#     def __hash__(self):
#         """
#         Hash the position along side the length of the set of goal positions that you haven't reached
#
#         Notes:
#             tuple (No Nones)
#                 with check in isGoalState -> Fail, Search nodes expanded: 149, cost of 26
#                 No check in isGoalState -> Success, Search nodes expanded: 283, cost of 29
#                 Can cause different paths to enter the same universe
#
#             len
#                 with check in isGoalState -> Fail, Search nodes expanded: 88, cost of 26,
#                 No check in isGoalState -> Success, Search nodes expanded: 105, cost of 31
#                 Can cause different paths to enter the same universe
#
#             frozenset
#                 with check in isGoalState -> Fail, Search nodes expanded: 149, cost of 26
#                 No check in isGoalState -> Success, Search nodes expanded: 283, cost of 29
#                 Can cause different paths to enter the same universe
#
#             tuple (With Nones) V1
#                 with check in isGoalState -> Fail, Search nodes expanded: 447, cost of 28
#                 No check in isGoalState -> Success, Search nodes expanded: 494, cost of 29
#                 Can probably not cause different paths to enter the same universe because the hash
#                 is based on the order of tuple corners visited and the tuple corner itself.
#
#              tuple (Just adding the position of a corner in a list of corners visited, then hashing
#              that list as a tuple)
#                 with check in isGoalState -> Fail, Search nodes expanded: 447, cost of 28
#                 No check in isGoalState -> Success, Search nodes expanded: 494, cost of 29
#                 Can probably not cause different paths to enter the same universe because the hash
#                 is based on the order of tuple corners visited and the tuple corner itself.
#
#         :return:
#         """
#         return hash((self.position, tuple(self.list_tuple_order_traveled)))
#
#     def __eq__(self, other):
#         if isinstance(other, HashableGoal):
#             return self.__hash__() == other.__hash__()
#         return False
#
#     # V1
#     # def is_done(self):
#     #     """
#     #     If set_position_remaining is empty,it means you reached all goal positions.
#     #
#     #     :return:
#     #     """
#     #     if isinstance(self.list_tuple_order_traveled[-1], Tuple):
#     #         return True
#     #     return False
