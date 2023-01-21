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


class QuestionPassAllTestsExtraCredit(Question):

    def execute(self, grader: Grader) -> bool:

        # TODO: is this the right way to use grader?  The autograder doesn't seem to use it.
        grader.assignZeroCredit()
        bool_test_failed = False

        test_case: TestCase
        callable_that_wraps_test_case: TYPE_CALLABLE_THAT_NEEDS_GRADER

        for test_case, callable_that_wraps_test_case in self.list_tuple__test_case__callable_that_wraps_test_case:
            if not callable_that_wraps_test_case(grader):
                bool_test_failed = True

        if bool_test_failed:
            grader.fail("Tests failed.")
            return False
        else:
            grader.assignFullCredit()
            grader.addPoints(self.INT_POINTS_EXTRA)

        return True
