"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/3/2023

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
from pacman.graphics.graphics_pacman import GraphicsPacman
from pacman.multiagentTestClasses import GradingAgent

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


def run(layout_: Layout,
        layout_name: str,
        agent_pacman_: Agent,
        list_agent_ghost: List[Agent],
        display: GraphicsPacman,
        number_of_games: int = 1,
        name: str = 'games'
        ) -> Dict[str, Any]:
    """
    Runs a few games and outputs their statistics.
    """
    time_start = time.time()
    print('*** Running %s on {} {} time(s).'.format(name, layout_name, number_of_games))

    games = main.run_games(
        layout_,
        agent_pacman_,
        list_agent_ghost,
        display,
        number_of_games,
        False,
        bool_catch_exceptions=True,
        timeout=120
    )
    print('*** Finished running {} on {} after {} seconds.'.format(name, layout_name, time.time() - time_start))

    dict_stats = {
        'time': time.time() - time_start, 'wins': [g.state.isWin() for g in games].count(True), 'games': games,
        'scores': [g.state.getScore() for g in games],
        'timeouts': [g.agentTimeout for g in games].count(True),
        'crashes': [g.agentCrashed for g in games].count(True)
    }

    print('*** Won {} out of {} games. Average score: {} ***'.format(dict_stats['wins'],
                                                                     len(games),
                                                                     sum(dict_stats['scores']) * 1.0 / len(games)
                                                                     ))
    return dict_stats


def get_class_test_case_subclass(name_test_case_subclass: str) -> Type[TestCase]:
    test_case_subclass: Union[Type[TestCase], str] = name_test_case_subclass

    if isinstance(name_test_case_subclass, str):
        test_case_subclass = DICT_K_NAME_TEST_CASE_SUBCLASS_V_TEST_CASE_SUBCLASS.get(
            name_test_case_subclass
        )

    if test_case_subclass is None:
        raise Exception("{} is not a valid TestCase subclass".format(name_test_case_subclass))

    return test_case_subclass


DICT_K_NAME_TEST_CASE_SUBCLASS_V_TEST_CASE_SUBCLASS = {}


