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
from abc import ABC
from abc import abstractmethod
from typing import Hashable
from typing import List
from typing import Tuple
from typing import Union

from common.graphics.graphics import Graphics
from pacman.agent import Agent


class SearchProblem(ABC):
    """
    This class outlines the structure of a search problem_multi_agent_tree, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def __init__(self):  # FIXME: THIS IS MISSING state_pacman

        self.graphics: Union[Graphics, None] = None

        self._expanded = None  # FIXME: NEED THIS

    def set_graphics(self, graphics: Graphics):
        self.graphics = graphics

    @abstractmethod
    def getStartState(self) -> Union[Tuple[int, int], Hashable]:
        """
        Returns the start state_pacman for the search problem_multi_agent_tree.
        """
        pass

    @abstractmethod
    def isGoalState(self, state) -> bool:
        """
          state_pacman: Search state_pacman

        Returns True if and only if the state_pacman is a valid goal state_pacman.
        """
        pass

    @abstractmethod
    def getSuccessors(self, state) -> List[Union[tuple, str, int]]:
        """
          state_pacman: Search state_pacman

        For a given state_pacman, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state_pacman, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        pass

    @abstractmethod
    def getCostOfActions(self, actions) -> int:
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        pass
