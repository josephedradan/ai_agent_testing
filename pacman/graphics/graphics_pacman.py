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
from typing import Union

from common.graphics.display import Display

if TYPE_CHECKING:
    from common.game_state import GameState
    from common.game_state_data import GameStateData


class GraphicsPacman(ABC):
    """
    Common class for graphics type stuff

    """

    def __init__(self,
                 display: Union[Display, None] = None,
                 time_frame: float = 0.0,
                 time_sleep: float = 0.0,
                 zoom: float = 1.0,
                 ):
        self.display: Display = display
        self.time_frame: float = time_frame
        self.time_sleep: float = time_sleep
        self.zoom: float = zoom

    @abstractmethod
    def initialize(self, state: GameStateData, isBlue: bool = False):
        pass

    @abstractmethod
    def update(self, state: GameState):
        pass
