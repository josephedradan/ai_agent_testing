"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/18/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from pacman.grader import Grader
from pacman.question import Question
from pacman.test_case import TestCase
from pacman.types_ import TYPE_CALLABLE_THAT_NEEDS_GRADER


class QuestionNumberPassed(Question):
    """Grade is the number of test cases passed."""

    def execute(self, grader: Grader) -> bool:
        test_case: TestCase
        callable_that_wraps_test_case: TYPE_CALLABLE_THAT_NEEDS_GRADER

        grader.addPoints(
            [callable_that_wraps_test_case(grader) for test_case, callable_that_wraps_test_case
             in self.list_tuple__test_case__callable_that_wraps_test_case].count(True)
        )
        return True
