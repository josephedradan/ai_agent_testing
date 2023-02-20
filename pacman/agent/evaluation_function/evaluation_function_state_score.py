"""
Date created: 12/27/2022

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


if TYPE_CHECKING:
    from pacman.agent import Agent
    from common.state import State
    from pacman.game.actiondirection import Action


def evaluation_function_state_score(agent: Agent, state: State, action: Action) -> float:
    return state.getScore()
