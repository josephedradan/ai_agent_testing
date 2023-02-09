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

from pacman.game.common import TYPE_REPRESENTATIVE
from pacman.game.directions import Action
from pacman.game.directions import Directions

if TYPE_CHECKING:
    from pacman.game.common import TYPE_POSITION

    from common.state import State


class RulesAgent(ABC):

    @staticmethod
    @abstractmethod
    def getLegalActions(state: State, representative: TYPE_REPRESENTATIVE) -> List[Directions]:
        """
        Returns a list of possible actions.
        """
        pass

    @staticmethod
    @abstractmethod
    def applyAction(state: State, action: Action, representative: TYPE_REPRESENTATIVE):
        """
        Edits the state_pacman to reflect the results of the action.
        """
        pass
