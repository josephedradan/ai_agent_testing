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

import random
from typing import List
from typing import TYPE_CHECKING
from typing import Tuple

from multiagent.agent.agent_pacman import AgentPacman
from multiagent.game.directions import Action
from multiagent.game.directions import Directions

if TYPE_CHECKING:
    from multiagent.game.gamestate import GameState


class AgentPacmanGreedy(AgentPacman):
    # TODO: FIX THIS JOSEPH THE SOLUTION IS SUBOPTIMAL
    def __init__(self):
        super().__init__()

    def getAction(self, game_state: GameState) -> Action:

        # Generate candidate actions
        legal: List[Action] = game_state.getLegalPacmanActions()

        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        successors: List[Tuple[GameState, Action]] = (
            [(game_state.generateSuccessor(0, action), action) for action in legal]
        )

        print("successors", successors, type(successors))

        scored: List[Tuple[float, Action]] = (
            [(self.evaluation_function(_game_state, action), action) for _game_state, action in successors]
        )

        # print("scored", scored, type(scored))

        score_best: float = max(scored)[0]

        # print("score_best", score_best, type(score_best))

        list_action_best: List[Action] = [pair[1] for pair in scored if pair[0] == score_best]

        # print("list_action_best", list_action_best, type(list_action_best))
        # print()

        return random.choice(list_action_best)
