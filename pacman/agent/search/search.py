# search.py
# ---------
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
from typing import Any
from typing import Callable
from typing import Hashable
from typing import List
from typing import Set
from typing import Tuple
from typing import Union

from pacman import util
from pacman.agent.heuristic_function import nullHeuristic
from pacman.agent.search_problem import SearchProblem
from pacman.game.directions import Directions


def tinyMazeSearch(problem) -> List[str]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def dfs_recursive_problem_main(problem: SearchProblem) -> List[str]:
    """
    Main function for the dfs recursive call search given a SearchProblem object.

    :param problem:
    :return:
    """

    # ----- Utility Setup -----

    # List of all directions as strings to travel to
    list_str_direction_answer: List[str] = []

    # Set of tuples positions already traveled to
    set_tuple_position_traveled: Set[Tuple[int, int]] = set()

    #####

    # Recursive DFS to travel to all Successors
    def dfs_recursive_successor(list_successor_current: List[Tuple[Tuple[int, int], str, int]]) -> Union[None, bool]:
        """
        Recursive DFS on the list_successor_current to travel to all the tuple positions given by
        problem.getSuccessors()

        Notes:
            Does a DFS search using recursive calls

        Important Notes:
            Can reach maximum recursion depth

        :param list_successor_current: [((int, int), "Direction", step_cost), ...]
        :return: None or bool

        """
        nonlocal list_str_direction_answer  # Make it clear that we are using a nonlocal var
        nonlocal set_tuple_position_traveled  # Make it clear that we are using a nonlocal var

        # Type hinting so you can understand
        i: Tuple[Tuple[int, int], str, int]

        # Loop over the successors
        for i in list_successor_current:

            # Current position tuple
            tuple_position_current: Tuple[int, int] = i[0]

            # Current direction string
            str_direction_current: str = i[1]

            # Current Step cost
            cost_step_current: int = i[2]

            # Check if current position tuple has not been traveled to already
            if tuple_position_current not in set_tuple_position_traveled:

                # Get list of new successors based on current position tuple
                list_successor_new = problem.getSuccessors(tuple_position_current)

                # Append current direction string to list of the string directions
                list_str_direction_answer.append(str_direction_current)

                # Add current position tuple to set of traveled tuple positions
                set_tuple_position_traveled.add(tuple_position_current)

                # If current position tuple has reached the goal
                if problem.isGoalState(tuple_position_current):
                    return True

                # Recursive call using the new list of successors
                result = dfs_recursive_successor(list_successor_new)

                # If the result of the recursive call is True then get out of recursive call
                if result is True:
                    return result

                # If the added str_direction_current did not lead to the correct path, then pop it
                list_str_direction_answer.pop()

    # ----- Initialization -----

    # Get first position tuple
    tuple_position_first: Tuple[int, int] = problem.getStartState()

    # Add the first position tuple to tuple positions traveled
    set_tuple_position_traveled.add(tuple_position_first)

    # Initial recursive call
    dfs_recursive_successor(problem.getSuccessors(tuple_position_first))

    return list_str_direction_answer


def dfs_iterative_problem_main(problem: SearchProblem) -> List[str]:
    """
    Main function for the dfs iterative search given a SearchProblem object.

    Notes:
        Does a DFS search using a loop.

        Mimics DFS search using recursive calls.

    :param problem:
    :return:
    """

    # ----- Utility Setup -----

    # Set of tuples positions already traveled to
    set_tuple_position_traveled: Set[Tuple[int, int]] = set()

    # List of all directions as strings to travel to
    list_str_direction_answer: List[str] = []

    # ----- Memory Utility Setup (Equivalent to a Stack frame) -----

    # List containing the result of problem.getSuccessors calls (Mimics stack frame memory)
    list_list_successor_stack_frame: List[List[Tuple[Tuple[int, int], str, int]]] = []

    # Stack containing tuple position objects (Mimics stack frame memory)
    stack_tuple_position_stack_frame: util.Stack[Tuple[int, int]] = util.Stack()

    # ----- Initialization -----

    # Get first position tuple
    tuple_position_first: Tuple[int, int] = problem.getStartState()

    # Append the successors of the first position tuple to this stack frame
    list_list_successor_stack_frame.append(problem.getSuccessors(tuple_position_first))

    # Push the first position tuple to the stack of tuple positions
    stack_tuple_position_stack_frame.push(tuple_position_first)

    # Main loop that does the equivalent of a dfs recursive call algorithm
    while True:

        # Get List of successors based on the last list in the list of list of successors
        list_successor_current = list_list_successor_stack_frame[-1]

        # If the list of successors is empty then go back to the previous stack frame (backtrack equivalent)
        if len(list_successor_current) == 0:
            list_list_successor_stack_frame.pop()
            stack_tuple_position_stack_frame.pop()
            list_str_direction_answer.pop()
            continue

        # Get current successor
        successor_current = list_successor_current.pop()

        # Current tuple position
        tuple_position_current: Tuple[int, int] = successor_current[0]

        # Current direction string
        str_direction_current: str = successor_current[1]

        # Check if current position tuple has not been traveled to already
        if tuple_position_current in set_tuple_position_traveled:
            # Skip current position tuple
            continue

        # Add current position tuple to set of traveled tuple positions
        set_tuple_position_traveled.add(tuple_position_current)

        # Get list of new successors based on current position tuple
        list_successor_new: List[Tuple[Tuple[int, int], str, int]] = problem.getSuccessors(tuple_position_current)

        # ----- Stack frame related stuff -----

        # Append the new list of successors to the list of list of successors
        list_list_successor_stack_frame.append(list_successor_new)

        # Push the current position tuple to the stack of position tuples
        stack_tuple_position_stack_frame.push(tuple_position_current)

        # Append current direction string to list of the string directions
        list_str_direction_answer.append(str_direction_current)

        #####

        # If current position tuple has reached the goal
        if problem.isGoalState(tuple_position_current):
            # Get out the loop
            break

        # ----- Debugging stuff -----
        # print(list_successor_current)
        # print(tuple_position_current)
        # print(list_str_direction_answer)
        # print()

    return list_str_direction_answer


