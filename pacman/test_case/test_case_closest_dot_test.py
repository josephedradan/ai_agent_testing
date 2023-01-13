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

from typing import Any
from typing import Dict
from typing import TYPE_CHECKING

from pacman.agent import *
from pacman.game.game_state import GameState
from pacman.game.layout import Layout
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from pacman.grader import Grader


class ClosestDotTest(TestCase):

    def __init__(self, question, testDict):
        super(ClosestDotTest, self).__init__(question, testDict)
        self.layoutText = testDict['layout']
        self.layoutName = testDict['layoutName']

    def _solution(self):
        lay = Layout([l.strip() for l in self.layoutText.split('\n')])
        gameState = GameState()
        gameState.initialize(lay, 0)
        path = ClosestDotSearchAgent().findPathToClosestDot(gameState)
        return path

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']
        gold_length = int(dict_file_solution['solution_length'])

        solution = self._solution()

        if type(solution) != type([]):
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('\tThe result must be a list. (Instead, it is %s)' % type(solution))
            return False

        if len(solution) != gold_length:
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('Closest dot not found.')
            grader.addMessage('\tstudent solution length:\n%s' % len(solution))
            grader.addMessage('')
            grader.addMessage('\tcorrect solution length:\n%s' % gold_length)
            return False

        grader.addMessage('PASS: %s' % self.path_file_test)
        grader.addMessage('\tpacman layout:\t\t%s' % self.layoutName)
        grader.addMessage('\tsolution length:\t\t%s' % len(solution))
        return True

    def writeSolution(self, filePath):
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']

        # open file and write comments
        handle = open(filePath, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path_file_test)

        print("Solving problem", self.layoutName)
        print(self.layoutText)

        length = len(self._solution())
        print("Problem solved")

        handle.write('solution_length: "%s"\n' % length)
        handle.close()
        return True
