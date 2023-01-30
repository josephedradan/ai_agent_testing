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
from pacman.test_case.test_case_epsilon_greedy_test import EpsilonGreedyTest
from pacman.test_case.test_case_eval_agent_test import EvalAgentTest
from pacman.test_case.test_case_graph_game_tree_test import GraphGameTreeTest
from pacman.test_case.test_case_graph_game_tree_test import MultiAgentTreeState
from pacman.test_case.test_case_graph_search_tes import GraphSearchTest
from pacman.test_case.test_case_grid_policy_test import GridPolicyTest
from pacman.test_case.test_case_heuristic_grade import HeuristicGrade
from pacman.test_case.test_case_heuristic_test import HeuristicTest
from pacman.test_case.test_case_pacman_game_tree_test import PacmanGameTreeTest
from pacman.test_case.test_case_pacman_search_test import PacmanSearchTest
from pacman.test_case.test_case_q_learning_approximate_test import ApproximateQLearningTest
from pacman.test_case.test_case_q_learning_test import QLearningTest
from pacman.test_case.test_case_question_8_test import Question8Test
from pacman.test_case.test_case_value_iteration_test import ValueIterationTest
from pacman.test_case.test_case_value_iteration_test_asynchronous import AsynchronousValueIterationTest
from pacman.test_case.test_case_value_iteration_test_prioritized_sweeping import PrioritizedSweepingValueIterationTest

if TYPE_CHECKING:
    pass

LIST_SUBCLASS_TEST_CASE = [
    ClosestDotTest,
    CornerHeuristicPacman,
    CornerHeuristicSanity,
    CornerProblemTest,
    MultiAgentTreeState,
    GraphSearchTest,
    HeuristicGrade,
    HeuristicTest,
    PacmanSearchTest,
    #
    PacmanGameTreeTest,
    EvalAgentTest,
    GraphGameTreeTest,
    # ,
    ValueIterationTest,
    AsynchronousValueIterationTest,
    PrioritizedSweepingValueIterationTest,
    ApproximateQLearningTest,
    QLearningTest,
    EpsilonGreedyTest,
    GridPolicyTest,
    Question8Test,

]

DICT_K_NAME_SUBCLASS_TEST_V_SUBCLASS_TEST_CASE = {
    subclass_test_case_.__name__: subclass_test_case_ for subclass_test_case_ in LIST_SUBCLASS_TEST_CASE
}


def get_subclass_test_case(name_subclass_test_case: Union[str, Type[TestCase], None]) -> Type[TestCase]:
    test_case_subclass: Union[Type[TestCase], str] = name_subclass_test_case

    if isinstance(name_subclass_test_case, str):
        test_case_subclass = DICT_K_NAME_SUBCLASS_TEST_V_SUBCLASS_TEST_CASE.get(
            name_subclass_test_case
        )

    if test_case_subclass is None:
        raise Exception("{} is not a valid TestCase subclass".format(name_subclass_test_case))

    return test_case_subclass
