"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/13/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import Any
from typing import Dict

from gridworld.main_grid_world import Gridworld
from gridworld.main_grid_world import makeGrid
from pacman import analysis
from pacman.agent.valueIterationAgents import ValueIterationAgent
from common.grader import Grader
from pacman.test_case import TestCase

### q2/q3
### =====
## For each parameter setting, compute the optimal policy, see if it satisfies some properties


def followPath(policy, start, numSteps=100):
    state = start
    path = []
    for i in range(numSteps):
        if state not in policy:
            break
        action = policy[state]
        path.append("(%s,%s)" % state)
        if action == 'north': nextState = state[0], state[1] + 1
        if action == 'south': nextState = state[0], state[1] - 1
        if action == 'east': nextState = state[0] + 1, state[1]
        if action == 'west': nextState = state[0] - 1, state[1]
        if action == 'exit' or action == None:
            path.append('TERMINAL_STATE')
            break
        state = nextState

    return path


def parseGrid(string):
    grid = [[entry.strip() for entry in line.split()] for line in string.split('\n')]
    for row in grid:
        for x, col in enumerate(row):
            try:
                col = int(col)
            except:
                pass
            if col == "_":
                col = ' '
            row[x] = col
    return makeGrid(grid)


def computePolicy( grid, discount):
    valueIterator = ValueIterationAgent(grid, discount=discount)
    policy = {}
    for state in grid.getStates():
        policy[state] = valueIterator.computeActionFromValues(state)
    return policy


