"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/24/2022

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
from multiagent.graphics.graphics import Graphics

if TYPE_CHECKING:
    from multiagent.game.gamestate import GameState


class Agent(ABC):
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, game_state): # inspects the starting game_state
    """

    def __init__(self, index: int):
        self.index = index

        self._graphics: Union[Graphics, None] = None

    # TODO IN THE FUTURE USE THIS I THINK
    # def __init__(self, index=0, graphics_actual: Union[GraphicsActual, None] = None):
    #     self.index = index
    #     self._graphics_actual = graphics_actual

    @abstractmethod
    def getAction(self, game_state: GameState) -> Action:
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        pass

    def set_graphics(self, graphics: Graphics):
        self._graphics = graphics

    def get_graphics(self) -> Graphics:
        return self._graphics