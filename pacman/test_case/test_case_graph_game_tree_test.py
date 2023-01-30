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

from collections import defaultdict
from typing import Any
from typing import Dict
from typing import List
from typing import Set
from typing import TYPE_CHECKING
from typing import Tuple

from common.game_state import GameState
from pacman.agent import *
from pacman.test_case.game_state_multi_agent_tree_state import MultiAgentTreeState
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from pacman.question.question import Question
    from common.grader import Grader


class MultiagentTreeProblem(object):
    def __init__(self,
                 num_agents: int,
                 state_start: str,
                 set_state_win: Set[str],
                 set_state_lose: Set[str],
                 list_successor: List[Tuple[str, str, str]],
                 dict_evaluation_k_state_v_value: Dict[str, float]
                 ):

        self.state_start: MultiAgentTreeState = MultiAgentTreeState(self, state_start)

        self.num_agents:int = num_agents
        self.set_state_win: Set[str] = set_state_win
        self.set_state_lose: Set[str] = set_state_lose
        self.dict_evaluation_k_state_v_value: Dict[str, float] = dict_evaluation_k_state_v_value
        self.list_successor: List[Tuple[str, str, str]] = list_successor

        self.reset()

        self.stateToSuccessorMap = defaultdict(dict)
        self.stateToActions = defaultdict(list)

        for state, action, nextState in list_successor:
            self.stateToActions[state].append(action)
            self.stateToSuccessorMap[state][action] = nextState

    def reset(self):
        self.generatedStates = set([self.state_start.state])


def get_multi_agent_tree_problem_from_dict_file_test(dict_file_test: Dict[str, Any]) -> MultiagentTreeProblem:
    num_agents: int = int(dict_file_test["num_agents"])
    state_start: str = dict_file_test["start_state"]
    set_state_win: Set[str] = set(dict_file_test["win_states"].split(" "))
    set_state_lose: Set[str] = set(dict_file_test["lose_states"].split(" "))
    list_successor: List[Tuple[str, str, str]] = []

    dict_evaluation_k_state_v_value: Dict[str, float] = {}

    for line in dict_file_test["evaluation"].split('\n'):
        tokens = line.split()
        if len(tokens) == 2:
            state, value = tokens
            dict_evaluation_k_state_v_value[state] = float(value)
        else:
            raise Exception("[parseTree] Bad evaluation line: |%s|" % (line,))

    for line in dict_file_test["successors"].split('\n'):
        tokens = line.split()
        if len(tokens) == 3:
            state, action, nextState = tokens
            list_successor.append((state, action, nextState))
        else:
            raise Exception("[parseTree] Bad successor line: |%s|" % (line,))

    return MultiagentTreeProblem(num_agents, state_start, set_state_win, set_state_lose, list_successor,
                                 dict_evaluation_k_state_v_value)


class GraphGameTreeTest(TestCase):

    def __init__(self, question: Question, dict_test: Dict[str, Any]):
        super(GraphGameTreeTest, self).__init__(question, dict_test)

        self.problem_multi_agent_tree: MultiagentTreeProblem = get_multi_agent_tree_problem_from_dict_file_test(dict_test)

        self.str_class_agent: str  = self.dict_file_test['agent']
        self.diagram = self.dict_file_test['diagram'].split('\n')
        self.depth = int(self.dict_file_test['depth'])

    def _solve_problem(self):
        """

        Notes:
            Create agent
            Give

        """
        self.problem_multi_agent_tree.reset()
        # agent_being_tested = getattr(multiAgents, self.str_class_agent)(depth=self.depth)

        agent_being_tested: Agent = get_subclass_agent(self.str_class_agent)(depth=self.depth)

        action = agent_being_tested.getAction(self.problem_multi_agent_tree.state_start)
        generated = self.problem_multi_agent_tree.generatedStates

        return action, " ".join([str(s) for s in sorted(generated)])

    def _add_diagram_to_message(self):
        self.add_message_to_messages('Tree:')

        for line in self.diagram:
            self.add_message_to_messages(line)

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # multiAgents = moduleDict['projectTestClasses']

        goldAction = dict_file_solution['action']
        goldGenerated = dict_file_solution['generated']
        action, generated = self._solve_problem()

        fail = False
        if action != goldAction:
            self.add_message_to_messages('Incorrect move for depth=%s' % (self.depth,))
            self.add_message_to_messages(
                '    Student move: %s\n    Optimal move: %s' % (action, goldAction))
            fail = True

        if generated != goldGenerated:
            self.add_message_to_messages(
                'Incorrect generated nodes for depth=%s' % (self.depth,))
            self.add_message_to_messages('    Student generated nodes: %s\n    Correct generated nodes: %s' % (
                generated, goldGenerated))
            fail = True

        if fail:
            self._add_diagram_to_message()
            return self._procedure_test_fail(grader)
        else:
            return self._procedure_test_pass(grader)

    def write_solution(self, path_file_solution: str) -> bool:
        # multiAgents = moduleDict['projectTestClasses']
        action, generated = self._solve_problem()

        with open(path_file_solution, 'w') as handle:
            handle.write('# This is the solution file for %s.\n' % self.path_file_test)
            handle.write('action: "%s"\n' % (action,))
            handle.write('generated: "%s"\n' % (generated,))
        return True
