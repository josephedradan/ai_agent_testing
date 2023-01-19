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


class NumberPassedQuestion(Question):
    """Grade is the number of test cases passed."""

    def execute(self, grader: Grader):
        grader.addPoints([f(grader) for _, f in self.list_tuple__test_case__callable_that_wraps_test_case].count(True))
