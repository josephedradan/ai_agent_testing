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
from pacman.agent.search.search import bfs
from pacman.agent.search_problem import CornersProblem
from pacman.game.actions import Actions
from pacman.game.layoutpacman import LayoutPacman
from pacman.game.player import Player
from pacman.game.type_player import TypePlayer
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from pacman.question.question import Question
    from common.grader import Grader


def getStatesFromPath(start, path):
    "Returns the list of states visited along the path"
    vis = [start]
    curr = start
    for a in path:
        x, y = curr
        dx, dy = Actions.directionToVector(a)
        curr = (int(x + dx), int(y + dy))
        vis.append(curr)
    return vis


class CornerProblemTest(TestCase):

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        super(CornerProblemTest, self).__init__(question, dict_file_test)

        self.str_layout: Union[str, None] = dict_file_test.get('layout')

        self.name_layout: Union[str, None] = dict_file_test.get('layoutName')

    def solution(self):
        lay = LayoutPacman([l.strip() for l in self.str_layout.split('\n')])

        agent: Agent = AgentPacman()  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        list_player = [Player(agent, TypePlayer.PACMAN)]  # TODO: VERY GHETTO, MAKE GOOD SOLUTION

        ################

        state_pacman = StatePacman()
        state_pacman.initialize(lay, list_player)

        problem = CornersProblem(agent, state_pacman)
        path = bfs(problem)

        state_pacman = StatePacman()
        state_pacman.initialize(lay, list_player)
        print("---- FUCK SOLUTION",list_player, state_pacman.get_dict_k_player_v_container_state())
        visited = getStatesFromPath(state_pacman.getPacmanPosition(), path)
        top, right = state_pacman.getWalls().height - 2, state_pacman.getWalls().width - 2
        missedCorners = [p for p in ((1, 1), (1, top), (right, 1), (right, top)) if p not in visited]

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
        grader.addMessage('\tpacman str_path_layout:\t\t%s' % self.name_layout)
        grader.addMessage('\tsolution length:\t\t%s' % len(solution))
        return True

    def write_solution(self, path_file_solution: str) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']

        # open file and write comments
        handle = open(path_file_solution, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path_file_test)

        print("Solving problem_multi_agent_tree", self.name_layout)
        print(self.str_layout)

        path, _ = self.solution()
        length = len(path)
        print("Problem solved")

        handle.write('solution_length: "%s"\n' % length)
        handle.close()
