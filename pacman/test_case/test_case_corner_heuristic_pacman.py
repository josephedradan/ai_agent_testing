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

from common.state_pacman import StatePacman
from pacman.agent import Agent
from pacman.agent import AgentPacman
from pacman.agent.search.search import astar
from pacman.agent.search_problem.agent_pacman__search_problem import cornersHeuristic
from pacman.agent.search_problem.search_problem_corners import CornersProblem
from pacman.game.layoutpacman import LayoutPacman
from pacman.game.player_pacman import PlayerPacman
from pacman.game.type_player import TypePlayerPacman
from pacman.test_case.common import wrap_solution
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from common.grader import Grader
    from pacman.question import Question


class CornerHeuristicPacman(TestCase):

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        super(CornerHeuristicPacman, self).__init__(question, dict_file_test)

        self.name_layout: Union[str, None] = dict_file_test.get('layout_name')

        self.str_layout: Union[str, None] = dict_file_test.get('layout_text')

    # def execute(self, grade, moduleDict, solutionDict):
    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']

        total = 0
        true_cost = float(dict_file_solution['cost'])
        thresholds = [int(x) for x in dict_file_solution['thresholds'].split()]

        agent: Agent = AgentPacman()  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        list_player = [PlayerPacman(
            self.question.get_graphics().get_gui(),
            self.question.get_graphics(),
            agent,
            TypePlayerPacman.PACMAN)
        ]  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        #####

        lay = LayoutPacman([l.strip() for l in self.str_layout.split('\n')])

        state_pacman = StatePacman()
        state_pacman.initialize(lay, list_player)
        problem = CornersProblem(agent, state_pacman)

        start_state = problem.getStartState()
        if cornersHeuristic(start_state, problem) > true_cost:
            grader.addMessage('FAIL: Inadmissible heuristic')
            return False
        path = astar(problem, cornersHeuristic)
        print("path:", path)
        print("path length:", len(path))
        cost = problem.getCostOfActions(path)
        if cost > true_cost:
            grader.addMessage('FAIL: Inconsistent heuristic')
            return False
        expanded = problem._expanded
        points = 0
        for threshold in thresholds:
            if expanded <= threshold:
                points += 1
        grader.addPoints(points)
        if points >= len(thresholds):
            grader.addMessage('PASS: Heuristic resulted in expansion of %d nodes' % expanded)
        else:
            grader.addMessage('FAIL: Heuristic resulted in expansion of %d nodes' % expanded)
        return True

    def write_solution(self, path_file_solution: str) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']
        # write comment
        handle = open(path_file_solution, 'w')
        handle.write('# This solution file specifies the length of the optimal path\n')
        handle.write('# as well as the thresholds on number of nodes expanded to be\n')
        handle.write('# used in scoring.\n')

        agent: Agent = AgentPacman()  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        list_player = [PlayerPacman(agent, TypePlayerPacman.PACMAN)]  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        ######

        # solve problem_multi_agent_tree and write solution
        lay = LayoutPacman([l.strip() for l in self.str_layout.split('\n')])
        start_state = StatePacman()
        start_state.initialize(lay, list_player)
        problem = CornersProblem(agent, start_state)
        solution = astar(problem, cornersHeuristic)
        handle.write('cost: "%d"\n' % len(solution))
        handle.write('path: """\n%s\n"""\n' % wrap_solution(solution))
        handle.write('thresholds: "2000 1600 1200"\n')
        handle.close()
        return True
