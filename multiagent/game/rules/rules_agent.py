"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/27/2022

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

from abc import ABC
from abc import abstractmethod
from typing import List
from typing import TYPE_CHECKING
from typing import Union

from multiagent.game.directions import Action
from multiagent.game.directions import Directions

if TYPE_CHECKING:
    from multiagent.game.gamestate import GameState


class RulesAgent(ABC):

    @staticmethod
    @abstractmethod
    def getLegalActions(state: GameState, index_agent: Union[int, None] = None) -> List[Directions]:
        """
        Returns a list of possible actions.
        """
        pass

    @staticmethod
    @abstractmethod
    def applyAction(state: GameState, action: Action, index_agent: Union[int, None] = None):
        """
        Edits the state to reflect the results of the action.
        """
        pass
