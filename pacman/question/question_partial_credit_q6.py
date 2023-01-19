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


class Q6PartialCreditQuestion(Question):
    """Fails any test which returns False, otherwise doesn't effect the grader object.
    Partial credit tests will add the required points."""

    def execute(self, grader: Grader):
        grader.assignZeroCredit()

        results = []
        for _, f in self.list_tuple__test_case__callable_that_wraps_test_case:
            results.append(f(grader))
        if False in results:
            grader.assignZeroCredit()
