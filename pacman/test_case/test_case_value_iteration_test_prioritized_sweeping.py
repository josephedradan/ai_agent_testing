"""
Date created: 1/13/2023

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
from functools import reduce

from pacman.agent.valueIterationAgents import PrioritizedSweepingValueIterationAgent
from pacman.test_case import ValueIterationTest


class PrioritizedSweepingValueIterationTest(ValueIterationTest):
    def runAgent(self, numIterations):

        agent = PrioritizedSweepingValueIterationAgent(
            self.grid,
            discount=self.discount,
            iterations=numIterations
        )
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
