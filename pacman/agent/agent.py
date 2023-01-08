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

from pacman.game.directions import Action

if TYPE_CHECKING:
    from pacman.game.gamestate import GameState
    from pacman.graphics.graphics_pacman import GraphicsPacman


class Agent(ABC):
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, game_state): # inspects the starting game_state
    """

    def __init__(self, index: int, **kwargs):
        self.index = index

        if kwargs:
            raise Exception("ADDITIONAL KWARGS FOUND FIX THIS SHIT JOSEPH: {}".format(kwargs.items()))

        self._graphics: Union[GraphicsPacman, None] = None

    # TODO IN THE FUTURE USE THIS I THINK
    # def __init__(self, index=0, graphics_actual: Union[Display, None] = None):
    #     self.index = index
    #     self._graphics_actual = graphics_actual

    @abstractmethod
    def getAction(self, game_state: GameState) -> Action:
        """
        The Agent will receive a GameState (from either {agent_pacman_, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        pass

    def set_graphics(self, graphics: GraphicsPacman):
        self._graphics = graphics

    def get_graphics(self) -> GraphicsPacman:
        return self._graphics