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

import random
from typing import List
from typing import TYPE_CHECKING
from typing import Tuple

from pacman.agent.agent_pacman import AgentPacman
from pacman.game.action_direction import Action
from pacman.game.action_direction import ActionDirection

if TYPE_CHECKING:
    from common.state import State
    from common.state_pacman import StatePacman

class AgentPacmanGreedy(AgentPacman):
    # TODO: FIX THIS JOSEPH THE SOLUTION IS SUBOPTIMAL
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getAction(self, state: State) -> Action:

        # Generate candidate actions
        legal: List[Action] = state.getLegalActions(self)

        if ActionDirection.STOP in legal:
            legal.remove(ActionDirection.STOP)

        successors: List[Tuple[State, Action]] = (
            [(state.generateSuccessor(self, action), action) for action in legal]
        )

        # print("-- successors", successors, type(successors))

        scored: List[Tuple[float, Action]] = (
            [(self.evaluation_function(self, _state, action), action) for _state, action in successors]
        )

        # print("scored", scored, type(scored))

        score_best: float = max(scored)[0]

        # print("score_best", score_best, type(score_best))

        list_action_best: List[Action] = [pair[1] for pair in scored if pair[0] == score_best]

        # print("list_action_best", list_action_best, type(list_action_best))
        # print()

        return random.choice(list_action_best)
