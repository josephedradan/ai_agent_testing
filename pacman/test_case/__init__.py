"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/12/2023

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

import json
import random
from abc import ABC
# Template modeling a generic test case
from abc import abstractmethod
from collections import defaultdict
from pprint import pprint
from typing import Any
from typing import Dict
from typing import List
from typing import TYPE_CHECKING

from pacman import main

from pacman.agent import *
from pacman.game import layout
from pacman.game.layout import Layout
from pacman.game.layout import get_layout
from pacman.graphics.graphics_pacman import GraphicsPacman
from pacman.main import run_pacman_games
from pacman.multiagentTestClasses import GradingAgent
from pacman.test_case.test_case import TestCase
from pacman.test_case.test_case_eval_agent_test import EvalAgentTest
from pacman.test_case.test_case_graph_game_tree_test import GraphGameTreeTest
from pacman.test_case.test_case_pacman_game_tree_test import PacmanGameTreeTest

if TYPE_CHECKING:
    from pacman.game.game_state import GameState
    from pacman._question import Question
    from pacman.grader import Grader

LIST_TEST_CASE_SUBCLASS =[
    PacmanGameTreeTest,
    EvalAgentTest,
    GraphGameTreeTest,

]

DICT_K_NAME_TEST_CASE_SUBCLASS_V_TEST_CASE_SUBCLASS = {
    test_case_subclass_.__name__ : test_case_subclass_ for test_case_subclass_ in LIST_TEST_CASE_SUBCLASS
}

def get_class_test_case_subclass(name_test_case_subclass: str) -> Type[TestCase]:
    test_case_subclass: Union[Type[TestCase], str] = name_test_case_subclass

    if isinstance(name_test_case_subclass, str):
        test_case_subclass = DICT_K_NAME_TEST_CASE_SUBCLASS_V_TEST_CASE_SUBCLASS.get(
            name_test_case_subclass
        )

    if test_case_subclass is None:
        raise Exception("{} is not a valid TestCase subclass".format(name_test_case_subclass))

    return test_case_subclass
