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
import sys
from typing import Any
from typing import Dict

from pacman.agent.qlearningAgents import QLearningAgent
from pacman.grader import Grader
from pacman.gridworld import Gridworld
from pacman.gridworld import GridworldEnvironment
from pacman.test_case import TestCase
from pacman.test_case.test_case_grid_policy_test import parseGrid
from pacman.util import Experiences


class EpsilonGreedyTest(TestCase):

    def __init__(self, question, testDict):
        super(EpsilonGreedyTest, self).__init__(question, testDict)
        self.discount = float(testDict['discount'])
        self.grid = Gridworld(parseGrid(testDict['grid']))
        if 'noise' in testDict: self.grid.setNoise(float(testDict['noise']))
        if 'livingReward' in testDict: self.grid.setLivingReward(float(testDict['livingReward']))

        self.grid = Gridworld(parseGrid(testDict['grid']))
        self.env = GridworldEnvironment(self.grid)
        self.epsilon = float(testDict['epsilon'])
        self.learningRate = float(testDict['learningRate'])
        self.numExperiences = int(testDict['numExperiences'])
        self.numIterations = int(testDict['iterations'])
        self.opts = {'actionFn': self.env.getPossibleActions, 'epsilon': self.epsilon, 'gamma': self.discount,
                     'alpha': self.learningRate}
        if sys.platform == 'win32':
            _, question_name, test_name = testDict['path_test_output'].split('\\')
        else:
            _, question_name, test_name = testDict['path_test_output'].split('/')
        self.experiences = Experiences(test_name.split('.')[0])

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        if self.testEpsilonGreedy():
            return self._procedure_test_pass(grader)
        else:
            return self._procedure_test_fail(grader)

    def writeSolution(self, filePath):
        with open(filePath, 'w') as handle:
            handle.write('# This is the solution file for %s.\n' % self.path_file_test)
            handle.write('# File intentionally blank.\n')
        return True

    def runAgent(self):
        agent = QLearningAgent(**self.opts)
        states = [state for state in self.grid.getStates() if len(self.grid.getPossibleActions(state)) > 0]
        states.sort()
        for i in range(self.numExperiences):
            lastExperience = self.experiences.get_experience()
            agent.update(*lastExperience)
        return agent

    def testEpsilonGreedy(self, tolerance=0.025):

        agent = self.runAgent()
        for state in self.grid.getStates():
            numLegalActions = len(agent.getLegalActions(state))
            if numLegalActions <= 1:
                continue
            numGreedyChoices = 0
            optimalAction = agent.computeActionFromQValues(state)
            for iteration in range(self.numIterations):
                # assume that their computeActionFromQValues implementation is correct (q4 tests this)
                if agent.getAction(state) == optimalAction:
                    numGreedyChoices += 1
            # e = epsilon, g = # greedy actions, n = numIterations, k = numLegalActions
            # g = n * [(1-e) + e/k] -> e = (n - g) / (n - n/k)
            empiricalEpsilonNumerator = self.numIterations - numGreedyChoices
            empiricalEpsilonDenominator = self.numIterations - self.numIterations / float(numLegalActions)
            empiricalEpsilon = empiricalEpsilonNumerator / empiricalEpsilonDenominator
            error = abs(empiricalEpsilon - self.epsilon)
            if error > tolerance:
                self.addMessage("Epsilon-greedy action selection is not correct.")
                self.addMessage("Actual epsilon = %f; student empirical epsilon = %f; error = %f > tolerance = %f" % (
                    self.epsilon, empiricalEpsilon, error, tolerance))
                return False
        return True