class Container:
    # To get low memory usage
    __slots__ = ["successor", "container_parent", "position", "direction", "cost", "cost_accumulated",
                 "cost_accumulated_plus_heuristic_result", "cost_heuristic"]

    def __init__(self,
                 successor: Tuple[Union[Tuple, Hashable], Union[str, None], float],
                 container_parent: Union[Any, None] = None):
        """
        A Container object contains the successor given and its parent Container.
        This object is used to keep track of the child successor's parent successor.

        Takes in a successor (tuple) and a Container of the previous successor.

        :param successor: A tuple containing the position tuple, direction, and step cost
        :param container_parent: Container object that is the parent of the given successor
        """
        self.successor: Tuple[Union[Tuple, Hashable], Union[str, None], float] = successor
        self.container_parent: Union[Container, None] = container_parent

        self.position: Union[Tuple, Hashable] = successor[0]
        self.direction: Union[str, None] = successor[1]
        self.cost: float = successor[2]

        # Accumulated cost of this container is based on the previous container's accumulated cost
        self.cost_accumulated: float = self.cost + (
            self.container_parent.cost_accumulated if self.container_parent else 0)

        # Cost from the heuristic
        self.cost_heuristic: float = 0

    def __hash__(self):
        """
        Hash position because it's easy
        :return:
        """
        return hash(self.position)

        # return hash((self.position, self.direction))

    def __eq__(self, other):
        """
        Equality override

        :param other:
        :return:
        """
        if isinstance(other, type(self)):
            return self.__hash__() == other.__hash__()
        return False

    def __str__(self) -> str:
        """
        String representation of object
        :return:
        """
        return f"{self.position}"

    def set_cost_heuristic(self, value: float) -> None:
        self.cost_heuristic = value

    def get_cost_accumulated_plus_heuristic_result(self) -> float:
        return self.cost_accumulated + self.cost_heuristic

    def get_path(self) -> List[str]:
        """
        Get path to self.position by repeating the process of getting the container_parent and getting its direction
        and adding it into a list.

        Once all the list has been constructed, reverse that list because the list was constructed by going backwards
        to the source.

        :return:
        """

        # List of directions
        list_str_direction_answer: List[str] = []

        # Current container object
        container_current: Container = self

        # Loop to append current's direction and replace current container.
        while container_current.container_parent is not None:
            list_str_direction_answer.append(container_current.direction)
            container_current = container_current.container_parent

        list_str_direction_answer.reverse()  # Fastest reverse other than slicing with -1

        return list_str_direction_answer


