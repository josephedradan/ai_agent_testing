"""
Date created: 1/18/2023

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
# Question in which predict credit is given for test cases with a ``points'' property.
# All other tests are mandatory and must be passed.
from common.grader import Grader
from pacman.question import Question
from pacman.test_case import TestCase
from pacman.types_ import TYPE_CALLABLE_THAT_NEEDS_GRADER


class QuestionPartialCreditHacked(Question):

    def execute(self, grader: Grader) -> bool:
        """
        Notes:
            bool_a_test_has_failed = False

            Loop over all callable_that_wraps_test_case
                Get points if test succeeded
                If callable_that_wraps_test_case failed
                    bool_a_test_has_failed = True
            return bool_a_test_has_failed
        """
        grader.assignZeroCredit()

        points_earned: int = 0
        bool_a_test_has_failed: bool = False

        test_case: TestCase
        callable_that_wraps_test_case: TYPE_CALLABLE_THAT_NEEDS_GRADER

        for test_case, callable_that_wraps_test_case in self.list_tuple__test_case__callable_that_wraps_test_case:

            bool_test_passed: bool = callable_that_wraps_test_case(grader)

            if bool_test_passed:
                if "points" in test_case.dict_file_test:
                    points_earned += int(test_case.dict_file_test["points"])

                if not bool_a_test_has_failed:
                    bool_a_test_has_failed = True

        if points_earned == self.INT_POINTS_MAX and not bool_a_test_has_failed:
            grader.assignZeroCredit()
        else:
            grader.addPoints(points_earned)

        return bool_a_test_has_failed
