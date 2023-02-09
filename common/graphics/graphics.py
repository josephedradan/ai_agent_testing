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

from common.graphics.gui import GUI

if TYPE_CHECKING:
    from common.state import State
    from common.state_data_pacman import StateDataPacman


class Graphics(ABC):
    """
    Common class for graphics type stuff

    """

    def __init__(self,
                 gui: Union[GUI, None] = None,
                 time_frame: float = 0.0,
                 time_sleep: float = 0.0,
                 zoom: float = 1.0,
                 ):
        self.gui: GUI = gui
        self.time_frame: float = time_frame
        self.time_sleep: float = time_sleep
        self.zoom: float = zoom

    @abstractmethod
    def initialize(self, state: StateDataPacman, isBlue: bool = False): # FIXME: GENERALIZE THSI
        pass

    @abstractmethod
    def update(self, state: State): # FIXME: GENERALIZE THSI
        pass

    @abstractmethod
    def drawExpandedCells(self, cells):  # FIXME: GENERALIZE THSI
        pass