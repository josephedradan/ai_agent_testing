"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/18/2023

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

from typing import TYPE_CHECKING

from pacman.agent import Agent
from pacman.game.directions import Directions

if TYPE_CHECKING:
    from common.state import State

class GoWestAgent(Agent):
    "An player that goes West until it can't."

    def getAction(self, state: State):
        "The player receives a State (defined in pacman.py)."
        if Directions.WEST in state.getLegalActions(self):
            return Directions.WEST
        else:
            return Directions.STOP
