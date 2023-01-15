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

if TYPE_CHECKING:
    pass


def get_class_question_subclass(name_question_subclass: Union[str, Type[Question], None]) -> Type[Question]:
    question_subclass = name_question_subclass

    if isinstance(name_question_subclass, str):
        question_subclass = Question.DICT_K_NAME_QUESTION_SUBCLASS_V_QUESTION_SUBCLASS.get(
            name_question_subclass
        )

    if question_subclass is None:
        raise Exception("{} is not a valid Question subclass".format(name_question_subclass))

    return question_subclass
