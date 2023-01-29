"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/12/2023

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

import json
import random
# from multiagent.agent.agent import Agent
# from multiagent.agent.agent_ghost_directional import AgentGhostDirectional
# from multiagent._test_case import TestCase
# from multiagent.agent import *
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from pacman.agent import Agent
from pacman.game.directions import Action
from common.game_state import GameState

TYPE_TUPLE_GAME_STATE__ACTION_WRONG__ACTION_CORRECT = Tuple[GameState, Action, Action]


class GradingAgent(Agent):
    """
    Takes in an agent,
        Uses an agent's
            getAction
            registerInitialState
        and
            uses answers from a .solution file via
                list_list_list_action__value_optimal
                list_list_action_alt_depth
                list_list_action_partial_play_bug
            to check if agent's
                getAction
            is correct

    """

    @classmethod
    def from_dict(cls, seed, agent_to_be_tested, dict_file_solution: Dict[str, Any]):

        list_list_list_action__value_optimal = (
            [json.loads(x) for x in dict_file_solution['optimalActions'].split('\n')]
        )

        list_list_action_alt_depth = (
            [json.loads(x) for x in dict_file_solution['altDepthActions'].split('\n')]
        )

        list_list_action_partial_play_bug = (
            [json.loads(x) for x in dict_file_solution['partialPlyBugActions'].split('\n')]
        )

        return cls(
            seed,
            agent_to_be_tested,
            list_list_list_action__value_optimal,
            list_list_action_alt_depth,
            list_list_action_partial_play_bug
        )

    def __init__(self,
                 seed: int,
                 agent_to_be_tested: Agent,
                 list_list_list_action__value_optimal: List[List[List[List[Action], int]]],
                 list_list_action_alt_depth: List[List[List[Action]]],
                 list_list_action_partial_play_bug: List[List[List[Action]]]
                 ):

        # save student agent and actions of reference agents
        self.agent_to_be_tested: Agent = agent_to_be_tested

        ##########

        ##########

        # Notes: Should come from reading a file
        self.list_list_list_list_action__value_optimal: List[List[List[List[Action], int]]] = (
            list_list_list_action__value_optimal
        )

        # Notes: Should come from reading a file
        self.list_list_list_action_alt_depth: List[List[List[Action]]] = list_list_action_alt_depth

        # Notes: Should come from reading a file
        self.list_list_list_action_partial_play_bug: List[List[List[Action]]] = list_list_action_partial_play_bug

        # create fields for storing specific wrong actions
        self.list_tuple_game_state__action_from_agent_to_be_tested__action_optimal: List[
            TYPE_TUPLE_GAME_STATE__ACTION_WRONG__ACTION_CORRECT] = []

        self.amount_wrong_states_explored: int = 0

        # boolean vectors represent types of implementation the student could have
        self.list_bool_action_consistent_with_optimal: List[bool] = (
            [True for i in range(len(list_list_list_action__value_optimal[0]))]
        )
        self.list_bool_action_consistent_with_alternative_depth: List[bool] = (
            [True for i in range(len(list_list_action_alt_depth[0]))]
        )
        self.list_bool_action_consistent_with_partial_play_bug: List[bool] = (
            [True for i in range(len(list_list_action_partial_play_bug[0]))]
        )

        # keep track of elapsed moves
        self._count_action_called = 0
        self.seed: int = seed

    def registerInitialState(self, game_state: GameState):
        if 'registerInitialState' in dir(self.agent_to_be_tested):
            self.agent_to_be_tested.registerInitialState(game_state)
        random.seed(self.seed)

    def getAction(self, game_state: GameState) -> Action:
        GameState.getAndResetExplored()

        # (Action, exploration_depth)
        tuple__action__len_explored___from_agent_to_be_tested: Tuple[Action, int] = (
            (self.agent_to_be_tested.getAction(game_state), len(GameState.getAndResetExplored()))
        )

        # Possible correct solution (Came from a file)
        list_list_list_action__value_optimal = self.list_list_list_list_action__value_optimal[self._count_action_called]

        # Possible correct solution (Came from a file)
        list_list_action_alt_depth = self.list_list_list_action_alt_depth[self._count_action_called]

        # Possible correct solution (Came from a file)
        list_list_action_partial_play_bug = self.list_list_list_action_partial_play_bug[self._count_action_called]

        bool_is_agent_to_be_tested_action_is_optimal: bool = False
        bool_is_agent_to_be_tested_exploration_depth_correct: bool = False

        # Check if (Action, exploration_depth) from agent_to_be_tested is correct
        for i, list_action__value_optimal in enumerate(list_list_list_action__value_optimal):

            # Check if Action is correct
            if tuple__action__len_explored___from_agent_to_be_tested[0] in list_list_list_action__value_optimal[i][0]:
                bool_is_agent_to_be_tested_action_is_optimal = True
            else:
                self.list_bool_action_consistent_with_optimal[i] = False

            # Check if exploration_depth is correct
            if tuple__action__len_explored___from_agent_to_be_tested[1] == list_list_list_action__value_optimal[i][1]:
                bool_is_agent_to_be_tested_exploration_depth_correct = True

        # bool_is_agent_to_be_tested_exploration_depth_correct is False
        if not bool_is_agent_to_be_tested_exploration_depth_correct:
            self.amount_wrong_states_explored += 1

        ##########

        # Check if Action is correct using list_list_action_alt_depth
        for i, list_action_alt_depth in enumerate(list_list_action_alt_depth):
            if tuple__action__len_explored___from_agent_to_be_tested[0] not in list_list_action_alt_depth[i]:
                self.list_bool_action_consistent_with_alternative_depth[i] = False

        ##########

        # Check if Action is correct using list_list_action_partial_play_bug
        for i, list_action_partial_play_bug in enumerate(list_list_action_partial_play_bug):
            if tuple__action__len_explored___from_agent_to_be_tested[0] not in list_list_action_partial_play_bug[i]:
                self.list_bool_action_consistent_with_partial_play_bug[i] = False

        ##########

        action_optimal: Action = list_list_list_action__value_optimal[0][0][0]

        # If agent_to_be_tested is incorrect
        if not bool_is_agent_to_be_tested_action_is_optimal:
            self.list_tuple_game_state__action_from_agent_to_be_tested__action_optimal.append(
                (
                    game_state,
                    tuple__action__len_explored___from_agent_to_be_tested[0],
                    action_optimal
                )
            )

        self._count_action_called += 1
        random.seed(self.seed + self._count_action_called)
        return action_optimal

    def get_list_tuple__game_state__action_wrong__action_correct(self) -> List[
        TYPE_TUPLE_GAME_STATE__ACTION_WRONG__ACTION_CORRECT]:
        return self.list_tuple_game_state__action_from_agent_to_be_tested__action_optimal

    def get_amount_wrong_states_explored(self) -> int:
        return self.amount_wrong_states_explored

    def get_value_failure(self) -> int:
        """
        Return +n if have n suboptimal moves.
        Return -n if have n off by one depth moves.
        Return 0 otherwise.
        """
        if self.amount_wrong_states_explored > 0:
            return -3
        if self.list_bool_action_consistent_with_optimal.count(True) > 0:
            return 0
        elif self.list_bool_action_consistent_with_partial_play_bug.count(True) > 0:
            return -2
        elif self.list_bool_action_consistent_with_alternative_depth.count(True) > 0:
            return -1
        else:
            return len(self.list_tuple_game_state__action_from_agent_to_be_tested__action_optimal)
