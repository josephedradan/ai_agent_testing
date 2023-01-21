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


class QuestionPartialCredit(Question):

    def execute(self, grader: Grader) -> bool:
        """
        Fails any test which returns False, otherwise doesn't effect the grader object.
        Partial credit tests will add the required points.

        Notes:
            Loop over all callable_that_wraps_test_case
                If a callable_that_wraps_test_case fails:
                    Get no credit
                    return False
            return True

        """
        grader.assignZeroCredit()

        test_case: TestCase
        callable_that_wraps_test_case: TYPE_CALLABLE_THAT_NEEDS_GRADER

        for test_case, callable_that_wraps_test_case in self.list_tuple__test_case__callable_that_wraps_test_case:
            if not callable_that_wraps_test_case(grader):
                grader.assignZeroCredit()
                grader.fail("Tests failed.")
                return False

        return True
