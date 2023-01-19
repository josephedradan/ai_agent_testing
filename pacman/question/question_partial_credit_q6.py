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


class QuestionPartialCreditQ6(Question):
    """
    Fails any test which returns False, otherwise doesn't effect the grader object.
    Partial credit tests will add the required points.
    """

    def execute(self, grader: Grader) -> bool:
        grader.assignZeroCredit()

        list_bool = []

        test_case: TestCase
        callable_that_wraps_test_case: TYPE_CALLABLE_THAT_NEEDS_GRADER

        for test_case, callable_that_wraps_test_case in self.list_tuple__test_case__callable_that_wraps_test_case:
            list_bool.append(callable_that_wraps_test_case(grader))

        if False in list_bool:
            grader.assignZeroCredit()
            return False

        return True