class TestCase(ABC):

    # def raiseNotDefined(self):
    #     print('Method not implemented: %s' % inspect.stack()[1][3])
    #     sys.exit(1)

    def __init_subclass__(cls, **kwargs):
        DICT_K_NAME_TEST_CASE_SUBCLASS_V_TEST_CASE_SUBCLASS[cls.__name__] = cls

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        print("dict_file_test")
        pprint(dict_file_test)
        self.question: Question = question
        self.dict_file_test: Dict[str, Any] = dict_file_test
        self.path_file_test: str = dict_file_test['path_file_test']
        self.messages: List[str] = []

    def getPath(self):
        return self.path_file_test

    # @abstractmethod
    # def __str__(self):
    #     pass
    #     # self.raiseNotDefined()

    @abstractmethod
    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        """
        Responsible for executing actual games

        :param grader:
        :param dict_file_solution:
        :return:
        """
        pass
        # self.raiseNotDefined()

    @abstractmethod
    def writeSolution(self, filePath):
        pass
        # self.raiseNotDefined()
        # return True

    # Tests should call the following messages for grading
    # to ensure a uniform format for test output.
    #
    # TODO: this is hairy, but we need to fix grading.py's interface
    # to get a nice hierarchical name_project - str_question - test structure,
    # then these should be moved into Question proper.
    def testPass(self, grades):
        grades.addMessage('PASS: %s' % (self.path_file_test,))
        for line in self.messages:
            grades.addMessage('    %s' % (line,))
        return True

    def testFail(self, grades):
        grades.addMessage('FAIL: %s' % (self.path_file_test,))
        for line in self.messages:
            grades.addMessage('    %s' % (line,))
        return False

    # This should really be str_question level?
    def testPartial(self, grades, points, maxPoints) -> bool:
        grades.addPoints(points)
        extraCredit = max(0, points - maxPoints)
        regularCredit = points - extraCredit

        grades.addMessage('%s: %s (%s of %s points)' % (
            "PASS" if points >= maxPoints else "FAIL", self.path_file_test, regularCredit, maxPoints))
        if extraCredit > 0:
            grades.addMessage('EXTRA CREDIT: %s points' % (extraCredit,))

        for line in self.messages:
            grades.addMessage('    %s' % (line,))

        return True

    def addMessage(self, message):
        self.messages.extend(message.split('\n'))


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
        # load student code and staff code solutions

        # multiAgents = moduleDict['projectTestClasses']
        # agent_ = getattr(multiAgents, self.str_class_agent)(depth=self.depth)

        agent_: Agent = get_class_agent(self.class_agent)(depth=self.depth)

        list_list__list_action__value_optimal = (
            [json.loads(x) for x in dict_file_solution['optimalActions'].split('\n')]
        )

        list_list_action_alt_depth = (
            [json.loads(x) for x in dict_file_solution['altDepthActions'].split('\n')]
        )

        list_list_action_partial_play_bug = (
            [json.loads(x) for x in dict_file_solution['partialPlyBugActions'].split('\n')]
        )

        # set up game game_state and play a game
        random.seed(self.seed)

        lay = layout.Layout([l.strip() for l in self.layout_text.split('\n')])

        pac = GradingAgent(
            self.seed,
            agent_,
            list_list__list_action__value_optimal,
            list_list_action_alt_depth,
            list_list_action_partial_play_bug
        )

        # check return codes and assign grader
        disp = self.question.get_display()
        stats = run(
            lay,
            self.layout_name,
            pac,
            [AgentGhostDirectional(i + 1) for i in range(2)],
            disp,
            name=self.class_agent
        )

        if stats['timeouts'] > 0:
            self.addMessage('Agent timed out on smallClassic.  No credit')
            return self.testFail(grader)
        if stats['crashes'] > 0:
            self.addMessage('Agent crashed on smallClassic.  No credit')
            return self.testFail(grader)
        code = pac.checkFailure()
        if code == 0:
            return self.testPass(grader)
        elif code == -3:
            if pac.getWrongStatesExplored() >= 0:
                self.addMessage('Bug: Wrong number of states expanded.')
                return self.testFail(grader)
            else:
                return self.testPass(grader)
        elif code == -2:
            self.addMessage('Bug: Partial Ply Bug')
            return self.testFail(grader)
        elif code == -1:
            self.addMessage('Bug: Search depth off by 1')
            return self.testFail(grader)
        elif code > 0:
            moves = pac.getSuboptimalMoves()
            state, studentMove, optMove = random.choice(moves)
            self.addMessage('Bug: Suboptimal moves')
            self.addMessage('State:%s\nStudent Move:%s\nOptimal Move:%s' % (
                state, studentMove, optMove))
            return self.testFail(grader)

    def writeList(self, handle, name, list):
        handle.write('%s: """\n' % name)
        for l in list:
            handle.write('%s\n' % json.dumps(l))
        handle.write('"""\n')

    def writeSolution(self, filePath):
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

        disp = self.question.get_display()
        run(lay, self.layout_name, pac, [AgentGhostDirectional(
            i + 1) for i in range(2)], disp, name=self.class_agent)
        (optimalActions, altDepthActions, partialPlyBugActions) = pac.getTraces()
        # recover traces and bool_record to file
        handle = open(filePath, 'w')
        self.writeList(handle, 'optimalActions', optimalActions)
        self.writeList(handle, 'altDepthActions', altDepthActions)
        self.writeList(handle, 'partialPlyBugActions', partialPlyBugActions)
        handle.close()


VERBOSE = False


class MultiagentTreeState(object):
    def __init__(self, problem, state):
        self.problem = problem
        self.state = state

    def generateSuccessor(self, agentIndex, action):
        if VERBOSE:
            print("generateSuccessor(%s, %s, %s) -> %s" % (self.state, agentIndex,
                                                           action,
                                                           self.problem.stateToSuccessorMap[self.state][action]))
        successor = self.problem.stateToSuccessorMap[self.state][action]
        self.problem.generatedStates.add(successor)
        return MultiagentTreeState(self.problem, successor)

    def getScore(self):
        if VERBOSE:
            print("getScore(%s) -> %s" %
                  (self.state, self.problem.evaluation[self.state]))
        if self.state not in self.problem.evaluation:
            raise Exception(
                'getScore() called on non-terminal game_state or before maximum depth achieved.')
        return float(self.problem.evaluation[self.state])

    def getLegalActions(self, agentIndex=0):
        if VERBOSE:
            print("getLegalActions(%s) -> %s" %
                  (self.state, self.problem.stateToActions[self.state]))
        # if len(self.problem.stateToActions[self.game_state]) == 0:
        #    print "WARNING: getLegalActions called on leaf game_state %s" % (self.game_state,)
        return list(self.problem.stateToActions[self.state])

    def isWin(self):
        if VERBOSE:
            print("isWin(%s) -> %s" %
                  (self.state, self.state in self.problem.winStates))
        return self.state in self.problem.winStates

    def isLose(self):
        if VERBOSE:
            print("isLose(%s) -> %s" %
                  (self.state, self.state in self.problem.loseStates))
        return self.state in self.problem.loseStates

    def getNumAgents(self):
        if VERBOSE:
            print("getNumAgents(%s) -> %s" %
                  (self.state, self.problem.numAgents))
        return self.problem.numAgents


