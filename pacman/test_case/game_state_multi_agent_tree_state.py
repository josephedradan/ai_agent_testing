"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/30/2023

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

from collections import defaultdict
from typing import Any
from typing import Dict
from typing import List
from typing import Set
from typing import TYPE_CHECKING
from typing import Tuple

from common.state import State
from pacman.agent import *
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from pacman.question.question import Question
    from common.grader import Grader

VERBOSE = False


class MultiAgentTreeState(State):
    def __init__(self, problem, state):
        self.problem = problem
        self.state = state

    def generateSuccessor(self, agentIndex, action):
        if VERBOSE:
            print("generateSuccessor(%s, %s, %s) -> %s" % (self.state, agentIndex,
                                                           action,
                                                           self.problem.stateToSuccessorMap[self.state][action]))

        successor = self.problem.stateToSuccessorMap[self.state][action]
        self.problem.generatedStates.add(successor)
        return MultiAgentTreeState(self.problem, successor)

    def getScore(self):
        if VERBOSE:
            print("getScore(%s) -> %s" %
                  (self.state, self.problem.dict_evaluation_k_state_v_value[self.state]))
        if self.state not in self.problem.dict_evaluation_k_state_v_value:
            raise Exception(
                'getScore() called on non-terminal state_pacman or before maximum depth achieved.')
        return float(self.problem.dict_evaluation_k_state_v_value[self.state])

    def getLegalActions(self, agentIndex=0):
        if VERBOSE:
            print("getLegalActions(%s) -> %s" %
                  (self.state, self.problem.stateToActions[self.state]))
        # if len(self.problem_multi_agent_tree.stateToActions[self.state_pacman]) == 0:
        #    print "WARNING: getLegalActions called on leaf state_pacman %s" % (self.state_pacman,)
        return list(self.problem.stateToActions[self.state])

    def isWin(self):
        if VERBOSE:
            print("isWin(%s) -> %s" %
                  (self.state, self.state in self.problem.set_state_win))
        return self.state in self.problem.set_state_win

    def isLose(self):
        if VERBOSE:
            print("isLose(%s) -> %s" %
                  (self.state, self.state in self.problem.set_state_lose))
        return self.state in self.problem.set_state_lose

    def getNumAgents(self):
        if VERBOSE:
            print("getNumAgents(%s) -> %s" %
                  (self.state, self.problem.num_agents))
        return self.problem.num_agents
