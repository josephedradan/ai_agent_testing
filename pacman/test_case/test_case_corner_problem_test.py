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

from pacman.agent.search_problem import CornersProblem
from pacman.game.actions import Actions
from pacman.game.game_state import GameState
from pacman.game.layout import Layout
from pacman.agent.search.search import bfs
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from pacman.grader import Grader


def getStatesFromPath(start, path):
    "Returns the list of states visited along the path"
    vis = [start]
    curr = start
    for a in path:
        x,y = curr
        dx, dy = Actions.directionToVector(a)
        curr = (int(x + dx), int(y + dy))
        vis.append(curr)
    return vis

class CornerProblemTest(TestCase):

    def __init__(self, question, testDict):
        super(CornerProblemTest, self).__init__(question, testDict)
        self.layoutText = testDict['layout']
        self.layoutName = testDict['layoutName']

    def solution(self):
        lay = Layout([l.strip() for l in self.layoutText.split('\n')])
        gameState = GameState()
        gameState.initialize(lay, 0)
        problem = CornersProblem(gameState)
        path = bfs(problem)

        gameState = GameState()
        gameState.initialize(lay, 0)
        visited = getStatesFromPath(gameState.getPacmanPosition(), path)
        top, right = gameState.getWalls().height-2, gameState.getWalls().width-2
        missedCorners = [p for p in ((1,1), (1,top), (right, 1), (right, top)) if p not in visited]

        return path, missedCorners

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']

        gold_length = int(dict_file_solution['solution_length'])
        solution, missedCorners = self.solution()

        if type(solution) != type([]):
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('The result must be a list. (Instead, it is %s)' % type(solution))
            return False

        if len(missedCorners) != 0:
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('Corners missed: %s' % missedCorners)
            return False

        if len(solution) != gold_length:
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('Optimal solution not found.')
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

        path, _ = self.solution()
        length = len(path)
        print("Problem solved")

        handle.write('solution_length: "%s"\n' % length)
        handle.close()
