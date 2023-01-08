"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/27/2022

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

if TYPE_CHECKING:
    from pacman.game.directions import Action
    from pacman.game.game_state import GameState


def evaluation_function_game_state_score(game_state: GameState, action: Action) -> float:
    return game_state.getScore()
