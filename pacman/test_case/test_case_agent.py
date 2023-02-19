"""
Date created: 2/9/2023

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
from abc import ABC
from typing import Any
from typing import Dict

from pacman.question import Question
from pacman.test_case import TestCase


class TestCaseAgent(TestCase, ABC):

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        super().__init__(question, dict_file_test)

        self.str_class_agent: str = self.dict_file_test['agent']
        self.depth: int = int(self.dict_file_test['depth'])