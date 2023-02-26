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
from pacman.agent import AgentPacman
from pacman.agent import ClosestDotSearchAgent
from pacman.game.layout_pacman import LayoutPacman
from pacman.game.player_pacman import PlayerPacman
from pacman.game.type_player_pacman import EnumPlayerPacman
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from common.grader import Grader
    from pacman.question import Question


class ClosestDotTest(TestCase):

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        super(ClosestDotTest, self).__init__(question, dict_file_test)

        self.str_layout: Union[str, None] = dict_file_test.get('layout_text')

        self.name_layout: Union[str, None] = dict_file_test.get('layout_name')

    def _get_solution(self) -> Any:
        layout = LayoutPacman([l.strip() for l in self.str_layout.split('\n')])

        state_pacman_start = StatePacman()
        state_pacman_start.initialize(layout, [PlayerPacman(self.question.get_graphics().get_gui(),
                                                            self.question.get_graphics(),
                                                            AgentPacman(),
                                                            EnumPlayerPacman.PACMAN)])

        path = ClosestDotSearchAgent().get_list_action_to_closest_dot(state_pacman_start)
        return path

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:

        length_solution = int(dict_file_solution['solution_length'])

        solution = self._get_solution()

        if not isinstance(solution, list):
            grader.addMessage(f'FAIL: {self.path_file_test}')
            grader.addMessage(f'\tThe result must be a list. (Instead, it is {type(solution)})')
            return False

        if len(solution) != length_solution:
            grader.addMessage(f'FAIL: {self.path_file_test}')
            grader.addMessage('Closest dot not found.')
            grader.addMessage(f'\tstudent solution length:\n{len(solution)}')
            grader.addMessage('')
            grader.addMessage(f'\tcorrect solution length:\n{length_solution}')
            return False

        grader.addMessage(f'PASS: {self.path_file_test}')
        grader.addMessage(f'\tpacman str_path_layout:\t\t{self.name_layout}')
        grader.addMessage(f'\tsolution length:\t\t{len(solution)}')
        return True

    def write_solution(self, path_file_solution: str) -> bool:

        # open file and write comments
        with open(path_file_solution, 'w') as file_obj:
            file_obj.write(f'# This is the solution file for {self.path_file_test}.\n')

            print("Solving problem_multi_agent_tree", self.name_layout)
            print(self.str_layout)

            length = len(self._get_solution())
            print("Problem solved")

            file_obj.write('solution_length: "%s"\n' % length)
            file_obj.close()

        return True
