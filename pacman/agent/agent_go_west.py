"""
Date created: 1/18/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Contributors:
    https://github.com/josephedradan

Reference:

"""
from __future__ import annotations

from typing import TYPE_CHECKING

from pacman.agent import Agent
from pacman.game.action_direction import ActionDirection

if TYPE_CHECKING:
    from common.state import State


class AgentGoWest(Agent):
    "An player that goes West until it can't."

    def getAction(self, state: State):
        "The player receives a State (defined in pacman.py)."
        if ActionDirection.WEST in state.getLegalActions(self):
            return ActionDirection.WEST
        else:
            return ActionDirection.STOP
