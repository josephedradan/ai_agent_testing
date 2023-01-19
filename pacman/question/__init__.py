"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/14/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Type
from typing import Union

from pacman.question.question import Question
from pacman.question.question_partial_credit import QuestionPartialCredit
from pacman.question.question_partial_credit_hacked import QuestionPartialCreditHacked
from pacman.question.question_partial_credit_q6 import QuestionPartialCreditQ6
from pacman.question.question_pass_all_tests import QuestionPassAllTests
from pacman.question.question_pass_all_tests_basic import QuestionNumberPassed
from pacman.question.question_pass_all_tests_extra_credit import QuestionPassAllTestsExtraCredit

if TYPE_CHECKING:
    pass


def get_subclass_question(name_subclass_question: Union[str, Type[Question], None]) -> Type[Question]:
    question_subclass = name_subclass_question

    if isinstance(name_subclass_question, str):
        question_subclass = Question.DICT_K_NAME_SUBCLASS_QUESTION_V_SUBCLASS_QUESTION.get(
            name_subclass_question
        )

    if question_subclass is None:
        raise Exception("{} is not a valid Question subclass".format(name_subclass_question))

    return question_subclass
