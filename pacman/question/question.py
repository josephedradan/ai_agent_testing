# testClasses.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# import modules from python standard library
# Class which models a str_question in a name_project.  Note that questions have a
# maximum number of points they are worth, and are composed of a series of
# test cases

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import TYPE_CHECKING
from typing import Tuple

from pacman.grader import Grader
from pacman.test_case import TestCase

if TYPE_CHECKING:
    from pacman.graphics.graphics_pacman import GraphicsPacman

TYPE_LIST_TUPLE__TEST_CASE__CALLABLE_THAT_WRAPS_TEST_CASE = List[Tuple[TestCase,
                                                                       Callable[[Grader, Dict[str, Any]], bool]]]


class Question(ABC):
    DICT_K_NAME_SUBCLASS_QUESTION_V_SUBCLASS_QUESTION = {}

    def __init__(self, dict_question: Dict[str, Any], graphics_pacman: GraphicsPacman):
        self.POINTS_MAX: int = int(dict_question['max_points'])

        self.list_tuple__test_case__callable_that_wraps_test_case: (
            TYPE_LIST_TUPLE__TEST_CASE__CALLABLE_THAT_WRAPS_TEST_CASE
        ) = []

        self.graphics_pacman: GraphicsPacman = graphics_pacman

    def __init_subclass__(cls, **kwargs):
        cls.DICT_K_NAME_SUBCLASS_QUESTION_V_SUBCLASS_QUESTION[cls.__name__] = cls

    # def raiseNotDefined(self):
    #     print('Method not implemented: %s' % inspect.stack()[1][3])
    #     sys.exit(1)

    def get_graphics_pacman(self) -> GraphicsPacman:
        return self.graphics_pacman

    def get_points_max(self) -> int:
        return self.POINTS_MAX

    def add_test_case_and_callable_that_wraps_test_case(self, test_case_object: TestCase,
                                                        callable_that_wraps_test_case: Callable):
        """
        Note that 'function' must be a function which accepts a single argument,
        namely a 'grading' object

        :param test_case_object:
        :param callable_that_wraps_test_case:
        :return:
        """
        self.list_tuple__test_case__callable_that_wraps_test_case.append(
            (test_case_object, callable_that_wraps_test_case)
        )

    @abstractmethod
    def execute(self, grader: Grader):
        pass
