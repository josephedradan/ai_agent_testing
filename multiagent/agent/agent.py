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

from abc import ABC, abstractmethod
from typing import Union

from multiagent.graphicsUtils import GraphicsActual


class Agent(ABC):
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """

    def __init__(self, index:int =0):
        self.index = index


    # TODO IN THE FUTURE USE THIS I THINK
    # def __init__(self, index=0, graphics_actual: Union[GraphicsActual, None] = None):
    #     self.index = index
    #     self._graphics_actual = graphics_actual

    @abstractmethod
    def getAction(self, state: GameState):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        pass
