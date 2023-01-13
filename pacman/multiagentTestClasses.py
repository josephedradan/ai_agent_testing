# multiagentTestClasses.py
# ------------------------
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
from __future__ import annotations

import json
from pprint import PrettyPrinter
# from multiagent.agent.agent import Agent
# from multiagent.agent.agent_ghost_directional import AgentGhostDirectional
# from multiagent._test_case import TestCase
# from multiagent.agent import *
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from pacman.agent import Agent
from pacman.game.directions import Action
from pacman.game.game_state import GameState

# A minimax tree which interfaces like game_state
#     game_state.getNumAgents()
#     game_state.isWin()
#     game_state.isLose()
#     game_state.generateSuccessor(agentIndex, action)
#     game_state.getScore()
#           used by multiAgents.scoreEvaluationFunction, which is the default
#

pp = PrettyPrinter()

# from game import Agent
# from agent_pacman_ import GameState
# from list_agent_ghost import AgentGhostRandom, AgentGhostDirectional
import random

# import layout

# import autograder
# import grading

# VERBOSE = False


# class MultiagentTreeState(object):
#     def __init__(self, problem, state):
#         self.problem = problem
#         self.state = state
#
#     def generateSuccessor(self, agentIndex, action):
#         if VERBOSE:
#             print("generateSuccessor(%s, %s, %s) -> %s" % (self.state, agentIndex,
#                                                            action,
#                                                            self.search_problem.stateToSuccessorMap[self.state][action]))
#         successor = self.search_problem.stateToSuccessorMap[self.state][action]
#         self.search_problem.generatedStates.add(successor)
#         return MultiagentTreeState(self.problem, successor)
#
#     def getScore(self):
#         if VERBOSE:
#             print("getScore(%s) -> %s" %
#                   (self.state, self.search_problem.evaluation[self.state]))
#         if self.state not in self.search_problem.evaluation:
#             raise Exception(
#                 'getScore() called on non-terminal game_state or before maximum depth achieved.')
#         return float(self.search_problem.evaluation[self.state])
#
#     def getLegalActions(self, agentIndex=0):
#         if VERBOSE:
#             print("getLegalActions(%s) -> %s" %
#                   (self.state, self.search_problem.stateToActions[self.state]))
#         # if len(self.search_problem.stateToActions[self.game_state]) == 0:
#         #    print "WARNING: getLegalActions called on leaf game_state %s" % (self.game_state,)
#         return list(self.search_problem.stateToActions[self.state])
#
#     def isWin(self):
#         if VERBOSE:
#             print("isWin(%s) -> %s" %
#                   (self.state, self.state in self.search_problem.winStates))
#         return self.state in self.search_problem.winStates
#
#     def isLose(self):
#         if VERBOSE:
#             print("isLose(%s) -> %s" %
#                   (self.state, self.state in self.search_problem.loseStates))
#         return self.state in self.search_problem.loseStates
#
#     def getNumAgents(self):
#         if VERBOSE:
#             print("getNumAgents(%s) -> %s" %
#                   (self.state, self.search_problem.numAgents))
#         return self.search_problem.numAgents


# class MultiagentTreeProblem(object):
#     def __init__(self, numAgents, startState, winStates, loseStates, successors, evaluation):
#         self.startState = MultiagentTreeState(self, startState)
#
#         self.numAgents = numAgents
#         self.winStates = winStates
#         self.loseStates = loseStates
#         self.evaluation = evaluation
#         self.successors = successors
#
#         self.reset()
#
#         self.stateToSuccessorMap = defaultdict(dict)
#         self.stateToActions = defaultdict(list)
#         for state, action, nextState in successors:
#             self.stateToActions[state].append(action)
#             self.stateToSuccessorMap[state][action] = nextState
#
#     def reset(self):
#         self.generatedStates = set([self.startState.state])
#

# def parseTreeProblem(dict_file_test):
#     numAgents = int(dict_file_test["num_agents"])
#     startState = dict_file_test["start_state"]
#     winStates = set(dict_file_test["win_states"].split(" "))
#     loseStates = set(dict_file_test["lose_states"].split(" "))
#     successors = []
#
#     evaluation = {}
#     for line in dict_file_test["evaluation"].split('\n'):
#         tokens = line.split()
#         if len(tokens) == 2:
#             state, value = tokens
#             evaluation[state] = float(value)
#         else:
#             raise Exception("[parseTree] Bad evaluation line: |%s|" % (line,))
#
#     for line in dict_file_test["successors"].split('\n'):
#         tokens = line.split()
#         if len(tokens) == 3:
#             state, action, nextState = tokens
#             successors.append((state, action, nextState))
#         else:
#             raise Exception("[parseTree] Bad successor line: |%s|" % (line,))
#
#     return MultiagentTreeProblem(numAgents, startState, winStates, loseStates, successors, evaluation)