def generic_search_algorithm_base(problem: SearchProblem,
                                  data_structure_from_util: Callable,
                                  args_for_data_structure_from_util=None) -> List[str]:
    """
    Generic search algorithm that uses the given data structure from the util file as the main data structure

    :param problem: ( ͡° ͜ʖ ͡°)
    :param data_structure_from_util: a data structure
    :param args_for_data_structure_from_util: args for initializing data_structure_from_util
    :return:
    """
    # ----- Utility Setup -----

    # Initialize the data structure
    if args_for_data_structure_from_util:
        # If the data structure has an init with arguments
        data_structure_from_util_object: Union[
            util.Stack,
            util.Queue,
            util.PriorityQueue,
            util.PriorityQueueWithFunction] = data_structure_from_util(*args_for_data_structure_from_util)
    else:
        # If the data structure does not have an init with arguments
        data_structure_from_util_object: Union[
            util.Stack,
            util.Queue,
            util.PriorityQueue,
            util.PriorityQueueWithFunction] = data_structure_from_util()

    # Set of tuples positions already traveled to
    set_container_traveled: Set[Container] = set()

    # # List of all directions as strings to travel to
    list_str_direction_answer: List[str] = []

    # ----- Initialization -----

    # Get first position tuple
    tuple_position_first: Hashable = problem.getStartState()

    # Create the first container object
    container_first = Container((tuple_position_first, None, 1))

    # Push the first container to the stack
    if type(data_structure_from_util_object) == util.PriorityQueue:
        data_structure_from_util_object.push(container_first, container_first.cost)
    else:
        data_structure_from_util_object.push(container_first)

    # Loop while the stack is not empty
    while not data_structure_from_util_object.isEmpty():

        # Get the first container
        container_current: Container = data_structure_from_util_object.pop()

        # print(container_current)

        # print("\t", container_current)

        # Check if the container has been traveled to already
        if container_current in set_container_traveled:
            continue

        # Check if the container's position is the goal
        if problem.isGoalState(container_current.position):
            # Hack 1
            # if type(problem).__name__ == "CornersProblem":
            #     # for i in container_current.get_path():
            #     #     print(i)
            #     list_str_direction_answer.extend(container_current.get_path())
            #
            #     while not data_structure_from_util_object.isEmpty():
            #         data_structure_from_util_object.pop()
            #
            #     set_container_traveled = set()
            #
            #     container_current.container_parent = None
            #
            #     # print(problem.getSuccessors(container_current.position))
            #     # print(container_current)
            #     # print()
            #     if problem.is_goal_state_all():
            #         break
            # else:
            #     # Assign the answer and leave the while loop
            #     list_str_direction_answer = container_current.get_path()
            #     break

            # Assign the answer and leave the while loop
            list_str_direction_answer = container_current.get_path()
            break

        # Add the container to the set of containers traveled to
        set_container_traveled.add(container_current)

        # Make the list of successors
        list_successor = problem.getSuccessors(container_current.position)

        # Loop over list of successors and make them into containers and push them into the stack
        for successor in list_successor:
            container_new = Container(successor, container_current)

            if type(data_structure_from_util_object) == util.PriorityQueue:
                data_structure_from_util_object.push(container_new, container_new.cost_accumulated)
            else:
                data_structure_from_util_object.push(container_new)

    return list_str_direction_answer


def depth_first_search(problem: SearchProblem, heuristic: Callable = nullHeuristic) -> List[str]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    # print("Start:", problem.getStartState())  # (int, int) Is a Position
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    # print("Problem:", problem)  # some object who cares
    # print("Position:", problem.getStartState())  # (int, int) -> Position
    # print()

    # Version 1 (DFS Recursive)
    # solution: List[string_given] = dfs_recursive_problem_main(problem)

    # Version 2 (DFS Iterative that mimics DFS Recursive)
    # solution: List[string_given] = dfs_iterative_problem_main(problem)

    # Version 3 (Generic Iterative)
    solution: List[str] = generic_search_algorithm_base(problem, util.Stack)

    return solution


def breadth_first_search(problem: SearchProblem, heuristic: Callable = nullHeuristic) -> List[str]:
    """
    Search the shallowest nodes in the search tree first.

    """

    # Just swap out the util.Stack callable with a util.Queue callable
    solution: List[str] = generic_search_algorithm_base(problem, util.Queue)

    return solution


def uniform_cost_search(problem: SearchProblem, heuristic: Callable = nullHeuristic) -> List[str]:
    """
    Search the node of least total cost first.

    """


    """
    
    Reference:
        Dijkstra's Algorithm - Computerphile
            Reference:
                https://www.youtube.com/watch?v=GazC3A4OQTE&t=346s
                
        Uniform Cost Search
            Reference:
                https://www.youtube.com/watch?v=dRMvK76xQJI
    """

    # Just swap out the util.Queue callable with a util.PriorityQueue callable
    solution: List[str] = generic_search_algorithm_base(problem, util.PriorityQueue)

    return solution


def a_star_search(problem: SearchProblem, heuristic: Callable = nullHeuristic) -> List[str]:
    """
    Search the node that has the lowest combined cost and heuristic first.

    """

    "*** YOUR CODE HERE ***"

    def priority_function(container: Container) -> float:
        """
        Because I hard coded the push method for a util.PriorityQueue object to use a container object's
        .cost_accumulated instance variable for it's "priorty" argument inside of "generic_search_algorithm_base"
        function, the only other way to modify the "priority" argument is to use a custom priority function with a
        util.PriorityQueueWithFunction object.

        Basically, this function is a wrapper over a container object to use its .cost_accumulated instance variable
        and adds that value with the result of the given heuristic function then returns this new value.


        :param container: A Container object
        :return:
        """
        nonlocal problem  # Make it clear that we are using a nonlocal var
        nonlocal heuristic  # Make it clear that we are using a nonlocal var

        """
        Give the heuristic function the container's position and the problem object to get the heuristic 
        algorithm's distance to the goal
        """
        heuristic_result = heuristic(container.position, problem)

        # Add the container's cost_accumulated with the heuristic_result to get that A* distance result thingy
        container.set_cost_heuristic(heuristic_result)
        return container.get_cost_accumulated_plus_heuristic_result()

    """
    Run the generic search algorithm with a custom priority queue which uses my priority function along with the 
    util.PriorityQueueWithFunction callable because that's the only one that supports a custom priority function
    """
    solution: List[str] = generic_search_algorithm_base(
        problem,
        util.PriorityQueueWithFunction,
        args_for_data_structure_from_util=(priority_function,)
    )

    return solution


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
