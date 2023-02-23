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
from typing import Union

from common.state_pacman import StatePacman
from pacman.agent import Agent
from pacman.agent import AgentPacman
from pacman.agent.search.search import astar
from pacman.agent.search_problem import CornersProblem
from pacman.agent.search_problem.agent_pacman__search_problem import cornersHeuristic
from pacman.game.layoutpacman import LayoutPacman
from pacman.game.player_pacman import PlayerPacman
from pacman.game.type_player_pacman import EnumPlayerPacman
from pacman.test_case.common import followPath
from pacman.test_case.common import wrap_solution
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from pacman.question.question import Question
    from common.grader import Grader


class CornerHeuristicSanity(TestCase):

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        super(CornerHeuristicSanity, self).__init__(question, dict_file_test)

        self.str_layout: Union[str, None] = dict_file_test.get('layout_text')

        self.name_layout: Union[str, None] = dict_file_test.get('layout_name')

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']

        agent: Agent = AgentPacman()  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        list_player = [PlayerPacman(
            self.question.get_graphics().get_gui(),
            self.question.get_graphics(),
            agent,
            EnumPlayerPacman.PACMAN
        )]  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        #####

        lay = LayoutPacman([l.strip() for l in self.str_layout.split('\n')])

        state_pacman = StatePacman()

        state_pacman.initialize(lay, list_player)

        problem = CornersProblem(agent, state_pacman)
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
        for state_pacman in states:
            heuristics.append(cornersHeuristic(state_pacman, problem))
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

        agent: Agent = AgentPacman()  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        list_player = [PlayerPacman(agent, EnumPlayerPacman.PACMAN)]  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        ######

        # solve problem_multi_agent_tree and write solution
        lay = LayoutPacman([l.strip() for l in self.str_layout.split('\n')])
        start_state = StatePacman()
        start_state.initialize(lay, list_player)
        problem = CornersProblem(agent, start_state)
        solution = astar(problem, cornersHeuristic)
        handle.write('cost: "%d"\n' % len(solution))
        handle.write('path: """\n%s\n"""\n' % wrap_solution(solution))
        handle.close()
        return True