# def run(lay, layName, pac, list_agent_ghost, disp, nGames=1, name='games'):
#     """
#     Runs a few games and outputs their statistics.
#     """
#     starttime = time.time()
#     print('*** Running %s on' % name, layName, '%d time(s).' % nGames)
#     games = agent_pacman_.runGames(lay, pac, list_agent_ghost, disp,
#                             nGames, False, bool_catch_exceptions=True, timeout=120)
#     print('*** Finished running %s on' % name, layName,
#           'after %d seconds.' % (time.time() - starttime))
#     stats = {'time': time.time() - starttime, 'wins': [g.state.isWin() for g in games].count(True), 'games': games,
#              'scores': [g.state.getScore() for g in games],
#              'timeouts': [g.agentTimeout for g in games].count(True),
#              'crashes': [g.agentCrashed for g in games].count(True)}
#     print('*** Won %d out of %d games. Average score: %f ***' %
#           (stats['wins'], len(games), sum(stats['scores']) * 1.0 / len(games)))
#     return stats


# class PolyAgent(Agent):
#     def __init__(self, seed, multiAgents, ourPacOptions, depth):
#         # prepare our agent_pacman_ agents
#         solutionAgents, alternativeDepthAgents, partialPlyBugAgents = self.construct_our_pacs(
#             multiAgents, ourPacOptions)
#         for p in solutionAgents:
#             p.depth = depth
#         for p in partialPlyBugAgents:
#             p.depth = depth
#         for p in alternativeDepthAgents[:2]:
#             p.depth = max(1, depth - 1)
#         for p in alternativeDepthAgents[2:]:
#             p.depth = depth + 1
#         self.solutionAgents = solutionAgents
#         self.alternativeDepthAgents = alternativeDepthAgents
#         self.partialPlyBugAgents = partialPlyBugAgents
#         # prepare fields for storing the results
#         self.optimalActionLists = []
#         self.alternativeDepthLists = []
#         self.partialPlyBugLists = []
#         self.seed = seed
#         self.stepCount = 0
#
#     def select(self, list, indices):
#         """
#         Return a sublist of elements given by indices in list.
#         """
#         return [list[i] for i in indices]
#
#     def construct_our_pacs(self, multiAgents, keyword_dict):
#         pacs_without_stop = [multiAgents.StaffMultiAgentSearchAgent(
#             **keyword_dict) for i in range(3)]
#         keyword_dict['keepStop'] = 'True'
#         pacs_with_stop = [multiAgents.StaffMultiAgentSearchAgent(
#             **keyword_dict) for i in range(3)]
#         keyword_dict['usePartialPlyBug'] = 'True'
#         partial_ply_bug_pacs = [
#             multiAgents.StaffMultiAgentSearchAgent(**keyword_dict)]
#         keyword_dict['keepStop'] = 'False'
#         partial_ply_bug_pacs = partial_ply_bug_pacs + \
#                                [multiAgents.StaffMultiAgentSearchAgent(**keyword_dict)]
#         for pac in pacs_with_stop + pacs_without_stop + partial_ply_bug_pacs:
#             pac.verbose = False
#         ourpac = [pacs_with_stop[0], pacs_without_stop[0]]
#         alternative_depth_pacs = self.select(
#             pacs_with_stop + pacs_without_stop, [1, 4, 2, 5])
#         return (ourpac, alternative_depth_pacs, partial_ply_bug_pacs)
#
#     def registerInitialState(self, state):
#         for agent in self.solutionAgents + self.alternativeDepthAgents:
#             if 'registerInitialState' in dir(agent):
#                 agent.registerInitialState(state)
#         random.seed(self.seed)
#
#     def getAction(self, game_state):
#         # survey agents
#         GameState.getAndResetExplored()
#         optimalActionLists = []
#         for agent in self.solutionAgents:
#             optimalActionLists.append((agent.getBestPacmanActions(
#                 game_state)[0], len(GameState.getAndResetExplored())))
#         alternativeDepthLists = [agent.getBestPacmanActions(
#             game_state)[0] for agent in self.alternativeDepthAgents]
#         partialPlyBugLists = [agent.getBestPacmanActions(
#             game_state)[0] for agent in self.partialPlyBugAgents]
#         # bool_record responses
#         self.optimalActionLists.append(optimalActionLists)
#         self.alternativeDepthLists.append(alternativeDepthLists)
#         self.partialPlyBugLists.append(partialPlyBugLists)
#         self.stepCount += 1
#         random.seed(self.seed + self.stepCount)
#         return optimalActionLists[0][0][0]
#
#     def getTraces(self):
#         # return traces from individual agents
#         return (self.optimalActionLists, self.alternativeDepthLists, self.partialPlyBugLists)


