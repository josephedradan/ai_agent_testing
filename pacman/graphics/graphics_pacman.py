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
    from pacman.game.gamestate import GameState


class GraphicsPacman(ABC):
    """
    Common class for graphics type stuff

    """

    @abstractmethod
    def initialize(self, state: GameState, isBlue: bool = False):
        pass

    @abstractmethod
    def update(self, state: GameState):
        pass
