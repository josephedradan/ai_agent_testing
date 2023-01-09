"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/31/2022

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
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pacman.game.game_state import GameState
    from pacman.game.game_state_data import GameStateData


class GraphicsPacman(ABC):
    """
    Common class for graphics type stuff

    """

    # def __init__(self, display):



    @abstractmethod
    def initialize(self, state: GameStateData, isBlue: bool = False):
        pass

    @abstractmethod
    def update(self, state: GameState):
        pass