# class PacmanGameTreeTest(TestCase):
#
#     def __init__(self, str_question, dict_file_test):
#         super(PacmanGameTreeTest, self).__init__(str_question, dict_file_test)
#         self.seed = int(self.dict_file_test['seed'])
#         self.str_class_agent = self.dict_file_test['str_class_agent']
#         self.layout_text = self.dict_file_test['layout']
#         self.layout_name = self.dict_file_test['str_layout_name']
#         self.depth = int(self.dict_file_test['depth'])
#         self.max_points = int(self.dict_file_test['max_points'])
#
#     def execute(self, grader, moduleDict, dict_file_solution):
#         # load student code and staff code solutions
#         multiAgents = moduleDict['projectTestClasses']
#         studentAgent = getattr(multiAgents, self.str_class_agent)(depth=self.depth)
#         allActions = [json.loads(x)
#                       for x in dict_file_solution['optimalActions'].split('\n')]
#         altDepthActions = [json.loads(
#             x) for x in dict_file_solution['altDepthActions'].split('\n')]
#         partialPlyBugActions = [json.loads(
#             x) for x in dict_file_solution['partialPlyBugActions'].split('\n')]
#         # set up game game_state and play a game
#         random.seed(self.seed)
#         lay = layout.Layout([l.strip() for l in self.layout_text.split('\n')])
#
#         pac = GradingAgent(
#             self.seed,
#             studentAgent,
#             allActions,
#             altDepthActions,
#             partialPlyBugActions
#         )
#
#         # check return codes and assign grader
#         disp = self.str_question.get_display()
#         stats = run(lay, self.layout_name, pac, [AgentGhostDirectional(
#             i + 1) for i in range(2)], disp, name=self.str_class_agent)
#         if stats['timeouts'] > 0:
#             self.addMessage('Agent timed out on smallClassic.  No credit')
#             return self.testFail(grader)
#         if stats['crashes'] > 0:
#             self.addMessage('Agent crashed on smallClassic.  No credit')
#             return self.testFail(grader)
#         code = pac.checkFailure()
#         if code == 0:
#             return self.testPass(grader)
#         elif code == -3:
#             if pac.getWrongStatesExplored() >= 0:
#                 self.addMessage('Bug: Wrong number of states expanded.')
#                 return self.testFail(grader)
#             else:
#                 return self.testPass(grader)
#         elif code == -2:
#             self.addMessage('Bug: Partial Ply Bug')
#             return self.testFail(grader)
#         elif code == -1:
#             self.addMessage('Bug: Search depth off by 1')
#             return self.testFail(grader)
#         elif code > 0:
#             moves = pac.getSuboptimalMoves()
#             state, studentMove, optMove = random.choice(moves)
#             self.addMessage('Bug: Suboptimal moves')
#             self.addMessage('State:%s\nStudent Move:%s\nOptimal Move:%s' % (
#                 state, studentMove, optMove))
#             return self.testFail(grader)
#
#     def writeList(self, handle, name, list):
#         handle.write('%s: """\n' % name)
#         for l in list:
#             handle.write('%s\n' % json.dumps(l))
#         handle.write('"""\n')
#
#     def writeSolution(self, moduleDict, filePath):
#         # load module, set seed, create list_agent_ghost and macman, run game
#         multiAgents = moduleDict['projectTestClasses']
#         random.seed(self.seed)
#         lay = layout.Layout([l.strip() for l in self.layout_text.split('\n')])
#         if self.str_class_agent == 'AgentPacmanExpectimax':
#             ourPacOptions = {'expectimax': 'True'}
#         elif self.str_class_agent == 'AgentPacmanMinimaxAlphaBeta':
#             ourPacOptions = {'alphabeta': 'True'}
#         else:
#             ourPacOptions = {}
#         pac = PolyAgent(self.seed, multiAgents, ourPacOptions, self.depth)
#         disp = self.str_question.get_display()
#         run(lay, self.layout_name, pac, [AgentGhostDirectional(
#             i + 1) for i in range(2)], disp, name=self.str_class_agent)
#         (optimalActions, altDepthActions, partialPlyBugActions) = pac.getTraces()
#         # recover traces and bool_record to file
#         handle = open(filePath, 'w')
#         self.writeList(handle, 'optimalActions', optimalActions)
#         self.writeList(handle, 'altDepthActions', altDepthActions)
#         self.writeList(handle, 'partialPlyBugActions', partialPlyBugActions)
#         handle.close()
#
#
# class GraphGameTreeTest(TestCase):
#
#     def __init__(self, str_question, dict_file_test):
#         super(GraphGameTreeTest, self).__init__(str_question, dict_file_test)
#         self.problem = parseTreeProblem(dict_file_test)
#         self.str_class_agent = self.dict_file_test['str_class_agent']
#         self.diagram = self.dict_file_test['diagram'].split('\n')
#         self.depth = int(self.dict_file_test['depth'])
#
#     def solveProblem(self, multiAgents):
#         self.search_problem.reset()
#         studentAgent = getattr(multiAgents, self.str_class_agent)(depth=self.depth)
#         action = studentAgent.getAction(self.search_problem.startState)
#         generated = self.search_problem.generatedStates
#         return action, " ".join([string_given(s) for s in sorted(generated)])
#
#     def addDiagram(self):
#         self.addMessage('Tree:')
#         for line in self.diagram:
#             self.addMessage(line)
#
#     def execute(self, grader, moduleDict, dict_file_solution):
#         multiAgents = moduleDict['projectTestClasses']
#         goldAction = dict_file_solution['action']
#         goldGenerated = dict_file_solution['generated']
#         action, generated = self.solveProblem(multiAgents)
#
#         fail = False
#         if action != goldAction:
#             self.addMessage('Incorrect move for depth=%s' % (self.depth,))
#             self.addMessage(
#                 '    Student move: %s\n    Optimal move: %s' % (action, goldAction))
#             fail = True
#
#         if generated != goldGenerated:
#             self.addMessage(
#                 'Incorrect generated nodes for depth=%s' % (self.depth,))
#             self.addMessage('    Student generated nodes: %s\n    Correct generated nodes: %s' % (
#                 generated, goldGenerated))
#             fail = True
#
#         if fail:
#             self.addDiagram()
#             return self.testFail(grader)
#         else:
#             return self.testPass(grader)
#
#     def writeSolution(self, moduleDict, filePath):
#         multiAgents = moduleDict['projectTestClasses']
#         action, generated = self.solveProblem(multiAgents)
#         with open(filePath, 'w') as handle:
#             handle.write('# This is the solution file for %s.\n' % self.path_file_test)
#             handle.write('action: "%s"\n' % (action,))
#             handle.write('generated: "%s"\n' % (generated,))
#         return True
#
#
# import time
#
#
# class EvalAgentTest(TestCase):
#
#     def __init__(self, str_question, dict_file_test):
#         super(EvalAgentTest, self).__init__(str_question, dict_file_test)
#         pprint(dict_file_test)
#         self.str_layout_name = dict_file_test['str_layout_name']
#         self.str_class_agent = dict_file_test['str_class_agent']
#         self.list_agent_ghost = eval(dict_file_test['list_agent_ghost'])
#         self.maxTime = int(dict_file_test['maxTime'])
#         self.seed = int(dict_file_test['randomSeed'])
#         self.number_of_games = int(dict_file_test['number_of_games'])
#
#         self.scoreMinimum = int(
#             dict_file_test['scoreMinimum']) if 'scoreMinimum' in dict_file_test else None
#         self.nonTimeoutMinimum = int(
#             dict_file_test['nonTimeoutMinimum']) if 'nonTimeoutMinimum' in dict_file_test else None
#         self.winsMinimum = int(
#             dict_file_test['winsMinimum']) if 'winsMinimum' in dict_file_test else None
#
#         self.scoreThresholds = [int(s) for s in dict_file_test.get(
#             'scoreThresholds', '').split()]
#         self.nonTimeoutThresholds = [int(s) for s in dict_file_test.get(
#             'nonTimeoutThresholds', '').split()]
#         self.winsThresholds = [int(s) for s in dict_file_test.get(
#             'winsThresholds', '').split()]
#
#         self.maxPoints = sum([len(t) for t in [
#             self.scoreThresholds, self.nonTimeoutThresholds, self.winsThresholds]])
#         self.agentArgs = dict_file_test.get('agentArgs', '')
#
#     def execute(self, grader, moduleDict, dict_file_solution):
#         startTime = time.time()
#
#         # TODO: multiAgents TO 'projectTestClasses'
#         agentType = getattr(moduleDict['projectTestClasses'], self.str_class_agent)
#         agentOpts = agent_pacman_.parseAgentArgs(
#             self.agentArgs) if self.agentArgs != '' else {}
#         agent = agentType(**agentOpts)
#
#         lay = layout.getLayout(self.str_layout_name, 3)
#
#         disp = self.str_question.get_display()
#
#         random.seed(self.seed)
#         games = agent_pacman_.runGames(lay, agent, self.list_agent_ghost, disp, self.number_of_games,
#                                 False, bool_catch_exceptions=True, timeout=self.maxTime)
#         totalTime = time.time() - startTime
#
#         stats = {'time': totalTime, 'wins': [g.state.isWin() for g in games].count(True),
#                  'games': games, 'scores': [g.state.getScore() for g in games],
#                  'timeouts': [g.agentTimeout for g in games].count(True),
#                  'crashes': [g.agentCrashed for g in games].count(True)}
#
#         averageScore = sum(stats['scores']) / float(len(stats['scores']))
#         nonTimeouts = self.number_of_games - stats['timeouts']
#         wins = stats['wins']
#
#         def gradeThreshold(value, minimum, thresholds, name):
#             points = 0
#             passed = (minimum == None) or (value >= minimum)
#             if passed:
#                 for t in thresholds:
#                     if value >= t:
#                         points += 1
#             return (passed, points, value, minimum, thresholds, name)
#
#         results = [gradeThreshold(averageScore, self.scoreMinimum, self.scoreThresholds, "average score"),
#                    gradeThreshold(nonTimeouts, self.nonTimeoutMinimum,
#                                   self.nonTimeoutThresholds, "games not timed out"),
#                    gradeThreshold(wins, self.winsMinimum, self.winsThresholds, "wins")]
#
#         totalPoints = 0
#         for passed, points, value, minimum, thresholds, name in results:
#             if minimum == None and len(thresholds) == 0:
#                 continue
#
#             # print passed, points, value, minimum, thresholds, test_case_object
#             totalPoints += points
#             if not passed:
#                 assert points == 0
#                 self.addMessage(
#                     "%s %s (fail: below minimum value %s)" % (value, name, minimum))
#             else:
#                 self.addMessage("%s %s (%s of %s points)" %
#                                 (value, name, points, len(thresholds)))
#
#             if minimum != None:
#                 self.addMessage("    Grading scheme:")
#                 self.addMessage("     < %s:  fail" % (minimum,))
#                 if len(thresholds) == 0 or minimum != thresholds[0]:
#                     self.addMessage("    >= %s:  0 points" % (minimum,))
#                 for idx, threshold in enumerate(thresholds):
#                     self.addMessage("    >= %s:  %s points" %
#                                     (threshold, idx + 1))
#             elif len(thresholds) > 0:
#                 self.addMessage("    Grading scheme:")
#                 self.addMessage("     < %s:  0 points" % (thresholds[0],))
#                 for idx, threshold in enumerate(thresholds):
#                     self.addMessage("    >= %s:  %s points" %
#                                     (threshold, idx + 1))
#
#         if any([not passed for passed, _, _, _, _, _ in results]):
#             totalPoints = 0
#
#         return self.testPartial(grader, totalPoints, self.maxPoints)
#
#     def writeSolution(self, moduleDict, filePath):
#         handle = open(filePath, 'w')
#         handle.write('# This is the solution file for %s.\n' % self.path_file_test)
#         handle.write('# File intentionally blank.\n')
#         handle.close()
#         return True
