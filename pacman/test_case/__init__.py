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

# Template modeling a generic test case
from typing import TYPE_CHECKING
from typing import Type
from typing import Union

from pacman.test_case.test_case import TestCase
from pacman.test_case.test_case_closest_dot_test import ClosestDotTest
from pacman.test_case.test_case_corner_heuristic_pacman import CornerHeuristicPacman
from pacman.test_case.test_case_corner_heuristic_sanity import CornerHeuristicSanity
from pacman.test_case.test_case_corner_problem_test import CornerProblemTest
from pacman.test_case.test_case_eval_agent_test import EvalAgentTest
from pacman.test_case.test_case_graph_game_tree_test import GraphGameTreeTest
from pacman.test_case.test_case_graph_game_tree_test import MultiagentTreeState
from pacman.test_case.test_case_graph_search_tes import GraphSearchTest
from pacman.test_case.test_case_heuristic_grade import HeuristicGrade
from pacman.test_case.test_case_heuristic_test import HeuristicTest
from pacman.test_case.test_case_pacman_game_tree_test import PacmanGameTreeTest
from pacman.test_case.test_case_pacman_search_test import PacmanSearchTest

if TYPE_CHECKING:
    pass

LIST_TEST_CASE_SUBCLASS = [
    ClosestDotTest,
    CornerHeuristicPacman,
    CornerHeuristicSanity,
    CornerProblemTest,
    MultiagentTreeState,
    GraphSearchTest,
    HeuristicGrade,
    HeuristicTest,
    PacmanSearchTest,
    #
    PacmanGameTreeTest,
    EvalAgentTest,
    GraphGameTreeTest,

]

DICT_K_NAME_TEST_CASE_SUBCLASS_V_TEST_CASE_SUBCLASS = {
    test_case_subclass_.__name__: test_case_subclass_ for test_case_subclass_ in LIST_TEST_CASE_SUBCLASS
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
