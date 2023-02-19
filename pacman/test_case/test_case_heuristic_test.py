"""
Date created: 1/12/2023

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
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import TYPE_CHECKING

from common.state_pacman import StatePacman
from pacman.agent import AgentPacman
from pacman.agent.heuristic_function import get_heuristic_function
from pacman.agent.search.search import astar
from pacman.agent.search_problem import get_subclass_search_problem
from pacman.game.layoutpacman import LayoutPacman
from pacman.game.player_pacman import PlayerPacman
from pacman.game.type_player_pacman import TypePlayerPacman
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from common.grader import Grader


class HeuristicTest(TestCase):

    def __init__(self, question, testDict):
        super(HeuristicTest, self).__init__(question, testDict)
        self.layoutText = testDict['layout_text']
        self.layout_name = testDict['layout_name']
        self.searchProblemClassName = testDict['searchProblemClass']
        self.heuristicName = testDict['heuristic']

    def _setupProblem(self):
        layout = LayoutPacman([l.strip() for l in self.layoutText.split('\n')])

        state_pacman_start = StatePacman()
        state_pacman_start.initialize(layout, [PlayerPacman(self.question.get_graphics().get_gui(),
                                                            self.question.get_graphics(),
                                                            AgentPacman(),
                                                            TypePlayerPacman.PACMAN)])

        # class_problem = getattr(searchAgents, self.searchProblemClassName)
        class_problem = get_subclass_search_problem(self.searchProblemClassName)

        problem = class_problem(state_pacman_start)
        state = problem.getStartState()

        # heuristic = getattr(searchAgents, self.heuristicName)
        heuristic = get_heuristic_function(self.heuristicName)

        return problem, state, heuristic

    def checkHeuristic(self, heuristic, problem, state, solutionCost):
        h0 = heuristic(state, problem)

        if solutionCost == 0:
            if h0 == 0:
                return True, ''
            else:
                return False, 'Heuristic failed H(goal) == 0 test'

        if h0 < 0:
            return False, 'Heuristic failed H >= 0 test'
        if not h0 > 0:
            return False, 'Heuristic failed non-triviality test'
        if not h0 <= solutionCost:
            return False, 'Heuristic failed admissibility test'

        for succ, action, stepCost in problem.getSuccessors(state):
            h1 = heuristic(succ, problem)
            if h1 < 0: return False, 'Heuristic failed H >= 0 test'
            if h0 - h1 > stepCost: return False, 'Heuristic failed consistency test'

        return True, ''

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']
        solutionCost = int(dict_file_solution['solution_cost'])
        problem, state, heuristic = self._setupProblem()

        passed, message = self.checkHeuristic(heuristic, problem, state, solutionCost)

        if not passed:
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('%s' % message)
            return False
        else:
            grader.addMessage('PASS: %s' % self.path_file_test)
            return True

    def write_solution(self, path_file_solution: str) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']
        # open file and write comments
        handle = open(path_file_solution, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path_file_test)

        print("Solving problem_multi_agent_tree", self.layout_name, self.heuristicName)
        print(self.layoutText)
        problem, _, heuristic = self._setupProblem()

        path = astar(problem, heuristic)
        cost = problem.getCostOfActions(path)
        print("Problem solved")

        handle.write('solution_cost: "%s"\n' % cost)
        handle.close()
        return True
