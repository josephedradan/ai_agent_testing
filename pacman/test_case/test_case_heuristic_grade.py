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

from common.state_pacman import StatePacman
from pacman.agent import Agent
from pacman.agent import AgentPacman
from pacman.agent.heuristic_function import get_heuristic_function
from pacman.agent.search.search import astar
from pacman.agent.search_problem import get_subclass_search_problem
from pacman.game.layoutpacman import LayoutPacman
from pacman.game.player_pacman import PlayerPacman
from pacman.game.type_player import TypePlayerPacman
from pacman.test_case.common import checkSolution
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from common.grader import Grader


class HeuristicGrade(TestCase):

    def __init__(self, question, testDict):
        super(HeuristicGrade, self).__init__(question, testDict)
        self.layoutText = testDict['layout_text']
        self.layout_name = testDict['layout_name']
        self.searchProblemClassName = testDict['searchProblemClass']
        self.heuristicName = testDict['heuristic']
        self.basePoints = int(testDict['basePoints'])
        self.thresholds = [int(t) for t in testDict['gradingThresholds'].split()]

    def _setupProblem(self):

        agent: Agent = AgentPacman()  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        list_player = [PlayerPacman(self.question.get_graphics().get_gui(),
                                    self.question.get_graphics(),
                                    agent,
                                    TypePlayerPacman.PACMAN)]  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        #####

        lay = LayoutPacman([l.strip() for l in self.layoutText.split('\n')])

        gameState = StatePacman()
        gameState.initialize(lay, list_player)

        # problemClass = getattr(searchAgents, self.searchProblemClassName)
        problemClass = get_subclass_search_problem(self.searchProblemClassName)

        problem = problemClass(gameState)  # FIXME: JOSEPH FIX

        state = problem.getStartState()
        # heuristic = getattr(searchAgents, self.heuristicName)
        heuristic = get_heuristic_function(self.heuristicName)

        return problem, state, heuristic

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']
        problem, _, heuristic = self._setupProblem()

        path = astar(problem, heuristic)

        expanded = problem._expanded

        if not checkSolution(problem, path):
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('\tReturned path is not a solution.')
            grader.addMessage('\tpath returned by astar: %s' % expanded)
            return False

        grader.addPoints(self.basePoints)
        points = 0
        for threshold in self.thresholds:
            if expanded <= threshold:
                points += 1
        grader.addPoints(points)
        if points >= len(self.thresholds):
            grader.addMessage('PASS: %s' % self.path_file_test)
        else:
            grader.addMessage('FAIL: %s' % self.path_file_test)
        grader.addMessage('\texpanded nodes: %s' % expanded)
        grader.addMessage('\tthresholds: %s' % self.thresholds)

        return True

    def write_solution(self, path_file_solution: str) -> bool:
        handle = open(path_file_solution, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path_file_test)
        handle.write('# File intentionally blank.\n')
        handle.close()
        return True
