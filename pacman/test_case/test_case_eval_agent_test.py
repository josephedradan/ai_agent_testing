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

import random
import time
from pprint import pprint
from typing import Any
from typing import Dict
from typing import List
from typing import TYPE_CHECKING

from pacman import main
from pacman.agent import *  # IMPORTANT: THIS IS NEEDED FOR eval TO WORK CORRECTLY
from pacman.game.game import Game
from pacman.game.layout import get_layout
from pacman.main import arg_parser_pacman
from pacman.main import run_pacman_games
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from pacman.question.question import Question
    from common.grader import Grader


class EvalAgentTest(TestCase):

    def __init__(self,
                 question: Question,
                 dict_file_test: Dict[str, Any]):

        super(EvalAgentTest, self).__init__(question, dict_file_test)

        self.__special_condition = False

        pacman_args = dict_file_test.get('pacmanParams')
        if pacman_args and isinstance(pacman_args, str):
            self.dict_file_test.update(arg_parser_pacman(pacman_args.split()))
            pprint("LKL")
            pprint(arg_parser_pacman(pacman_args.split()))
            pprint("LKL")

            self.__special_condition = True

        if not self.__special_condition:
            self.name_layout: Union[str] = dict_file_test.get('layoutName')
            self.name_class_agent: Union[str] = dict_file_test.get('agentName')
            self.list_agent_ghost: List[Agent] = eval(dict_file_test['ghosts'])
            self.maxTime: int = int(dict_file_test['maxTime'])
            self.seed: int = int(dict_file_test['randomSeed'])
            self.number_of_games: int = int(dict_file_test['numGames'])
        else:
            # Note that the only shared variable is number_of_games when self.__special_condition is True
            self.number_of_games = self.dict_file_test['number_of_games']

        self.scoreMinimum = int(dict_file_test['scoreMinimum']) if 'scoreMinimum' in dict_file_test else None
        self.nonTimeoutMinimum = int(
            dict_file_test['nonTimeoutMinimum']) if 'nonTimeoutMinimum' in dict_file_test else None
        self.winsMinimum = int(
            dict_file_test['winsMinimum']) if 'winsMinimum' in dict_file_test else None

        self.scoreThresholds = [int(s) for s in dict_file_test.get(
            'scoreThresholds', '').split()]
        self.nonTimeoutThresholds = [int(s) for s in dict_file_test.get(
            'nonTimeoutThresholds', '').split()]
        self.winsThresholds = [int(s) for s in dict_file_test.get(
            'winsThresholds', '').split()]

        self.maxPoints = sum([len(t) for t in [
            self.scoreThresholds, self.nonTimeoutThresholds, self.winsThresholds]])
        self.agentArgs = dict_file_test.get('agentArgs', '')

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:

        time_start = time.time()

        if self.__special_condition:

            list_game = run_pacman_games(**self.dict_file_test)

        else:

            # TODO: multiAgents TO 'projectTestClasses'
            # class_agent = getattr(moduleDict['projectTestClasses'], self.str_class_agent)

            class_agent: Type[Agent] = get_subclass_agent(self.name_class_agent)

            agentOpts = main.get_dict_kwargs(self.agentArgs) if self.agentArgs != '' else {}

            agent_object: Agent = class_agent(**agentOpts)

            layout_ = get_layout(self.name_layout, 3)

            graphics_pacman = self.question.get_graphics_pacman()

            random.seed(self.seed)

            list_game: List[Game] = run_pacman_games(
                layout_,
                agent_object,
                self.list_agent_ghost,
                graphics_pacman,
                self.number_of_games,
                bool_record=False,
                bool_catch_exceptions=True,
                timeout=self.maxTime
            )

        time_total = time.time() - time_start

        stats = {'time': time_total,
                 'wins': [g.game_state.isWin() for g in list_game].count(True),
                 'games': list_game,
                 'scores': [g.game_state.getScore() for g in list_game],
                 'timeouts': [g.agentTimeout for g in list_game].count(True),
                 'crashes': [g.agentCrashed for g in list_game].count(True)}

        averageScore = sum(stats['scores']) / float(len(stats['scores']))
        nonTimeouts = self.number_of_games - stats['timeouts']
        wins = stats['wins']

        def gradeThreshold(value, minimum, thresholds, name):
            points = 0
            passed = (minimum == None) or (value >= minimum)
            if passed:
                for t in thresholds:
                    if value >= t:
                        points += 1
            return (passed, points, value, minimum, thresholds, name)

        results = [
            gradeThreshold(
                averageScore,
                self.scoreMinimum,
                self.scoreThresholds,
                "average score"
            ),
            gradeThreshold(
                nonTimeouts,
                self.nonTimeoutMinimum,
                self.nonTimeoutThresholds,
                "Games not timed out"
            ),
            gradeThreshold(
                wins,
                self.winsMinimum,
                self.winsThresholds,
                "wins"
            )
        ]

        totalPoints = 0
        for passed, points, value, minimum, thresholds, name in results:
            if minimum == None and len(thresholds) == 0:
                continue

            # print passed, points, value, minimum, thresholds, test_case_object
            totalPoints += points
            if not passed:
                assert points == 0
                self.addMessage(
                    "%s %s (fail: below minimum value %s)" % (value, name, minimum))
            else:
                self.addMessage("%s %s (%s of %s points)" %
                                (value, name, points, len(thresholds)))

            if minimum != None:
                self.addMessage("    Grading scheme:")
                self.addMessage("     < %s:  fail" % (minimum,))
                if len(thresholds) == 0 or minimum != thresholds[0]:
                    self.addMessage("    >= %s:  0 points" % (minimum,))
                for idx, threshold in enumerate(thresholds):
                    self.addMessage("    >= %s:  %s points" %
                                    (threshold, idx + 1))
            elif len(thresholds) > 0:
                self.addMessage("    Grading scheme:")
                self.addMessage("     < %s:  0 points" % (thresholds[0],))
                for idx, threshold in enumerate(thresholds):
                    self.addMessage("    >= %s:  %s points" %
                                    (threshold, idx + 1))

        if any([not passed for passed, _, _, _, _, _ in results]):
            totalPoints = 0

        return self._procedure_test_pass_extra_credit(grader, totalPoints, self.maxPoints)

    def write_solution(self, path_file_solution: str) -> bool:
        handle = open(path_file_solution, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path_file_test)
        handle.write('# File intentionally blank.\n')
        handle.close()
        return True
