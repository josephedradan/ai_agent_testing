"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/13/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
### q8
from hashlib import sha1
from typing import Any
from typing import Dict

from pacman.analysis import question8
from common.grader import Grader
from pacman.test_case import TestCase


class Question8Test(TestCase):

    def __init__(self, question, testDict):
        super(Question8Test, self).__init__(question, testDict)

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        studentSolution = question8()
        studentSolution = str(studentSolution).strip().lower()
        hashedSolution = sha1(studentSolution.encode('utf-8')).hexdigest()
        if hashedSolution == '46729c96bb1e4081fdc81a8ff74b3e5db8fba415':
            return self._procedure_test_pass(grader)
        else:
            self.addMessage("Solution is not correct.")
            self.addMessage("   Student solution: %s" % (studentSolution,))
            return self._procedure_test_fail(grader)

    def write_solution(self, path_file_solution: str) -> bool:
        handle = open(path_file_solution, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path_file_test)
        handle.write('# File intentionally blank.\n')
        handle.close()
        return True