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
# Class which models a question in a project.  Note that questions have a
# maximum number of points they are worth, and are composed of a series of
# test cases

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from types import FunctionType
from typing import Any
from typing import Dict
from typing import Type
from typing import Union

from multiagent.graphics.graphics import Graphics


def get_class_question_subclass(name_question_subclass: Union[str, Type[Question], None]) -> Type[Question]:
    question_subclass = name_question_subclass

    if isinstance(name_question_subclass, str):
        question_subclass = Question.DICT_K_NAME_QUESTION_SUBCLASSE_V_QUESTION_SUBCLASS.get(
            name_question_subclass
        )

    if question_subclass is None:
        raise Exception("{} is not a valid Question subclass".format(name_question_subclass))

    return question_subclass


class Question(ABC):
    DICT_K_NAME_QUESTION_SUBCLASSE_V_QUESTION_SUBCLASS = {}

    def __init__(self, dict_question: Dict[str, Any], display: Graphics):
        self.POINTS_MAX = int(dict_question['max_points'])
        self.testCases = []
        self.display: Graphics = display

    def __init_subclass__(cls, **kwargs):
        cls.DICT_K_NAME_QUESTION_SUBCLASSE_V_QUESTION_SUBCLASS[cls.__name__] = cls

    # def raiseNotDefined(self):
    #     print('Method not implemented: %s' % inspect.stack()[1][3])
    #     sys.exit(1)

    def get_display(self) -> Graphics:
        return self.display

    def get_max_points(self) -> int:
        return self.POINTS_MAX

    def add_test_case(self, name_test_case, function: FunctionType):
        """
        Note that 'function' must be a function which accepts a single argument,
        namely a 'grading' object

        :param name_test_case:
        :param function:
        :return:
        """
        self.testCases.append((name_test_case, function))

    @abstractmethod
    def execute(self, grades):
        pass


# Question in which all test cases must be passed in order to receive credit
class PassAllTestsQuestion(Question):

    def execute(self, grades):
        # TODO: is this the right way to use grades?  The autograder doesn't seem to use it.
        testsFailed = False
        grades.assignZeroCredit()
        for _, f in self.testCases:
            if not f(grades):
                testsFailed = True
        if testsFailed:
            grades.fail("Tests failed.")
        else:
            grades.assignFullCredit()


class ExtraCreditPassAllTestsQuestion(Question):
    def __init__(self, dict_question, display):
        Question.__init__(self, dict_question, display)
        self.extraPoints = int(dict_question['extra_points'])

    def execute(self, grades):
        raise Exception("JOSEPH THIS FUNCTION IS CALLED execute")
        # TODO: is this the right way to use grades?  The autograder doesn't seem to use it.
        testsFailed = False
        grades.assignZeroCredit()
        for _, f in self.testCases:
            if not f(grades):
                testsFailed = True
        if testsFailed:
            grades.fail("Tests failed.")
        else:
            grades.assignFullCredit()
            grades.addPoints(self.extraPoints)


# Question in which predict credit is given for test cases with a ``points'' property.
# All other tests are mandatory and must be passed.
class HackedPartialCreditQuestion(Question):

    def execute(self, grades):
        # TODO: is this the right way to use grades?  The autograder doesn't seem to use it.
        grades.assignZeroCredit()

        points = 0
        passed = True
        for testCase, f in self.testCases:
            testResult = f(grades)
            if "points" in testCase.dict_test:
                if testResult:
                    points += float(testCase.dict_test["points"])
            else:
                passed = passed and testResult

        # FIXME: Below terrible hack to match q3's logic
        if int(points) == self.POINTS_MAX and not passed:
            grades.assignZeroCredit()
        else:
            grades.addPoints(int(points))


class Q6PartialCreditQuestion(Question):
    """Fails any test which returns False, otherwise doesn't effect the grades object.
    Partial credit tests will add the required points."""

    def execute(self, grades):
        grades.assignZeroCredit()

        results = []
        for _, f in self.testCases:
            results.append(f(grades))
        if False in results:
            grades.assignZeroCredit()


class PartialCreditQuestion(Question):
    """Fails any test which returns False, otherwise doesn't effect the grades object.
    Partial credit tests will add the required points."""

    def execute(self, grades):
        grades.assignZeroCredit()

        for _, f in self.testCases:
            if not f(grades):
                grades.assignZeroCredit()
                grades.fail("Tests failed.")
                return False


class NumberPassedQuestion(Question):
    """Grade is the number of test cases passed."""

    def execute(self, grades):
        grades.addPoints([f(grades) for _, f in self.testCases].count(True))
