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


class HackedPartialCreditQuestion(Question):

    def execute(self, grader: Grader):
        # TODO: is this the right way to use grader?  The autograder doesn't seem to use it.
        grader.assignZeroCredit()

        points = 0
        passed = True
        for testCase, f in self.list_tuple__test_case__callable_that_wraps_test_case:
            testResult = f(grader)
            if "points" in testCase.dict_file_test:
                if testResult:
                    points += float(testCase.dict_file_test["points"])
            else:
                passed = passed and testResult

        # FIXME: Below terrible hack to match q3's logic
        if int(points) == self.POINTS_MAX and not passed:
            grader.assignZeroCredit()
        else:
            grader.addPoints(int(points))