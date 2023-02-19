"""
Date created: 2/1/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Contributors: 
    https://github.com/josephedradan

Reference:

"""

from typing import Callable
from typing import List
from typing import Tuple
from typing import Union

from common.action import Action
from pacman.agent import Agent
from pacman.game.player_pacman import PlayerPacman

TYPE_REPRESENTATIVE = Union[Agent, PlayerPacman]

from pacman.agent.search_problem import SearchProblem

TYPE_HEURISTIC_FUNCTION = Callable[[Tuple[int, int], SearchProblem], float]

TYPE_SEARCH_FUNCTION = Callable[[SearchProblem, Union[TYPE_HEURISTIC_FUNCTION, None]],
                                List[Action]]
