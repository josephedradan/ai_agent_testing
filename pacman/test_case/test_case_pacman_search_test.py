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
from pacman.agent import AgentPacman
from pacman.agent.heuristic_function import get_heuristic_function
from pacman.agent.search import get_search_function
from pacman.agent.search_problem import get_subclass_search_problem
from pacman.game.directions import Directions
from pacman.game.layoutpacman import LayoutPacman
from pacman.game.player_pacman import PlayerPacman
from pacman.game.type_player import TypePlayerPacman
from pacman.test_case.common import wrap_solution
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from common.grader import Grader


class PacmanSearchTest(TestCase):

    def __init__(self, question, dict_file_test):
        super(PacmanSearchTest, self).__init__(question, dict_file_test)

        self.layout_text = dict_file_test['layout_text']
        self.alg = dict_file_test['algorithm']
        self.layout_name = dict_file_test['layout_name']

        # TODO: sensible to have defaults like this?
        self.leewayFactor = float(dict_file_test.get('leewayFactor', '1'))
        self.costFn = eval(dict_file_test.get('costFn', 'None'))
        self.searchProblemClassName = dict_file_test.get('searchProblemClass', 'PositionSearchProblem')
        self.heuristicName = dict_file_test.get('heuristic', None)

    def getSolInfo(self):
        # alg = getattr(search, self.alg)
        alg = get_search_function(self.alg)

        lay = LayoutPacman([l.strip() for l in self.layout_text.split('\n')])

        state_pacman_start = StatePacman()
        state_pacman_start.initialize(lay, [PlayerPacman(self.question.get_graphics().get_gui(),
                                                         self.question.get_graphics(),
                                                         AgentPacman(),
                                                         TypePlayerPacman.PACMAN)])

        # class_problem = getattr(searchAgents, self.searchProblemClassName)
        class_problem = get_subclass_search_problem(self.searchProblemClassName)

        problemOptions = {}
        if self.costFn != None:
            problemOptions['costFn'] = self.costFn

        # TODO: Will most likely be PositionSearchProblem (Ctrl+F -> class: "PacmanSearchTest")
        problem_instance = class_problem(state_pacman_start, **problemOptions)

        # heuristic = getattr(searchAgents, self.heuristicName) if self.heuristicName != None else None
        heuristic = get_heuristic_function(self.heuristicName) if self.heuristicName != None else None

        if heuristic != None:
            # TODO: EXAMPLE: depth_first_search(position_search_problem, callable_heuristic)
            solution = alg(problem_instance, heuristic)
        else:
            solution = alg(problem_instance, None)

        if type(solution) != type([]):
            return None, None, 'The result of %s must be a list. (Instead, it is %s)' % (self.alg, type(solution))

        dirs = Directions.LEFT.keys()
        if [el in dirs for el in solution].count(False) != 0:
            return None, None, 'Output of %s must be a list of actions from game.Directions' % self.alg

        expanded = problem_instance._expanded
        return solution, expanded, None

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']
        gold_solution = [str.split(dict_file_solution['solution']), str.split(dict_file_solution['rev_solution'])]
        gold_expanded = max(int(dict_file_solution['expanded_nodes']), int(dict_file_solution['rev_expanded_nodes']))

        solution, expanded, error = self.getSolInfo()

        if error != None:
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('%s' % error)
            return False

        # FIXME: do we want to standardize test output format?

        if solution not in gold_solution:
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('Solution not correct.')
            grader.addMessage('\tstudent solution length: %s' % len(solution))
            grader.addMessage('\tstudent solution:\n%s' % wrap_solution(solution))
            grader.addMessage('')
            grader.addMessage('\tcorrect solution length: %s' % len(gold_solution[0]))
            grader.addMessage('\tcorrect (reversed) solution length: %s' % len(gold_solution[1]))
            grader.addMessage('\tcorrect solution:\n%s' % wrap_solution(gold_solution[0]))
            grader.addMessage('\tcorrect (reversed) solution:\n%s' % wrap_solution(gold_solution[1]))
            return False

        if expanded > self.leewayFactor * gold_expanded and expanded > gold_expanded + 1:
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('Too many node expanded; are you expanding nodes twice?')
            grader.addMessage('\tstudent nodes expanded: %s' % expanded)
            grader.addMessage('')
            grader.addMessage('\tcorrect nodes expanded: %s (leewayFactor %s)' % (gold_expanded, self.leewayFactor))
            return False

        grader.addMessage('PASS: %s' % self.path_file_test)
        grader.addMessage('\tpacman layout name:\t\t%s' % self.layout_name)
        grader.addMessage('\tsolution length: %s' % len(solution))
        grader.addMessage('\tnodes expanded:\t\t%s' % expanded)
        return True

    def write_solution(self, path_file_solution: str) -> bool:  # TODO: DONT KNOW
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']
        # open file and write comments
        handle = open(path_file_solution, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path_file_test)
        handle.write('# This solution is designed to support both right-to-left\n')
        handle.write('# and left-to-right implementations.\n')
        handle.write(
            '# Number of nodes expanded must be with a factor of %s of the numbers below.\n' % self.leewayFactor)

        # write forward solution
        solution, expanded, error = self.getSolInfo()
        if error != None: raise Exception("Error in solution code: %s" % error)
        handle.write('solution: """\n%s\n"""\n' % wrap_solution(solution))
        handle.write('expanded_nodes: "%s"\n' % expanded)

        # write backward solution
        search.REVERSE_PUSH = not search.REVERSE_PUSH
        solution, expanded, error = self.getSolInfo()
        if error != None: raise Exception("Error in solution code: %s" % error)
        handle.write('rev_solution: """\n%s\n"""\n' % wrap_solution(solution))
        handle.write('rev_expanded_nodes: "%s"\n' % expanded)

        # clean up
        search.REVERSE_PUSH = not search.REVERSE_PUSH
        handle.close()
        return True
