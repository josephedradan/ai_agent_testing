# keyboardAgents.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from __future__ import annotations

import random
from typing import TYPE_CHECKING
from typing import Union

from pacman.agent.agent import Agent
from pacman.game.actiondirection import Action
from pacman.game.actiondirection import ActionDirection
from common.graphics.gui import GUI
from common.graphics.gui_tkinter import GUITkinter

if TYPE_CHECKING:
    from common.state import State


class AgentKeyboard(Agent):
    """
    An player controlled by the keyboard.
    """
    # NOTE: Arrow keys also work.
    WEST_KEY = 'a'
    EAST_KEY = 'd'
    NORTH_KEY = 'w'
    SOUTH_KEY = 's'
    STOP_KEY = 'q'

    def __init__(self, **kwargs):
        super(AgentKeyboard, self).__init__(**kwargs)

        self.lastMove = ActionDirection.STOP
        self.keys = []

        ###
        # TODO JOSEPH SPEICAL

    # FIXME: GHETTO SOLUTIOn
    def set_gui(self, gui: GUI):
        self.gui = gui

    def getAction(self, state: State) -> Action:
        # from graphicsUtils import get_keys_waiting
        # from graphicsUtils import get_keys_pressed
        #
        # from multiagent import graphicsUtils
        # print(f"getAction {graphicsUtils._root_window=}")

        # TODO: THIS IS CRASHABLE JOSEPH
        keys = self.gui.get_keys_waiting() + self.gui.get_keys_pressed()

        if keys != []:
            self.keys = keys

        legal = state.getLegalActions(self)
        move = self.getMove(legal)

        if move == ActionDirection.STOP:
            # Try to move in the same _direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and ActionDirection.STOP in legal:
            move = ActionDirection.STOP

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move

    def getMove(self, legal):
        move = ActionDirection.STOP
        if (self.WEST_KEY in self.keys or 'Left' in self.keys) and ActionDirection.WEST in legal:
            move = ActionDirection.WEST
        if (self.EAST_KEY in self.keys or 'Right' in self.keys) and ActionDirection.EAST in legal:
            move = ActionDirection.EAST
        if (self.NORTH_KEY in self.keys or 'Up' in self.keys) and ActionDirection.NORTH in legal:
            move = ActionDirection.NORTH
        if (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and ActionDirection.SOUTH in legal:
            move = ActionDirection.SOUTH
        return move


class AgentKeyboard2(AgentKeyboard):
    """
    A second player controlled by the keyboard.
    """
    # NOTE: Arrow keys also work.
    WEST_KEY = 'j'
    EAST_KEY = "l"
    NORTH_KEY = 'i'
    SOUTH_KEY = 'k'
    STOP_KEY = 'u'

    def getMove(self, legal):
        move = ActionDirection.STOP
        if (self.WEST_KEY in self.keys) and ActionDirection.WEST in legal:
            move = ActionDirection.WEST
        if (self.EAST_KEY in self.keys) and ActionDirection.EAST in legal:
            move = ActionDirection.EAST
        if (self.NORTH_KEY in self.keys) and ActionDirection.NORTH in legal:
            move = ActionDirection.NORTH
        if (self.SOUTH_KEY in self.keys) and ActionDirection.SOUTH in legal:
            move = ActionDirection.SOUTH
        return move
