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
import sys
from functools import reduce
from typing import Any
from typing import Dict

from gridworld.main_grid_world import Gridworld
from pacman.agent.qlearningAgents import QLearningAgent
from common.grader import Grader
from gridworld.main import EnvironmentGridworld
from pacman.test_case import TestCase
from pacman.test_case.test_case_grid_policy_test import parseGrid
from common.util import Experiences


class QLearningTest(TestCase):

    def __init__(self, question, testDict):
        super(QLearningTest, self).__init__(question, testDict)
        self.discount = float(testDict['discount'])
        self.grid = Gridworld(parseGrid(testDict['grid']))
        if 'noise' in testDict: self.grid.setNoise(float(testDict['noise']))
        if 'livingReward' in testDict: self.grid.setLivingReward(float(testDict['livingReward']))
        self.grid = Gridworld(parseGrid(testDict['grid']))
        self.env = EnvironmentGridworld(self.grid)
        self.epsilon = float(testDict['epsilon'])
        self.learningRate = float(testDict['learningRate'])
        self.opts = {'actionFn': self.env.getPossibleActions, 'epsilon': self.epsilon, 'gamma': self.discount,
                     'alpha': self.learningRate}
        numExperiences = int(testDict['numExperiences'])
        maxPreExperiences = 10
        self.numsExperiencesForDisplay = list(range(min(numExperiences, maxPreExperiences)))
        self.testOutFile = testDict['path_test_output']
        if sys.platform == 'win32':
            _, name_question, name_test = testDict['path_test_output'].split('\\')
        else:
            _, name_question, name_test = testDict['path_test_output'].split('/')
        self.experiences = Experiences(name_test.split('.')[0])
        if maxPreExperiences < numExperiences:
            self.numsExperiencesForDisplay.append(numExperiences)

    def writeFailureFile(self, string):
        with open(self.testOutFile, 'w') as handle:
            handle.write(string)

    def removeFailureFileIfExists(self):
        if os.path.exists(self.testOutFile):
            os.remove(self.testOutFile)

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        failureOutputFileString = ''
        failureOutputStdString = ''
        for n in self.numsExperiencesForDisplay:
            checkValuesAndPolicy = (n == self.numsExperiencesForDisplay[-1])
            testPass, stdOutString, fileOutString = self.executeNExperiences(grader,
                                                                             dict_file_solution,
                                                                             n,
                                                                             checkValuesAndPolicy)
            failureOutputStdString += stdOutString
            failureOutputFileString += fileOutString
            if not testPass:
                self.addMessage(failureOutputStdString)
                self.addMessage('For more details to help you debug, see test output file %s\n\n' % self.testOutFile)
                self.writeFailureFile(failureOutputFileString)
                return self._procedure_test_fail(grader)
        self.removeFailureFileIfExists()
        return self._procedure_test_pass(grader)

    def executeNExperiences(self, grader, dict_file_solution, n, checkValuesAndPolicy):
        testPass = True
        valuesPretty, qValuesPretty, actions, policyPretty, lastExperience = self.runAgent( n)
        stdOutString = ''
        # fileOutString = "==================== Iteration %d ====================\n" % n
        fileOutString = ''
        if lastExperience is not None:
            # fileOutString += "Agent observed the transition (startState = %s, action = %s, endState = %s, reward = %f)\n\n\n" % lastExperience
            pass
        for action in actions:
            qValuesKey = 'q_values_k_%d_action_%s' % (n, action)
            qValues = qValuesPretty[action]

            if self.comparePrettyValues(qValues, dict_file_solution[qValuesKey]):
                # fileOutString += "Q-Values at iteration %d for action '%s' are correct." % (n, action)
                # fileOutString += "   Student/correct solution:\n\t%s" % self.prettyValueSolutionString(qValuesKey, qValues)
                pass
            else:
                testPass = False
                outString = "Q-Values at iteration %d for action '%s' are NOT correct." % (n, action)
                outString += "   Student solution:\n\t%s" % self.prettyValueSolutionString(qValuesKey, qValues)
                outString += "   Correct solution:\n\t%s" % self.prettyValueSolutionString(qValuesKey,
                                                                                           dict_file_solution[qValuesKey])
                stdOutString += outString
                fileOutString += outString
        if checkValuesAndPolicy:
            if not self.comparePrettyValues(valuesPretty, dict_file_solution['values']):
                testPass = False
                outString = "Values are NOT correct."
                outString += "   Student solution:\n\t%s" % self.prettyValueSolutionString('values', valuesPretty)
                outString += "   Correct solution:\n\t%s" % self.prettyValueSolutionString('values',
                                                                                           dict_file_solution['values'])
                stdOutString += outString
                fileOutString += outString
            if not self.comparePrettyValues(policyPretty, dict_file_solution['policy']):
                testPass = False
                outString = "Policy is NOT correct."
                outString += "   Student solution:\n\t%s" % self.prettyValueSolutionString('policy', policyPretty)
                outString += "   Correct solution:\n\t%s" % self.prettyValueSolutionString('policy',
                                                                                           dict_file_solution['policy'])
                stdOutString += outString
                fileOutString += outString
        return testPass, stdOutString, fileOutString

    def write_solution(self, path_file_solution: str) -> bool:
        with open(path_file_solution, 'w') as handle:
            valuesPretty = ''
            policyPretty = ''
            for n in self.numsExperiencesForDisplay:
                valuesPretty, qValuesPretty, actions, policyPretty, _ = self.runAgent( n)
                for action in actions:
                    handle.write(
                        self.prettyValueSolutionString('q_values_k_%d_action_%s' % (n, action), qValuesPretty[action]))
            handle.write(self.prettyValueSolutionString('values', valuesPretty))
            handle.write(self.prettyValueSolutionString('policy', policyPretty))
        return True

    def runAgent(self, numExperiences):
        agent = QLearningAgent(**self.opts)
        states = [state for state in self.grid.getStates() if len(self.grid.getPossibleActions(state)) > 0]
        states.sort()
        lastExperience = None
        for i in range(numExperiences):
            lastExperience = self.experiences.get_experience()
            agent.update(*lastExperience)
        actions = list(reduce(lambda a, b: set(a).union(b), [self.grid.getPossibleActions(state) for state in states]))
        values = {}
        qValues = {}
        policy = {}
        for state in states:
            values[state] = agent.computeValueFromQValues(state)
            policy[state] = agent.computeActionFromQValues(state)
            possibleActions = self.grid.getPossibleActions(state)
            for action in actions:
                if action not in qValues:
                    qValues[action] = {}
                if action in possibleActions:
                    qValues[action][state] = agent.getQValue(state, action)
                else:
                    qValues[action][state] = None
        valuesPretty = self.prettyValues(values)
        policyPretty = self.prettyPolicy(policy)
        qValuesPretty = {}
        for action in actions:
            qValuesPretty[action] = self.prettyValues(qValues[action])
        return (valuesPretty, qValuesPretty, actions, policyPretty, lastExperience)

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
