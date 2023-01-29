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
import os
from functools import reduce
from typing import Any
from typing import Dict

from gridworld.main_grid_world import Gridworld
from pacman.agent.valueIterationAgents import ValueIterationAgent
from common.grader import Grader
from pacman.test_case import TestCase
from pacman.test_case.test_case_grid_policy_test import parseGrid


class ValueIterationTest(TestCase):

    def __init__(self, question, testDict):
        super(ValueIterationTest, self).__init__(question, testDict)
        self.discount = float(testDict['discount'])
        self.grid = Gridworld(parseGrid(testDict['grid']))
        iterations = int(testDict['valueIterations'])
        if 'noise' in testDict: self.grid.setNoise(float(testDict['noise']))
        if 'livingReward' in testDict: self.grid.setLivingReward(float(testDict['livingReward']))

        maxPreIterations = 10
        self.numsIterationsForDisplay = list(range(min(iterations, maxPreIterations)))

        # pprint(testDict)
        self.testOutFile = testDict['path_test_output']

        if maxPreIterations < iterations:
            self.numsIterationsForDisplay.append(iterations)

    def writeFailureFile(self, string):
        with open(self.testOutFile, 'w') as handle:
            handle.write(string)

    def removeFailureFileIfExists(self):
        if os.path.exists(self.testOutFile):
            os.remove(self.testOutFile)

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        failureOutputFileString = ''
        failureOutputStdString = ''
        for n in self.numsIterationsForDisplay:
            checkPolicy = (n == self.numsIterationsForDisplay[-1])
            testPass, stdOutString, fileOutString = self.executeNIterations(grader,
                                                                            dict_file_solution,
                                                                            n,
                                                                            checkPolicy)
            failureOutputStdString += stdOutString
            failureOutputFileString += fileOutString
            if not testPass:
                self.add_message_to_messages(failureOutputStdString)
                self.add_message_to_messages('For more details to help you debug, see test output file %s\n\n' % self.testOutFile)
                self.writeFailureFile(failureOutputFileString)
                return self._procedure_test_fail(grader)
        self.removeFailureFileIfExists()
        return self._procedure_test_pass(grader)

    def executeNIterations(self, grader, dict_file_solution, n, checkPolicy):
        testPass = True

        valuesPretty, qValuesPretty, actions, policyPretty = self.runAgent(n)
        stdOutString = ''
        fileOutString = ''
        valuesKey = "values_k_%d" % n
        if self.comparePrettyValues(valuesPretty, dict_file_solution[valuesKey]):
            fileOutString += "Values at iteration %d are correct.\n" % n
            fileOutString += "   Student/correct solution:\n %s\n" % self.prettyValueSolutionString(valuesKey,
                                                                                                    valuesPretty)
        else:
            testPass = False
            outString = "Values at iteration %d are NOT correct.\n" % n
            outString += "   Student solution:\n %s\n" % self.prettyValueSolutionString(valuesKey, valuesPretty)
            outString += "   Correct solution:\n %s\n" % self.prettyValueSolutionString(valuesKey,
                                                                                        dict_file_solution[valuesKey])
            stdOutString += outString
            fileOutString += outString
        for action in actions:
            qValuesKey = 'q_values_k_%d_action_%s' % (n, action)
            qValues = qValuesPretty[action]
            if self.comparePrettyValues(qValues, dict_file_solution[qValuesKey]):
                fileOutString += "Q-Values at iteration %d for action %s are correct.\n" % (n, action)
                fileOutString += "   Student/correct solution:\n %s\n" % self.prettyValueSolutionString(qValuesKey,
                                                                                                        qValues)
            else:
                testPass = False
                outString = "Q-Values at iteration %d for action %s are NOT correct.\n" % (n, action)
                outString += "   Student solution:\n %s\n" % self.prettyValueSolutionString(qValuesKey, qValues)
                outString += "   Correct solution:\n %s\n" % self.prettyValueSolutionString(qValuesKey,
                                                                                            dict_file_solution[qValuesKey])
                stdOutString += outString
                fileOutString += outString
        if checkPolicy:
            if not self.comparePrettyValues(policyPretty, dict_file_solution['policy']):
                testPass = False
                outString = "Policy is NOT correct.\n"
                outString += "   Student solution:\n %s\n" % self.prettyValueSolutionString('policy', policyPretty)
                outString += "   Correct solution:\n %s\n" % self.prettyValueSolutionString('policy',
                                                                                            dict_file_solution['policy'])
                stdOutString += outString
                fileOutString += outString
        return testPass, stdOutString, fileOutString

    def write_solution(self, path_file_solution: str) -> bool:
        with open(path_file_solution, 'w') as handle:
            policyPretty = ''
            actions = []
            for n in self.numsIterationsForDisplay:
                valuesPretty, qValuesPretty, actions, policyPretty = self.runAgent(n)
                handle.write(self.prettyValueSolutionString('values_k_%d' % n, valuesPretty))
                for action in actions:
                    handle.write(
                        self.prettyValueSolutionString('q_values_k_%d_action_%s' % (n, action), qValuesPretty[action]))
            handle.write(self.prettyValueSolutionString('policy', policyPretty))
            handle.write(self.prettyValueSolutionString('actions', '\n'.join(actions) + '\n'))
        return True

    def runAgent(self, numIterations):
        agent = ValueIterationAgent(self.grid,
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

    def prettyPrint(self, elements, formatString):
        pretty = ''
        states = self.grid.getStates()
        for ybar in range(self.grid.grid.height):
            y = self.grid.grid.height - 1 - ybar
            row = []
            for x in range(self.grid.grid.width):
                if (x, y) in states:
                    value = elements[(x, y)]
                    if value is None:
                        row.append('   illegal')
                    else:
                        row.append(formatString.format(elements[(x, y)]))
                else:
                    row.append('_' * 10)
            pretty += '        %s\n' % ("   ".join(row),)
        pretty += '\n'
        return pretty

    def prettyValues(self, values):
        return self.prettyPrint(values, '{0:10.4f}')

    def prettyPolicy(self, policy):
        return self.prettyPrint(policy, '{0:10s}')

    def prettyValueSolutionString(self, name, pretty):
        return '%s: """\n%s\n"""\n\n' % (name, pretty.rstrip())

    def comparePrettyValues(self, aPretty, bPretty, tolerance=0.01):
        aList = self.parsePrettyValues(aPretty)
        bList = self.parsePrettyValues(bPretty)
        if len(aList) != len(bList):
            return False
        for a, b in zip(aList, bList):
            try:
                aNum = float(a)
                bNum = float(b)
                # error = abs((aNum - bNum) / ((aNum + bNum) / 2.0))
                error = abs(aNum - bNum)
                if error > tolerance:
                    return False
            except ValueError:
                if a.strip() != b.strip():
                    return False
        return True

    def parsePrettyValues(self, pretty):
        values = pretty.split()
        return values
