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
import time
from typing import Any
from typing import Dict
from typing import List
from typing import TYPE_CHECKING

from pacman.agent import *
from pacman.agent._agent_grading import GradingAgent
from pacman.game import layout
from pacman.game.layout import Layout
from pacman.graphics.graphics_pacman import GraphicsPacman
from pacman.main import run_pacman_games
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from pacman.game.game_state import GameState
    from pacman._question import Question
    from pacman.grader import Grader


class PolyAgent(Agent):
    def __init__(self, seed, ourPacOptions, depth):

        # prepare our agent_pacman_ agents
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

    def construct_our_pacs(self, keyword_dict):

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

    def registerInitialState(self, state):

        raise Exception("registerInitialState _test_case POLY")
        for agent in self.solutionAgents + self.alternativeDepthAgents:
            if 'registerInitialState' in dir(agent):
                agent.registerInitialState(state)
        random.seed(self.seed)

    def getAction(self, game_state):
        # survey agents
        GameState.getAndResetExplored()
        optimalActionLists = []
        for agent in self.solutionAgents:
            optimalActionLists.append((agent.getBestPacmanActions(
                game_state)[0], len(GameState.getAndResetExplored())))
        alternativeDepthLists = [agent.getBestPacmanActions(
            game_state)[0] for agent in self.alternativeDepthAgents]
        partialPlyBugLists = [agent.getBestPacmanActions(
            game_state)[0] for agent in self.partialPlyBugAgents]
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


def _run(layout_: Layout,
         layout_name: str,
         agent_pacman_: Agent,
         list_agent_ghost: List[Agent],
         graphics_pacman: GraphicsPacman,
         number_of_games: int = 1,
         name: str = 'games'
         ) -> Dict[str, Any]:
    """
    Runs a few pacman games and outputs their statistics.
    """
    time_start = time.time()
    print('*** Running %s on {} {} time(s).'.format(name, layout_name, number_of_games))

    list_game = run_pacman_games(
        layout_,
        agent_pacman_,
        list_agent_ghost,
        graphics_pacman,
        number_of_games,
        False,
        bool_catch_exceptions=True,
        timeout=120
    )
    print('*** Finished running {} on {} after {} seconds.'.format(name, layout_name, time.time() - time_start))

    dict_stats = {
        'time': time.time() - time_start, 'wins': [g.game_state.isWin() for g in list_game].count(True),
        'list_game': list_game,
        'scores': [g.game_state.getScore() for g in list_game],
        'timeouts': [g.agentTimeout for g in list_game].count(True),
        'crashes': [g.agentCrashed for g in list_game].count(True)
    }

    print('*** Won {} out of {} games. Average score: {} ***'.format(dict_stats['wins'],
                                                                     len(list_game),
                                                                     sum(dict_stats['scores']) * 1.0 / len(list_game)
                                                                     ))
    return dict_stats


class PacmanGameTreeTest(TestCase):

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        super(PacmanGameTreeTest, self).__init__(question, dict_file_test)
        self.seed: int = int(self.dict_file_test['seed'])
        self.class_agent: Type[Agent] = self.dict_file_test['alg']
        self.layout_text: str = self.dict_file_test['layout']
        self.layout_name: str = self.dict_file_test['layoutName']
        self.depth: int = int(self.dict_file_test['depth'])
        self.max_points: int = int(self.dict_file_test['max_points'])

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # load student value_failure and staff value_failure solutions

        # multiAgents = moduleDict['projectTestClasses']
        # agent_ = getattr(multiAgents, self.str_class_agent)(depth=self.depth)

        agent_: Agent = get_class_agent(self.class_agent)(depth=self.depth)

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

        # set up game game_state and play a game
        random.seed(self.seed)

        lay = layout.Layout([l.strip() for l in self.layout_text.split('\n')])

        agent_grading = GradingAgent.from_dict(
            self.seed,
            agent_,
            dict_file_solution,
            # list_list_list_action__value_optimal,
            # list_list_action_alt_depth,
            # list_list_action_partial_play_bug
        )

        # check return codes and assign grader
        disp = self.question.get_graphics_pacman()

        dict_stats = _run(
            lay,
            self.layout_name,
            agent_grading,
            [AgentGhostDirectional(i + 1) for i in range(2)],
            disp,
            name=self.class_agent
        )

        if dict_stats['timeouts'] > 0:
            self.addMessage('Agent timed out on smallClassic.  No credit')
            return self._procedure_test_fail(grader)

        if dict_stats['crashes'] > 0:
            self.addMessage('Agent crashed on smallClassic.  No credit')
            return self._procedure_test_fail(grader)

        value_failure = agent_grading.get_value_failure()

        if value_failure == 0:
            return self._procedure_test_pass(grader)

        elif value_failure == -3:
            if agent_grading.get_amount_wrong_states_explored() > 0:
                self.addMessage('Bug: Wrong number of states expanded.')
                return self._procedure_test_fail(grader)
            else:
                return self._procedure_test_pass(grader)

        elif value_failure == -2:
            self.addMessage('Bug: Partial Play Bug')
            return self._procedure_test_fail(grader)
        elif value_failure == -1:
            self.addMessage('Bug: Search depth off by 1')
            return self._procedure_test_fail(grader)

        elif value_failure > 0:
            moves = agent_grading.get_list_tuple__game_state__action_wrong__action_correct()
            game_state, action_wrong, action_correct = random.choice(moves)

            self.addMessage('Bug: Suboptimal moves')
            self.addMessage('State:{}\nStudent Move:{}\nOptimal Move:{}'.format(game_state,
                                                                                action_wrong,
                                                                                action_correct))
            return self._procedure_test_fail(grader)

    @staticmethod
    def _write_list_to_file(handle, name, list):
        handle.write('%s: """\n' % name)
        for l in list:
            handle.write('%s\n' % json.dumps(l))
        handle.write('"""\n')

    def writeSolution(self, path_file: str):
        """
        WRite solutions given path_file

        """
        # load module, set seed, create list_agent_ghost and macman, run game
        # multiAgents = moduleDict['projectTestClasses']

        random.seed(self.seed)
        lay = layout.Layout([l.strip() for l in self.layout_text.split('\n')])
        if self.class_agent == 'AgentPacmanExpectimax':
            ourPacOptions = {'expectimax': 'True'}
        elif self.class_agent == 'AgentPacmanMinimaxAlphaBeta':
            ourPacOptions = {'alphabeta': 'True'}
        else:
            ourPacOptions = {}

        # raise Exception("writeSolution CALLED")

        pac = PolyAgent(self.seed, ourPacOptions, self.depth)

        disp = self.question.get_graphics_pacman()
        _run(lay, self.layout_name, pac, [AgentGhostDirectional(
            i + 1) for i in range(2)], disp, name=self.class_agent)
        (optimalActions, altDepthActions, partialPlyBugActions) = pac.getTraces()
        # recover traces and bool_record to file
        handle = open(path_file, 'w')
        self._write_list_to_file(handle, 'optimalActions', optimalActions)
        self._write_list_to_file(handle, 'altDepthActions', altDepthActions)
        self._write_list_to_file(handle, 'partialPlyBugActions', partialPlyBugActions)
        handle.close()
