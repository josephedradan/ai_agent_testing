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
from __future__ import annotations

import time
from typing import Callable
from typing import List
from typing import TYPE_CHECKING
from typing import Type
from typing import Union

from pacman.agent import Agent
from pacman.agent.heuristic_function import foodHeuristic
from pacman.agent.heuristic_function import get_heuristic_function
from pacman.agent.search import search
from pacman.agent.search_problem import AnyFoodSearchProblem
from pacman.agent.search_problem import CornersProblem
from pacman.agent.search_problem import FoodSearchProblem
from pacman.agent.search_problem import SearchProblem
from pacman.agent.search_problem import get_subclass_search_problem
from pacman.agent.search_problem.agent_pacman__search_problem import cornersHeuristic
from pacman.agent.search_problem.search_problem_position import PositionSearchProblem
from pacman.game.directions import Action
from pacman.game.directions import Directions
from pacman.game.grid_pacman import GridPacman

if TYPE_CHECKING:
    from pacman.game.game_state import GameState


class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self,
                 fn: Callable = 'depth_first_search',
                 prob: Union[Type[SearchProblem], str] = 'PositionSearchProblem',
                 heuristic: Callable = 'nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the test_case_object and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)  # FIXME: CHANGE ME PLS TO THE DICT WAY

        print("func.__name__", func.__name__)  # TODO: PRINT STATEMTNS EHRE
        print("func.__code__.co_varnames", func.__code__.co_varnames)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:

            # if heuristic in globals().keys():
            #     heur = globals()[heuristic]
            # elif heuristic in dir(search):
            #     heur = getattr(search, heuristic)
            # else:
            #     raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            # print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))

            # TODO: JOSEPH CUSTOM RIGHT HERE
            heur = get_heuristic_function(heuristic)

            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        print("prob", prob)
        print("globals().keys()", globals().keys())
        # # Get the search problem type from the test_case_object
        # if prob not in globals().keys() or not prob.endswith('Problem'):
        #     raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        # self.searchType = globals()[prob]

        # TODO: JOSEPH CUSTOM HERE

        self.searchType: Type[SearchProblem] = get_subclass_search_problem(prob)

        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state: GameState):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (agent_pacman_.py)
        """

        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem: object = self.searchType(state)  # Makes a new search problem  # TODO: MAKE OBJECT FROM CLASS

        # TODO: APPRENTLY NOT ALL self.searchType are of type SearchProblem because of poor design of the original
        if isinstance(problem, SearchProblem):
            problem.set_graphics(self.get_graphics_pacman())

        # TODO: I THINK THIS IS A LIST OF Direction
        self.actions: List[Action] = self.searchFunction(problem)  # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (agent_pacman_.py)
        """
        if 'actionIndex' not in dir(self):
            self.actionIndex = 0

        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """

    def __init__(self):
        # FIXME: SHOULD CALL SUPER, BUT THE PARTIAL FUNCTION BELOW IS FUCKY
        self.searchFunction = search.uniform_cost_search
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)


class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """

    def __init__(self):
        # FIXME: SHOULD CALL SUPER, BUT THE PARTIAL FUNCTION BELOW IS FUCKY
        self.searchFunction = search.uniform_cost_search
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)


class AStarCornersAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"

    def __init__(self):
        # FIXME: SHOULD CALL SUPER, BUT THE PARTIAL FUNCTION BELOW IS FUCKY

        self.searchFunction = lambda prob: search.a_star_search(prob, cornersHeuristic)
        self.searchType = CornersProblem


class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"

    def __init__(self):
        # FIXME: SHOULD CALL SUPER, BUT THE PARTIAL FUNCTION BELOW IS FUCKY

        self.searchFunction = lambda prob: search.a_star_search(prob, foodHeuristic)
        self.searchType = FoodSearchProblem


class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"

    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.get_container_position_vector_successor(0, action)
        self.actionIndex = 0
        print('Path found with cost {}.'.format(len(self.actions)))

    def findPathToClosestDot(self, game_state: GameState) -> List[Action]:
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState

        # position_start: tuple = game_state.getPacmanPosition()
        # food: GridPacman = game_state.getFood()
        # walls: GridPacman = game_state.getWalls()
        problem: AnyFoodSearchProblem = AnyFoodSearchProblem(game_state)

        "*** YOUR CODE HERE ***"

        position_start: tuple
        food: GridPacman
        walls: GridPacman
        problem: AnyFoodSearchProblem

        # print(type(position_start))
        # print(position_start)
        # print(type(food))
        # print(food)
        # print(type(walls))
        # print(walls)
        # print(type(problem))
        # print()

        # Note that food is the same a foodGrid from problem 7 and foodGrid CHANGES OVER (foodHeuristic)
        # list_position_food_remaining = food.asList()

        ####################
        """
        V1
            "problem" has everything in it and you need to return a path which is the result
            of what the algorithms in search.py do.

        IMPORTANT NOTES:

            Cannot use foodHeuristic because it requires "problem" to be of type FoodSearchProblem.

            Cannot use manhattanHeuristic and euclideanHeuristic because they require "problem" to be of type
            PositionSearchProblem.

            Basically:
                Using "problem" of type FoodSearchProblem, you can use these heuristics:
                    foodHeuristic

                Using "problem" of type PositionSearchProblem, you can use these heuristics:
                    manhattanHeuristic
                    euclideanHeuristic

        Notes:
            Using search.aStarSearch defaults to UCS

        """
        return search.a_star_search(problem)
