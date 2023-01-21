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

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pacman.question.question import Question
    from common.grader import Grader


class TestCase(ABC):

    # def raiseNotDefined(self):
    #     print('Method not implemented: %s' % inspect.stack()[1][3])
    #     sys.exit(1)

    # def __init_subclass__(cls, **kwargs):
    #     DICT_K_NAME_TEST_CASE_SUBCLASS_V_TEST_CASE_SUBCLASS[cls.__name__] = cls

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):

        self.question: Question = question

        self.dict_file_test: Dict[str, Any] = dict_file_test

        self.path_file_test: str = dict_file_test.get('path_file_test')

        # self.container_file_test: ContainerFileTest = ContainerFileTest(dict_file_test)

        self.messages: List[str] = []

    def get_path_file_test(self) -> str:
        return self.path_file_test

    # @abstractmethod
    # def __str__(self):
    #     pass
    #     # self.raiseNotDefined()

    @abstractmethod
    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        """
        Responsible for executing actual games

        :param grader:
        :param dict_file_solution:
        :return:
        """
        pass
        # self.raiseNotDefined()

    @abstractmethod
    def write_solution(self, path_file_solution: str) -> bool:
        pass
        # self.raiseNotDefined()
        # return True

    # Tests should call the following messages for grading
    # to ensure a uniform format for test output.
    #
    # TODO: this is hairy, but we need to fix grading.py's interface
    # to get a nice hierarchical name_project - str_question - test structure,
    # then these should be moved into Question proper.
    def _procedure_test_pass(self, grader: Grader):
        grader.addMessage('PASS: %s' % (self.path_file_test,))
        for line in self.messages:
            grader.addMessage('    %s' % (line,))
        return True

    def _procedure_test_fail(self, grader: Grader):
        grader.addMessage('FAIL: %s' % (self.path_file_test,))
        for line in self.messages:
            grader.addMessage('    %s' % (line,))
        return False

    # This should really be str_question level?
    def _procedure_test_pass_extra_credit(self, grader: Grader, points: int, points_max: int) -> bool:
        grader.addPoints(points)
        points_extra_credit = max(0, points - points_max)
        points_regular = points - points_extra_credit

        grader.addMessage('{}: {} ({} of {} points)'.format(
            "PASS" if points >= points_max else "FAIL",
            self.path_file_test,
            points_regular,
            points_max
        ))

        if points_extra_credit > 0:
            grader.addMessage('EXTRA CREDIT: %s points' % (points_extra_credit,))

        for line in self.messages:
            grader.addMessage('    %s' % (line,))

        return True

    def addMessage(self, message):
        self.messages.extend(message.split('\n'))
