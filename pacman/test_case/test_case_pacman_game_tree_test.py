"""
Date created: 1/12/2023

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
from __future__ import annotations

import json
import random
import time
from io import TextIOWrapper
from pprint import pprint
from typing import Any
from typing import Dict
from typing import List
from typing import TYPE_CHECKING

from common.common import get_list_agent_from_list_container_object_construct
from pacman.agent import *
from pacman.agent._agent_grading import _GradingAgent
from pacman.game import layout_pacman
from pacman.graphics.graphics_pacman import GraphicsPacman
from pacman.main import run_pacman_games
from pacman.parser import ContainerObjectConstruct
from pacman.parser import get_list_container_object_construct_from_implicit
from pacman.test_case.test_case_agent import TestCaseAgent

if TYPE_CHECKING:
    from common.state import State
    from pacman.question.question import Question
    from common.grader import Grader


# FIXME: THIS HAPPENS TO BE NOT USED
class PolyAgent(Agent):
    def __init__(self, seed, ourPacOptions, depth):
        # prepare our pacman agents
        solutionAgents, alternativeDepthAgents, partialPlyBugAgents = self.construct_our_pacs(
            # multiAgents,
            ourPacOptions
        )

        for p in solutionAgents:
            p.depth = depth
        for p in partialPlyBugAgents:
            p.depth = depth
        for p in alternativeDepthAgents[:2]:
            p.depth = max(1, depth - 1)
        for p in alternativeDepthAgents[2:]:
            p.depth = depth + 1
        self.solutionAgents = solutionAgents
        self.alternativeDepthAgents = alternativeDepthAgents
        self.partialPlyBugAgents = partialPlyBugAgents
        # prepare fields for storing the results
        self.optimalActionLists = []
        self.alternativeDepthLists = []
        self.partialPlyBugLists = []
        self.seed = seed
        self.stepCount = 0

    def select(self, list, indices):
        """
        Return a sublist of elements given by indices in list.
        """
        return [list[i] for i in indices]

    def construct_our_pacs(self, keyword_dict):  # TODO: WTF IS THIS

        multiAgents = None

        pacs_without_stop = [multiAgents.StaffMultiAgentSearchAgent(**keyword_dict) for i in range(3)]

        keyword_dict['keepStop'] = 'True'

        pacs_with_stop = [multiAgents.StaffMultiAgentSearchAgent(**keyword_dict) for i in range(3)]

        keyword_dict['usePartialPlyBug'] = 'True'

        partial_ply_bug_pacs = [multiAgents.StaffMultiAgentSearchAgent(**keyword_dict)]

        keyword_dict['keepStop'] = 'False'

        partial_ply_bug_pacs = (
                partial_ply_bug_pacs +
                [multiAgents.StaffMultiAgentSearchAgent(**keyword_dict)]
        )
        for pac in pacs_with_stop + pacs_without_stop + partial_ply_bug_pacs:
            pac.verbose = False

        ourpac = [pacs_with_stop[0], pacs_without_stop[0]]

        alternative_depth_pacs = self.select(pacs_with_stop + pacs_without_stop, [1, 4, 2, 5])

        return (ourpac, alternative_depth_pacs, partial_ply_bug_pacs)

    def registerInitialState(self, state: State):

        for agent in self.solutionAgents + self.alternativeDepthAgents:
            if 'registerInitialState' in dir(agent):
                agent.registerInitialState(state)
        random.seed(self.seed)

    def getAction(self, state):
        # survey agents
        State.getAndResetExplored()
        optimalActionLists = []
        for agent in self.solutionAgents:
            optimalActionLists.append((agent.getBestPacmanActions(
                state)[0], len(State.getAndResetExplored())))
        alternativeDepthLists = [agent.getBestPacmanActions(
            state)[0] for agent in self.alternativeDepthAgents]
        partialPlyBugLists = [agent.getBestPacmanActions(
            state)[0] for agent in self.partialPlyBugAgents]
        # bool_record responses
        self.optimalActionLists.append(optimalActionLists)
        self.alternativeDepthLists.append(alternativeDepthLists)
        self.partialPlyBugLists.append(partialPlyBugLists)
        self.stepCount += 1
        random.seed(self.seed + self.stepCount)
        return optimalActionLists[0][0][0]

    def getTraces(self):
        # return traces from individual agents
        return (self.optimalActionLists, self.alternativeDepthLists, self.partialPlyBugLists)


def _run_pacman_games_wrapper(str_path_layout: str,
                              list_pacman: List[Agent],
                              list_ghost: List[Agent],
                              graphics_pacman: GraphicsPacman,
                              number_of_games: int = 1,
                              bool_record: bool = False,
                              num_training: int = 0,
                              bool_catch_exceptions: bool = True,
                              timeout: int = 120,
                              _name: str = 'games',
                              **kwargs,
                              ) -> Dict[str, Any]:
    """
    Runs a few pacman games and outputs their statistics.
    """
    time_start = time.time()
    print('*** Running %s on {} {} time(s).'.format(_name, str_path_layout, number_of_games))

    list_game = run_pacman_games(
        str_path_layout,
        list_pacman,
        list_ghost,
        graphics_pacman,
        number_of_games,
        bool_record,
        num_training,
        bool_catch_exceptions,
        timeout,
        **kwargs,
    )
    print('*** Finished running {} on {} after {} seconds.'.format(_name, str_path_layout, time.time() - time_start))

    dict_stats = {
        'time': time.time() - time_start, 'wins': [g.state_pacman.isWin() for g in list_game].count(True),
        'list_game': list_game,
        'scores': [g.state_pacman.getScore() for g in list_game],
        'timeouts': [g.agentTimeout for g in list_game].count(True),
        'crashes': [g.agentCrashed for g in list_game].count(True)
    }

    print('*** Won {} out of {} games. Average score: {} ***'.format(dict_stats['wins'],
                                                                     len(list_game),
                                                                     sum(dict_stats['scores']) * 1.0 / len(list_game)
                                                                     ))
    return dict_stats


class PacmanGameTreeTest(TestCaseAgent):
    """

    Used by:
        8-pacman-game.test

    """

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        super(PacmanGameTreeTest, self).__init__(question, dict_file_test)

        # self.str_class_agent: Type[Agent] = self.dict_file_test['agent']
        # self.depth: int = int(self.dict_file_test['depth'])

        self.seed: int = int(self.dict_file_test['seed'])

        self.layout_text: str = self.dict_file_test['layout_text']
        self.layout_name: str = self.dict_file_test['layout_name']
        self.max_points: int = int(self.dict_file_test['max_points'])

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # load student value_failure and staff value_failure solutions

        # multiAgents = moduleDict['projectTestClasses']
        # agent_to_be_tested = getattr(multiAgents, self.str_class_agent)(depth=self.depth)

        print("______ PacmanGameTreeTest")
        pprint(self.dict_file_test)

        # list_list_list_action__value_optimal = (
        #     [json.loads(x) for x in dict_file_solution['optimalActions'].split('\n')]
        # )
        #
        # list_list_action_alt_depth = (
        #     [json.loads(x) for x in dict_file_solution['altDepthActions'].split('\n')]
        # )
        #
        # list_list_action_partial_play_bug = (
        #     [json.loads(x) for x in dict_file_solution['partialPlyBugActions'].split('\n')]
        # )

        # set up game state and play a game
        random.seed(self.seed)

        # lay = layoutpacman.LayoutPacman([l.strip() for l in self.layout_text.split('\n')])

        agent_to_be_tested: Agent = get_subclass_agent(self.str_class_agent)(depth=self.depth)

        # agent_grading = _GradingAgent.from_dict(
        #     self.seed,
        #     agent_to_be_tested,
        #     dict_file_solution,
        #     # list_list_list_action__value_optimal,
        #     # list_list_action_alt_depth,
        #     # list_list_action_partial_play_bug
        # )


        # TODO: JOSEPH THIS IS YOUR OLD STYLE
        # list_container_object_construct_pacman = [ContainerObjectConstruct(
        #     _GradingAgent.__name__,
        #     [self.seed, agent_to_be_tested, dict_file_solution],
        #     {}
        # )]

        # list_agent_pacman = get_list_agent_from_list_container_object_construct(
        #     list_container_object_construct_pacman
        # )

        agent_grading = _GradingAgent(self.seed, agent_to_be_tested, dict_file_solution)

        list_agent_pacman = [agent_grading]

        # THE OLD [AgentPacmanGhostDirectional(i + 1) for i in range(2)],
        list_container_object_construct_ghost = get_list_container_object_construct_from_implicit(
            AgentPacmanGhostDirectional.__name__,
            "",
            2
        )

        list_agent_ghost = get_list_agent_from_list_container_object_construct(
            list_container_object_construct_ghost
        )

        # check return codes and assign grader
        graphics_pacman = self.question.get_graphics()

        dict_stats = _run_pacman_games_wrapper(
            self.layout_name,
            list_agent_pacman,
            list_agent_ghost,
            graphics_pacman,
        )

        if dict_stats['timeouts'] > 0:
            self.add_message_to_messages('Agent timed out on smallClassic.  No credit')
            return self._procedure_test_fail(grader)

        if dict_stats['crashes'] > 0:
            self.add_message_to_messages('Agent crashed on smallClassic.  No credit')
            return self._procedure_test_fail(grader)

        value_failure = agent_grading.get_value_failure()

        if value_failure == 0:
            return self._procedure_test_pass(grader)

        elif value_failure == -3:
            if agent_grading.get_amount_wrong_states_explored() > 0:
                self.add_message_to_messages('Bug: Wrong number of states expanded.')
                return self._procedure_test_fail(grader)
            else:
                return self._procedure_test_pass(grader)

        elif value_failure == -2:
            self.add_message_to_messages('Bug: Partial Play Bug')
            return self._procedure_test_fail(grader)
        elif value_failure == -1:
            self.add_message_to_messages('Bug: Search depth off by 1')
            return self._procedure_test_fail(grader)

        elif value_failure > 0:
            moves = agent_grading.get_list_tuple__state__action_wrong__action_correct()
            state, action_wrong, action_correct = random.choice(moves)

            self.add_message_to_messages('Bug: Suboptimal moves')
            self.add_message_to_messages('State:{}\nStudent Move:{}\nOptimal Move:{}'.format(state,
                                                                                             action_wrong,
                                                                                             action_correct))
            return self._procedure_test_fail(grader)

    @staticmethod
    def _write_list_to_file(handle: TextIOWrapper, name: str, list_: List):
        handle.write('%s: """\n' % name)
        for l in list_:
            handle.write('%s\n' % json.dumps(l))
        handle.write('"""\n')

    def write_solution(self, path_file: str):
        """
        WRite solutions given path_file

        """
        # load module, set seed, create ghosts and macman, run game
        # multiAgents = moduleDict['projectTestClasses']

        random.seed(self.seed)
        lay = layout_pacman.LayoutPacman([l.strip() for l in self.layout_text.split('\n')])
        if self.str_class_agent == 'AgentPacmanExpectimax':
            ourPacOptions = {'expectimax': 'True'}
        elif self.str_class_agent == 'AgentPacmanMinimaxAlphaBeta':
            ourPacOptions = {'alphabeta': 'True'}
        else:
            ourPacOptions = {}

        # raise Exception("writeSolution CALLED")

        pac = PolyAgent(self.seed, ourPacOptions, self.depth)

        disp = self.question.get_graphics()

        _run_pacman_games_wrapper(
            lay,
            self.layout_name,
            pac,
            [AgentPacmanGhostDirectional(i + 1) for i in range(2)],
            disp,
            _name=self.str_class_agent
        )

        (optimalActions, altDepthActions, partialPlyBugActions) = pac.getTraces()

        # recover traces and bool_record to file
        with open(path_file, 'w') as file_object:
            self._write_list_to_file(file_object, 'optimalActions', optimalActions)
            self._write_list_to_file(file_object, 'altDepthActions', altDepthActions)
            self._write_list_to_file(file_object, 'partialPlyBugActions', partialPlyBugActions)