class MultiagentTreeProblem(object):
    def __init__(self, numAgents, startState, winStates, loseStates, successors, evaluation):
        self.startState = MultiagentTreeState(self, startState)

        self.numAgents = numAgents
        self.winStates = winStates
        self.loseStates = loseStates
        self.evaluation = evaluation
        self.successors = successors

        self.reset()

        self.stateToSuccessorMap = defaultdict(dict)
        self.stateToActions = defaultdict(list)
        for state, action, nextState in successors:
            self.stateToActions[state].append(action)
            self.stateToSuccessorMap[state][action] = nextState

    def reset(self):
        self.generatedStates = set([self.startState.state])


def parseTreeProblem(testDict):
    numAgents = int(testDict["num_agents"])
    startState = testDict["start_state"]
    winStates = set(testDict["win_states"].split(" "))
    loseStates = set(testDict["lose_states"].split(" "))
    successors = []

    evaluation = {}
    for line in testDict["evaluation"].split('\n'):
        tokens = line.split()
        if len(tokens) == 2:
            state, value = tokens
            evaluation[state] = float(value)
        else:
            raise Exception("[parseTree] Bad evaluation line: |%s|" % (line,))

    for line in testDict["successors"].split('\n'):
        tokens = line.split()
        if len(tokens) == 3:
            state, action, nextState = tokens
            successors.append((state, action, nextState))
        else:
            raise Exception("[parseTree] Bad successor line: |%s|" % (line,))

    return MultiagentTreeProblem(numAgents, startState, winStates, loseStates, successors, evaluation)


class GraphGameTreeTest(TestCase):

    def __init__(self, question: Question, dict_test: Dict[str, Any]):
        super(GraphGameTreeTest, self).__init__(question, dict_test)
        self.problem = parseTreeProblem(dict_test)
        self.class_agent = self.dict_file_test['alg']
        self.diagram = self.dict_file_test['diagram'].split('\n')
        self.depth = int(self.dict_file_test['depth'])

    def solveProblem(self):

        self.problem.reset()
        # studentAgent = getattr(multiAgents, self.str_class_agent)(depth=self.depth)

        studentAgent = get_class_agent(self.class_agent)(depth=self.depth)

        action = studentAgent.getAction(self.problem.startState)
        generated = self.problem.generatedStates
        return action, " ".join([str(s) for s in sorted(generated)])

    def addDiagram(self):
        self.addMessage('Tree:')
        for line in self.diagram:
            self.addMessage(line)

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # multiAgents = moduleDict['projectTestClasses']

        goldAction = dict_file_solution['action']
        goldGenerated = dict_file_solution['generated']
        action, generated = self.solveProblem()

        fail = False
        if action != goldAction:
            self.addMessage('Incorrect move for depth=%s' % (self.depth,))
            self.addMessage(
                '    Student move: %s\n    Optimal move: %s' % (action, goldAction))
            fail = True

        if generated != goldGenerated:
            self.addMessage(
                'Incorrect generated nodes for depth=%s' % (self.depth,))
            self.addMessage('    Student generated nodes: %s\n    Correct generated nodes: %s' % (
                generated, goldGenerated))
            fail = True

        if fail:
            self.addDiagram()
            return self.testFail(grader)
        else:
            return self.testPass(grader)

    def writeSolution(self, filePath):
        # multiAgents = moduleDict['projectTestClasses']
        action, generated = self.solveProblem()

        with open(filePath, 'w') as handle:
            handle.write('# This is the solution file for %s.\n' % self.path_file_test)
            handle.write('action: "%s"\n' % (action,))
            handle.write('generated: "%s"\n' % (generated,))
        return True


import time


