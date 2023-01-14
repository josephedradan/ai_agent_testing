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
from pprint import PrettyPrinter
from typing import Any
from typing import Dict

from pacman.agent.qlearningAgents import ApproximateQAgent
from pacman.grader import Grader
from pacman.gridworld import Gridworld
from pacman.gridworld import GridworldEnvironment
from pacman.test_case import TestCase
from pacman.test_case.test_case_grid_policy_test import parseGrid
from pacman.util import Experiences

pp = PrettyPrinter()


class ApproximateQLearningTest(TestCase):

    def __init__(self, question, testDict):
        super(ApproximateQLearningTest, self).__init__(question, testDict)
        self.discount = float(testDict['discount'])
        self.grid = Gridworld(parseGrid(testDict['grid']))
        if 'noise' in testDict: self.grid.setNoise(float(testDict['noise']))
        if 'livingReward' in testDict: self.grid.setLivingReward(float(testDict['livingReward']))
        self.grid = Gridworld(parseGrid(testDict['grid']))
        self.env = GridworldEnvironment(self.grid)
        self.epsilon = float(testDict['epsilon'])
        self.learningRate = float(testDict['learningRate'])
        self.extractor = 'IdentityExtractor'
        if 'extractor' in testDict:
            self.extractor = testDict['extractor']
        self.opts = {'actionFn': self.env.getPossibleActions, 'epsilon': self.epsilon, 'gamma': self.discount,
                     'alpha': self.learningRate}
        numExperiences = int(testDict['numExperiences'])
        maxPreExperiences = 10
        self.numsExperiencesForDisplay = list(range(min(numExperiences, maxPreExperiences)))
        self.testOutFile = testDict['path_test_output']
        if sys.platform == 'win32':
            _, question_name, test_name = testDict['path_test_output'].split('\\')
        else:
            _, question_name, test_name = testDict['path_test_output'].split('/')
        self.experiences = Experiences(test_name.split('.')[0])
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
            testPass, stdOutString, fileOutString = self.executeNExperiences(grader, dict_file_solution, n)
            failureOutputStdString += stdOutString
            failureOutputFileString += fileOutString
            if not testPass:
                self.addMessage(failureOutputStdString)
                self.addMessage('For more details to help you debug, see test output file %s\n\n' % self.testOutFile)
                self.writeFailureFile(failureOutputFileString)
                return self._procedure_test_fail(grader)
        self.removeFailureFileIfExists()
        return self._procedure_test_pass(grader)

    def executeNExperiences(self, grader, dict_file_solution, n):
        testPass = True
        qValuesPretty, weights, actions, lastExperience = self.runAgent(n)
        stdOutString = ''
        fileOutString = "==================== Iteration %d ====================\n" % n
        if lastExperience is not None:
            fileOutString += "Agent observed the transition (startState = %s, action = %s, endState = %s, reward = %f)\n\n" % lastExperience
        weightsKey = 'weights_k_%d' % n
        if weights == eval(dict_file_solution[weightsKey]):
            fileOutString += "Weights at iteration %d are correct." % n
            fileOutString += "   Student/correct solution:\n\n%s\n\n" % pp.pformat(weights)
        for action in actions:
            qValuesKey = 'q_values_k_%d_action_%s' % (n, action)
            qValues = qValuesPretty[action]
            if self.comparePrettyValues(qValues, dict_file_solution[qValuesKey]):
                fileOutString += "Q-Values at iteration %d for action '%s' are correct." % (n, action)
                fileOutString += "   Student/correct solution:\n\t%s" % self.prettyValueSolutionString(qValuesKey,
                                                                                                       qValues)
            else:
                testPass = False
                outString = "Q-Values at iteration %d for action '%s' are NOT correct." % (n, action)
                outString += "   Student solution:\n\t%s" % self.prettyValueSolutionString(qValuesKey, qValues)
                outString += "   Correct solution:\n\t%s" % self.prettyValueSolutionString(qValuesKey,
                                                                                           dict_file_solution[
                                                                                               qValuesKey])
                stdOutString += outString
                fileOutString += outString
        return testPass, stdOutString, fileOutString

    def writeSolution(self, filePath):
        with open(filePath, 'w') as handle:
            for n in self.numsExperiencesForDisplay:
                qValuesPretty, weights, actions, _ = self.runAgent(n)
                handle.write(self.prettyValueSolutionString('weights_k_%d' % n, pp.pformat(weights)))
                for action in actions:
                    handle.write(
                        self.prettyValueSolutionString('q_values_k_%d_action_%s' % (n, action), qValuesPretty[action]))
        return True

    def runAgent(self, numExperiences):
        agent = ApproximateQAgent(extractor=self.extractor, **self.opts)
        states = [state for state in self.grid.getStates() if len(self.grid.getPossibleActions(state)) > 0]
        states.sort()
        lastExperience = None
        for i in range(numExperiences):
            lastExperience = self.experiences.get_experience()
            agent.update(*lastExperience)
        actions = list(reduce(lambda a, b: set(a).union(b), [self.grid.getPossibleActions(state) for state in states]))
        qValues = {}
        weights = agent.getWeights()
        for state in states:
            possibleActions = self.grid.getPossibleActions(state)
            for action in actions:
                if action not in qValues:
                    qValues[action] = {}
                if action in possibleActions:
                    qValues[action][state] = agent.getQValue(state, action)
                else:
                    qValues[action][state] = None
        qValuesPretty = {}
        for action in actions:
            qValuesPretty[action] = self.prettyValues(qValues[action])
        return (qValuesPretty, weights, actions, lastExperience)

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
