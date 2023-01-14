"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/13/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from functools import reduce

from pacman.agent.valueIterationAgents import AsynchronousValueIterationAgent
from pacman.test_case.test_case_value_iteration_test import ValueIterationTest


class AsynchronousValueIterationTest(ValueIterationTest):
    def runAgent(self, numIterations):
        agent = AsynchronousValueIterationAgent(self.grid,
                                                discount=self.discount,
                                                iterations=numIterations)
        states = self.grid.getStates()
        actions = list(reduce(lambda a, b: set(a).union(b), [self.grid.getPossibleActions(state) for state in states]))
        values = {}
        qValues = {}
        policy = {}
        for state in states:
            values[state] = agent.getValue(state)
            policy[state] = agent.computeActionFromValues(state)
            possibleActions = self.grid.getPossibleActions(state)
            for action in actions:
                if action not in qValues:
                    qValues[action] = {}
                if action in possibleActions:
                    qValues[action][state] = agent.computeQValueFromValues(state, action)
                else:
                    qValues[action][state] = None
        valuesPretty = self.prettyValues(values)
        policyPretty = self.prettyPolicy(policy)
        qValuesPretty = {}
        for action in actions:
            qValuesPretty[action] = self.prettyValues(qValues[action])
        return (valuesPretty, qValuesPretty, actions, policyPretty)
