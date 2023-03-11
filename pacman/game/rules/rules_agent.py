"""
Date created: 12/27/2022

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

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import List
from typing import TYPE_CHECKING

from pacman.game.handler_action_direction import HandlerActionDirection

if TYPE_CHECKING:
    from common.state_pacman import StatePacman
    from pacman.game.player_pacman import PlayerPacman
    from pacman.game.action_direction import ActionDirection
    from pacman.game.action_direction import Action


class RulesPacman(ABC):

    @staticmethod
    @abstractmethod
    def getLegalActions(state_pacman: StatePacman, player_pacman: PlayerPacman) -> List[ActionDirection]:
        """
        Returns a list of possible actions.
        """
        pass

        container_position_direction = state_pacman.get_container_state_GHOST(
            player_pacman.get_agent()).get_container_position_direction()

        return HandlerActionDirection.get_list_action_direction_possible(
            container_position_direction,
            state_pacman.state_data.layout_pacman.walls
        )

    @staticmethod
    @abstractmethod
    def applyAction(state_pacman: StatePacman, action: Action, player_pacman: PlayerPacman):
        """
        Edits the state to reflect the results of the action.
        """
        pass
