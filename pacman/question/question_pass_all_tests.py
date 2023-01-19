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
# Question in which all test cases must be passed in order to receive credit
from pacman.grader import Grader
from pacman.question import Question


class PassAllTestsQuestion(Question):

    def execute(self, grader: Grader):
        # TODO: is this the right way to use grader?  The autograder doesn't seem to use it.
        testsFailed = False
        grader.assignZeroCredit()
        for _, f in self.list_tuple__test_case__callable_that_wraps_test_case:
            if not f(grader):
                testsFailed = True
        if testsFailed:
            grader.fail("Tests failed.")
        else:
            grader.assignFullCredit()