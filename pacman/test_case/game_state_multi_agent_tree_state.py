"""
Date created: 1/30/2023

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
from typing import Union

from common.state import State
from pacman.agent import Agent

if TYPE_CHECKING:
    pass

VERBOSE = False


class MultiAgentTreeState(State):



    def __init__(self, problem, state, agent: Agent):  # TODO: THIS AGENT IS A BYPASS
        self.problem = problem
        self.state = state

        self._agent_BYPASS = agent

    def generateSuccessor(self, agentIndex, action):
        if VERBOSE:
            print("generateSuccessor(%s, %s, %s) -> %s" % (self.state, agentIndex,
                                                           action,
                                                           self.problem.stateToSuccessorMap[self.state][action]))

        successor = self.problem.stateToSuccessorMap[self.state][action]
        self.problem.generatedStates.add(successor)
        return MultiAgentTreeState(self.problem, successor, self._agent_BYPASS)

    def getScore(self):
        if VERBOSE:
            print("getScore(%s) -> %s" %
                  (self.state, self.problem.dict_evaluation_k_state_v_value[self.state]))
        if self.state not in self.problem.dict_evaluation_k_state_v_value:
            raise Exception(
                'getScore() called on non-terminal state or before maximum depth achieved.')
        return float(self.problem.dict_evaluation_k_state_v_value[self.state])

    def getLegalActions(self, agentIndex=0):
        if VERBOSE:
            print("getLegalActions(%s) -> %s" %
                  (self.state, self.problem.stateToActions[self.state]))
        # if len(self.problem_multi_agent_tree.stateToActions[self.state]) == 0:
        #    print "WARNING: getLegalActions called on leaf state %s" % (self.state,)
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

    #############  # TODO: IMPLEMENT THESE JOSEPH

    def get_index_by_agent(self, agent: Agent) -> Union[int, None]:
        pass

    def get_container_state_GHOST(self, agent: Agent):
        pass

    def get_agent_by_index(self, index: int) -> Union[Agent, None]:
        if index == 0:
            return self._agent_BYPASS
