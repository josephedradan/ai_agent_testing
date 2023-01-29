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
from typing import Union

from common.game_state_pacman import GameStatePacman
from pacman.agent.search.search import astar
from pacman.agent.search_problem import CornersProblem
from pacman.agent.search_problem.agent_pacman__search_problem import cornersHeuristic
from common.game_state import GameState
from pacman.game.layout import Layout
from pacman.test_case.common import followPath
from pacman.test_case.common import wrap_solution
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from pacman.question.question import Question
    from common.grader import Grader


class CornerHeuristicSanity(TestCase):

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        super(CornerHeuristicSanity, self).__init__(question, dict_file_test)

        self.str_layout: Union[str, None] = dict_file_test.get('layout')

        self.name_layout: Union[str, None] = dict_file_test.get('layoutName')

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']

        game_state = GameStatePacman()
        lay = Layout([l.strip() for l in self.str_layout.split('\n')])
        game_state.initialize(lay, 0)
        problem = CornersProblem(game_state)
        start_state = problem.getStartState()
        h0 = cornersHeuristic(start_state, problem)
        succs = problem.getSuccessors(start_state)
        # cornerConsistencyA
        for succ in succs:
            h1 = cornersHeuristic(succ[0], problem)
            if h0 - h1 > 1:
                grader.addMessage('FAIL: inconsistent heuristic')
                return False
        heuristic_cost = cornersHeuristic(start_state, problem)
        true_cost = float(dict_file_solution['cost'])
        # cornerNontrivial
        if heuristic_cost == 0:
            grader.addMessage('FAIL: must use non-trivial heuristic')
            return False
        # cornerAdmissible
        if heuristic_cost > true_cost:
            grader.addMessage('FAIL: Inadmissible heuristic')
            return False
        path = dict_file_solution['path'].split()
        states = followPath(path, problem)
        heuristics = []
        for state in states:
            heuristics.append(cornersHeuristic(state, problem))
        for i in range(0, len(heuristics) - 1):
            h0 = heuristics[i]
            h1 = heuristics[i + 1]
            # cornerConsistencyB
            if h0 - h1 > 1:
                grader.addMessage('FAIL: inconsistent heuristic')
                return False
            # cornerPosH
            if h0 < 0 or h1 < 0:
                grader.addMessage('FAIL: non-positive heuristic')
                return False
        # cornerGoalH
        if heuristics[len(heuristics) - 1] != 0:
            grader.addMessage('FAIL: heuristic non-zero at goal')
            return False
        grader.addMessage('PASS: heuristic value less than true cost at start state')
        return True

    def write_solution(self, path_file_solution: str) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']
        # write comment
        handle = open(path_file_solution, 'w')
        handle.write('# In order for a heuristic to be admissible, the value\n')
        handle.write('# of the heuristic must be less at each state than the\n')
        handle.write('# true cost of the optimal path from that state to a goal.\n')

        # solve problem and write solution
        lay = Layout([l.strip() for l in self.str_layout.split('\n')])
        start_state = GameState()
        start_state.initialize(lay, 0)
        problem = CornersProblem(start_state)
        solution = astar(problem, cornersHeuristic)
        handle.write('cost: "%d"\n' % len(solution))
        handle.write('path: """\n%s\n"""\n' % wrap_solution(solution))
        handle.close()
        return True
