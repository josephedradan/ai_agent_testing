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
    from pacman.question import Question


class ClosestDotTest(TestCase):

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        super(ClosestDotTest, self).__init__(question, dict_file_test)

        self.str_layout: Union[str, None] = dict_file_test.get('layout')

        self.name_layout: Union[str, None] = dict_file_test.get('layoutName')

    def _get_solution(self) -> Any:
        layout = Layout([l.strip() for l in self.str_layout.split('\n')])

        game_state_initial = GameState()
        game_state_initial.initialize(layout, 0)

        path = ClosestDotSearchAgent().findPathToClosestDot(game_state_initial)
        return path

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:

        gold_length = int(dict_file_solution['solution_length'])

        solution = self._get_solution()

        if not isinstance(solution, list):
            grader.addMessage(f'FAIL: {self.path_file_test}')
            grader.addMessage(f'\tThe result must be a list. (Instead, it is {type(solution)})')
            return False

        if len(solution) != gold_length:
            grader.addMessage(f'FAIL: {self.path_file_test}')
            grader.addMessage('Closest dot not found.')
            grader.addMessage(f'\tstudent solution length:\n{len(solution)}')
            grader.addMessage('')
            grader.addMessage(f'\tcorrect solution length:\n{gold_length}')
            return False

        grader.addMessage(f'PASS: {self.path_file_test}')
        grader.addMessage(f'\tpacman layout:\t\t{self.name_layout}')
        grader.addMessage(f'\tsolution length:\t\t{len(solution)}')
        return True

    def write_solution(self, path_file_solution: str) -> bool:

        # open file and write comments
        with open(path_file_solution, 'w') as file_obj:
            file_obj.write(f'# This is the solution file for {self.path_file_test}.\n')

            print("Solving problem", self.name_layout)
            print(self.str_layout)

            length = len(self._get_solution())
            print("Problem solved")

            file_obj.write('solution_length: "%s"\n' % length)
            file_obj.close()

        return True
