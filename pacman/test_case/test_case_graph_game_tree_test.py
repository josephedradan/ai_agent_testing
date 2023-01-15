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
from typing import TYPE_CHECKING

from pacman.agent import *
from pacman.test_case.test_case import TestCase

if TYPE_CHECKING:
    from pacman.question.question import Question
    from pacman.grader import Grader

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

        studentAgent = get_subclass_agent(self.class_agent)(depth=self.depth)

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
            return self._procedure_test_fail(grader)
        else:
            return self._procedure_test_pass(grader)

    def writeSolution(self, filePath):
        # multiAgents = moduleDict['projectTestClasses']
        action, generated = self.solveProblem()

        with open(filePath, 'w') as handle:
            handle.write('# This is the solution file for %s.\n' % self.path_file_test)
            handle.write('action: "%s"\n' % (action,))
            handle.write('generated: "%s"\n' % (generated,))
        return True
