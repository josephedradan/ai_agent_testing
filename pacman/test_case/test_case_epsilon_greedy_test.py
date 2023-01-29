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
from typing import Any
from typing import Dict
from typing import TYPE_CHECKING

from gridworld.main_grid_world import Gridworld

print("OS PATH APPENDED",os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "FROM", __file__)  # FIXME: GHETTO SOLUTION TO MISSING MODULE
from pprint import pprint
pprint(sys.path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pacman.agent.qlearningAgents import QLearningAgent
from common.grader import Grader
from gridworld.main import EnvironmentGridworld
from pacman.question.question import Question
from pacman.test_case import TestCase
from pacman.test_case.test_case_grid_policy_test import parseGrid
from common.util import Experiences

if TYPE_CHECKING:
    from common.grader import Grader


class EpsilonGreedyTest(TestCase):

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):

        super(EpsilonGreedyTest, self).__init__(question, dict_file_test)

        self.discount = float(dict_file_test['discount'])
        self.grid = Gridworld(parseGrid(dict_file_test['grid']))

        if 'noise' in dict_file_test: self.grid.setNoise(float(dict_file_test['noise']))

        if 'livingReward' in dict_file_test: self.grid.setLivingReward(float(dict_file_test['livingReward']))

        self.grid = Gridworld(parseGrid(dict_file_test['grid']))
        self.env = EnvironmentGridworld(self.grid)
        self.epsilon = float(dict_file_test['epsilon'])
        self.learningRate = float(dict_file_test['learningRate'])
        self.numExperiences = int(dict_file_test['numExperiences'])
        self.numIterations = int(dict_file_test['iterations'])
        self.opts = {'actionFn': self.env.getPossibleActions, 'epsilon': self.epsilon, 'gamma': self.discount,
                     'alpha': self.learningRate}
        if sys.platform == 'win32':
            _, name_question, name_test = dict_file_test['path_test_output'].split('\\')
        else:
            _, name_question, name_test = dict_file_test['path_test_output'].split('/')
        self.experiences = Experiences(name_test.split('.')[0])

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        if self.testEpsilonGreedy():
            return self._procedure_test_pass(grader)
        else:
            return self._procedure_test_fail(grader)

    def write_solution(self, path_file_solution: str) -> bool:
        with open(path_file_solution, 'w') as handle:
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
                self.add_message_to_messages("Epsilon-greedy action selection is not correct.")
                self.add_message_to_messages("Actual epsilon = %f; student empirical epsilon = %f; error = %f > tolerance = %f" % (
                    self.epsilon, empiricalEpsilon, error, tolerance))
                return False
        return True
