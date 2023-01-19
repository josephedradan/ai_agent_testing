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
# Question in which predict credit is given for test cases with a ``points'' property.
# All other tests are mandatory and must be passed.
from pacman.grader import Grader
from pacman.question import Question
from pacman.test_case import TestCase
from pacman.types_ import TYPE_CALLABLE_THAT_NEEDS_GRADER


class QuestionPartialCreditHacked(Question):

    def execute(self, grader: Grader) -> bool:
        grader.assignZeroCredit()

        points_earned = 0
        passed = True

        test_case: TestCase
        callable_that_wraps_test_case: TYPE_CALLABLE_THAT_NEEDS_GRADER

        for test_case, callable_that_wraps_test_case in self.list_tuple__test_case__callable_that_wraps_test_case:

            bool_test_passed: bool = callable_that_wraps_test_case(grader)

            if "points" in test_case.dict_file_test:
                if bool_test_passed:
                    points_earned += float(test_case.dict_file_test["points"])
            else:
                passed = passed and bool_test_passed

        # FIXME: Below terrible hack to match q3's logic
        if int(points_earned) == self.POINTS_MAX and not passed:
            grader.assignZeroCredit()
            return passed
        else:
            grader.addPoints(int(points_earned))

        return passed
