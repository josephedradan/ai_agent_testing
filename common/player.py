"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/11/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:
    python Generics (intermediate) anthony explains #430
        Notes:
        Reference:
            https://www.youtube.com/watch?v=LcfxUU1A-RQ

"""
from abc import ABC
from typing import Generic
from typing import TYPE_CHECKING
from typing import TypeVar

from common.graphics.graphics import Graphics

from pacman.agent import Agent
if TYPE_CHECKING:
    pass

T_GUI = TypeVar('T_GUI', bound=Graphics)
T_Graphics = TypeVar('T_Graphics', bound=Graphics)


class Player(ABC, Generic[T_GUI, T_Graphics]):
    gui: T_GUI
    graphics: T_Graphics
    agent: Agent

    def __init__(self, gui: T_GUI, graphics: T_Graphics, agent: Agent):
        self.gui = gui
        self.graphics = graphics

        self.agent = agent

    def get_agent(self) -> Agent:
        return self.agent

    def get_gui(self) -> T_GUI:
        return self.gui

    def get_graphics(self) -> T_Graphics:
        return self.graphics

    def __hash__(self):
        """
        Use the agent's hash because it is unique and this object is just a wrapper over it
        """
        return self.agent.__hash__()

    def __eq__(self, other):
        return self.agent.__eq__(other)

    def __repr__(self):
        return "({} {})".format(type(self).__name__, type(self.agent).__name__)

    def __str__(self):
        return self.__repr__()