class EvalAgentTest(TestCase):

    def __init__(self, question: Question, dict_file_test: Dict[str, Any]):
        super(EvalAgentTest, self).__init__(question, dict_file_test)
        pprint(dict_file_test)

        self.str_layout_name: str = dict_file_test['layoutName']
        self.str_class_agent: str = dict_file_test['agentName']
        self.list_agent_ghost: List[Agent] = eval(dict_file_test['ghosts'])
        self.maxTime: int = int(dict_file_test['maxTime'])
        self.seed: int = int(dict_file_test['randomSeed'])
        self.numGames: int = int(dict_file_test['numGames'])

        self.scoreMinimum = int(
            dict_file_test['scoreMinimum']) if 'scoreMinimum' in dict_file_test else None
        self.nonTimeoutMinimum = int(
            dict_file_test['nonTimeoutMinimum']) if 'nonTimeoutMinimum' in dict_file_test else None
        self.winsMinimum = int(
            dict_file_test['winsMinimum']) if 'winsMinimum' in dict_file_test else None

        self.scoreThresholds = [int(s) for s in dict_file_test.get(
            'scoreThresholds', '').split()]
        self.nonTimeoutThresholds = [int(s) for s in dict_file_test.get(
            'nonTimeoutThresholds', '').split()]
        self.winsThresholds = [int(s) for s in dict_file_test.get(
            'winsThresholds', '').split()]

        self.maxPoints = sum([len(t) for t in [
            self.scoreThresholds, self.nonTimeoutThresholds, self.winsThresholds]])
        self.agentArgs = dict_file_test.get('agentArgs', '')

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        time_start = time.time()

        # TODO: multiAgents TO 'projectTestClasses'
        # class_agent = getattr(moduleDict['projectTestClasses'], self.str_class_agent)
        class_agent: Type[Agent] = get_class_agent(self.str_class_agent)

        agentOpts = main.get_dict_kwargs(self.agentArgs) if self.agentArgs != '' else {}

        agent = class_agent(**agentOpts)

        lay = layout.getLayout(self.str_layout_name, 3)

        disp = self.question.get_display()

        random.seed(self.seed)

        games = main.run_games(
            lay,
            agent,
            self.list_agent_ghost,
            disp,
            self.numGames,
            False,
            bool_catch_exceptions=True,
            timeout=self.maxTime
        )

        time_total = time.time() - time_start

        stats = {'time': time_total, 'wins': [g.state.isWin() for g in games].count(True),
                 'games': games, 'scores': [g.state.getScore() for g in games],
                 'timeouts': [g.agentTimeout for g in games].count(True),
                 'crashes': [g.agentCrashed for g in games].count(True)}

        averageScore = sum(stats['scores']) / float(len(stats['scores']))
        nonTimeouts = self.numGames - stats['timeouts']
        wins = stats['wins']

        def gradeThreshold(value, minimum, thresholds, name):
            points = 0
            passed = (minimum == None) or (value >= minimum)
            if passed:
                for t in thresholds:
                    if value >= t:
                        points += 1
            return (passed, points, value, minimum, thresholds, name)

        results = [gradeThreshold(averageScore, self.scoreMinimum, self.scoreThresholds, "average score"),
                   gradeThreshold(nonTimeouts, self.nonTimeoutMinimum,
                                  self.nonTimeoutThresholds, "games not timed out"),
                   gradeThreshold(wins, self.winsMinimum, self.winsThresholds, "wins")]

        totalPoints = 0
        for passed, points, value, minimum, thresholds, name in results:
            if minimum == None and len(thresholds) == 0:
                continue

            # print passed, points, value, minimum, thresholds, test_case_object
            totalPoints += points
            if not passed:
                assert points == 0
                self.addMessage(
                    "%s %s (fail: below minimum value %s)" % (value, name, minimum))
            else:
                self.addMessage("%s %s (%s of %s points)" %
                                (value, name, points, len(thresholds)))

            if minimum != None:
                self.addMessage("    Grading scheme:")
                self.addMessage("     < %s:  fail" % (minimum,))
                if len(thresholds) == 0 or minimum != thresholds[0]:
                    self.addMessage("    >= %s:  0 points" % (minimum,))
                for idx, threshold in enumerate(thresholds):
                    self.addMessage("    >= %s:  %s points" %
                                    (threshold, idx + 1))
            elif len(thresholds) > 0:
                self.addMessage("    Grading scheme:")
                self.addMessage("     < %s:  0 points" % (thresholds[0],))
                for idx, threshold in enumerate(thresholds):
                    self.addMessage("    >= %s:  %s points" %
                                    (threshold, idx + 1))

        if any([not passed for passed, _, _, _, _, _ in results]):
            totalPoints = 0

        return self.testPartial(grader, totalPoints, self.maxPoints)

    def writeSolution(self, filePath):
        handle = open(filePath, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path_file_test)
        handle.write('# File intentionally blank.\n')
        handle.close()
        return True
