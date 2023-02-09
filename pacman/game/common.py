"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/1/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""

# class PlayerType(Enum):
#     PACMAN = auto()
#     GHOST = auto()
from typing import Callable
from typing import List
from typing import Tuple
from typing import Union

from common.action import Action
from pacman.agent import Agent
from pacman.game.player import Player

TYPE_REPRESENTATIVE = Union[Agent, Player]

TYPE_POSITION = Union[Tuple[int, ...]]

from pacman.agent.search_problem import SearchProblem

TYPE_HEURISTIC_FUNCTION = Callable[[Tuple[int, int], SearchProblem], float]


TYPE_SEARCH_FUNCTION = Callable[[SearchProblem, Union[TYPE_HEURISTIC_FUNCTION, None]],
                                List[Action]]