class GridPolicyTest(TestCase):

    def __init__(self, question, testDict):
        super(GridPolicyTest, self).__init__(question, testDict)

        # Function in module in analysis that returns (discount, noise)
        self.parameterFn = testDict['parameterFn']
        self.question2 = testDict.get('question2', 'false').lower() == 'true'

        # GridWorld specification
        #    _ is empty space
        #    numbers are terminal states with that value
        #    # is a wall
        #    S is a start state
        #
        self.gridText = testDict['grid']
        self.grid = Gridworld(parseGrid(testDict['grid']))
        self.gridName = testDict['gridName']

        # Policy specification
        #    _                  policy choice not checked
        #    N, E, S, W policy action must be north, east, south, west
        #
        self.policy = parseGrid(testDict['policy'])

        # State the most probable path must visit
        #    (x,y) for a particular location; (0,0) is bottom left
        #    terminal for the terminal state
        self.pathVisits = testDict.get('pathVisits', None)

        # State the most probable path must not visit
        #    (x,y) for a particular location; (0,0) is bottom left
        #    terminal for the terminal state
        self.pathNotVisits = testDict.get('pathNotVisits', None)

    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        if not hasattr(analysis, self.parameterFn):
            self.addMessage('Method not implemented: analysis.%s' % (self.parameterFn,))
            return self._procedure_test_fail(grader)

        result = getattr(analysis, self.parameterFn)()

        if type(result) == str and result.lower()[0:3] == "not":
            self.addMessage('Actually, it is possible!')
            return self._procedure_test_fail(grader)

        if self.question2:
            livingReward = None
            try:
                discount, noise = result
                discount = float(discount)
                noise = float(noise)
            except:
                self.addMessage('Did not return a (discount, noise) pair; instead analysis.%s returned: %s' % (
                    self.parameterFn, result))
                return self._procedure_test_fail(grader)
            if discount != 0.9 and noise != 0.2:
                self.addMessage(
                    'Must change either the discount or the noise, not both. Returned (discount, noise) = %s' % (
                        result,))
                return self._procedure_test_fail(grader)
        else:
            try:
                discount, noise, livingReward = result
                discount = float(discount)
                noise = float(noise)
                livingReward = float(livingReward)
            except:
                self.addMessage(
                    'Did not return a (discount, noise, living reward) triple; instead analysis.%s returned: %s' % (
                        self.parameterFn, result))
                return self._procedure_test_fail(grader)

        self.grid.setNoise(noise)
        if livingReward != None:
            self.grid.setLivingReward(livingReward)

        start = self.grid.getStartState()
        policy = computePolicy( self.grid, discount)

        ## check policy
        actionMap = {'N': 'north', 'E': 'east', 'S': 'south', 'W': 'west', 'X': 'exit'}
        width, height = self.policy.width, self.policy.height
        policyPassed = True
        for x in range(width):
            for y in range(height):
                if self.policy[x][y] in actionMap and policy[(x, y)] != actionMap[self.policy[x][y]]:
                    differPoint = (x, y)
                    policyPassed = False

        if not policyPassed:
            self.addMessage('Policy not correct.')
            self.addMessage('    Student policy at %s: %s' % (differPoint, policy[differPoint]))
            self.addMessage(
                '    Correct policy at %s: %s' % (differPoint, actionMap[self.policy[differPoint[0]][differPoint[1]]]))
            self.addMessage('    Student policy:')
            self.printPolicy(policy, False)
            self.addMessage("        Legend:  N,S,E,W at states which move north etc, X at states which exit,")
            self.addMessage("                 . at states where the policy is not defined (e.g. walls)")
            self.addMessage('    Correct policy specification:')
            self.printPolicy(self.policy, True)
            self.addMessage("        Legend:  N,S,E,W for states in which the student policy must move north etc,")
            self.addMessage("                 _ for states where it doesn't matter what the student policy does.")
            self.printGridworld()
            return self._procedure_test_fail(grader)

        ## check path
        path = followPath(policy, self.grid.getStartState())

        if self.pathVisits != None and self.pathVisits not in path:
            self.addMessage('Policy does not visit state %s when moving without noise.' % (self.pathVisits,))
            self.addMessage('    States visited: %s' % (path,))
            self.addMessage('    Student policy:')
            self.printPolicy(policy, False)
            self.addMessage("        Legend:  N,S,E,W at states which move north etc, X at states which exit,")
            self.addMessage("                 . at states where policy not defined")
            self.printGridworld()
            return self._procedure_test_fail(grader)

        if self.pathNotVisits != None and self.pathNotVisits in path:
            self.addMessage('Policy visits state %s when moving without noise.' % (self.pathNotVisits,))
            self.addMessage('    States visited: %s' % (path,))
            self.addMessage('    Student policy:')
            self.printPolicy(policy, False)
            self.addMessage("        Legend:  N,S,E,W at states which move north etc, X at states which exit,")
            self.addMessage("                 . at states where policy not defined")
            self.printGridworld()
            return self._procedure_test_fail(grader)

        return self._procedure_test_pass(grader)

    def printGridworld(self):
        self.addMessage('    Gridworld:')
        for line in self.gridText.split('\n'):
            self.addMessage('     ' + line)
        self.addMessage('        Legend: # wall, _ empty, S start, numbers terminal states with that reward.')

    def printPolicy(self, policy, policyTypeIsGrid):
        if policyTypeIsGrid:
            legend = {'N': 'N', 'E': 'E', 'S': 'S', 'W': 'W', ' ': '_', 'X': 'X', '.': '.'}
        else:
            legend = {'north': 'N', 'east': 'E', 'south': 'S', 'west': 'W', 'exit': 'X', '.': '.', ' ': '_'}

        for ybar in range(self.grid.grid.height):
            y = self.grid.grid.height - 1 - ybar
            if policyTypeIsGrid:
                self.addMessage(
                    "        %s" % ("    ".join([legend[policy[x][y]] for x in range(self.grid.grid.width)]),))
            else:
                self.addMessage("        %s" % (
                    "    ".join([legend[policy.get((x, y), '.')] for x in range(self.grid.grid.width)]),))
        # for state in sorted(self.grid.getStates()):
        #     if state != 'TERMINAL_STATE':
        #         self.addMessage('      (%s,%s) %s' % (state[0], state[1], policy[state]))

    def write_solution(self, path_file_solution: str) -> bool:
        with open(path_file_solution, 'w') as handle:
            handle.write('# This is the solution file for %s.\n' % self.path)
            handle.write('# File intentionally blank.\n')
        return True
