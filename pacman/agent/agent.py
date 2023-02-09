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
from pprint import pprint
from typing import TYPE_CHECKING
from typing import Union

from common.graphics.gui import GUI
from common.graphics.gui_tkinter import GUITkinter
from pacman.game.directions import Action

if TYPE_CHECKING:
    from common.state import State
    from common.graphics.graphics import Graphics


class Agent(ABC):
    """
    An player must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state_pacman: State): # inspects the starting state_pacman
    """

    def __init_subclass__(cls, **kwargs):
        print("THINGY", cls)

    def __init__(self,
                 graphics: Union[Graphics, None] = None,
                 gui: Union[GUI, None] = None,
                 **kwargs,
                 ):

        self.graphics: Union[Graphics, None] = graphics

        if gui:
            self.gui: Union[GUI, None] = gui
        elif self.graphics:
            self.gui: Union[GUI, None] = self.graphics.gui


        # TODO: JOSEPH COMMENT JOSEPH JUMP
        # print("GRAPHICS")
        # print(self.graphics)
        # print("ADDITIONAL KWARGS START")
        # pprint(kwargs)
        # print("ADDITIONAL KWARGS END")

        # if kwargs or args:
        #     raise Exception("ADDITIONAL KWARGS FOUND FIX THIS SHIT JOSEPH: {}".format(kwargs.items()))

    # TODO IN THE FUTURE USE THIS I THINK
    # def __init__(self, index=0, graphics_actual: Union[Display, None] = None):
    #     self.index = index
    #     self._graphics_actual = graphics_actual

    @abstractmethod
    def getAction(self, state: State) -> Action:
        """
        The Agent will receive a State (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        pass

    # def set_graphics(self, graphics_pacman: Graphics):
    #     self.graphics = graphics_pacman
    #
    # def get_graphics(self) -> Graphics:
    #     return self.graphics

    def registerInitialState(self, state: State):
        """
        Hidden function used by test cases and stuff, use it if you know what you are doing

        """
        pass
