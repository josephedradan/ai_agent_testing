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
from typing import Any
from typing import Dict

from pacman.agent.search import get_search_function
from pacman.agent.search_problem.search_problem_graph_search import GraphSearch
from common.grader import Grader
from pacman.test_case import TestCase


class GraphSearchTest(TestCase):

    def __init__(self, question, testDict):
        super(GraphSearchTest, self).__init__(question, testDict)
        self.graph_text = testDict['graph']
        self.alg = testDict['algorithm']
        self.diagram = testDict['diagram']
        self.exactExpansionOrder = testDict.get('exactExpansionOrder', 'True').lower() == "true"

        if 'heuristic' in testDict:
            self.heuristic = parseHeuristic(testDict['heuristic'])
            # self.heuristic = get_heuristic_function(testDict['heuristic'])
        else:
            self.heuristic = None

    # Note that the return type of this function is a tripple:
    # (solution, expanded states, error message)
    def getSolInfo(self):
        # alg = getattr(search, self.alg)
        alg = get_search_function(self.alg)

        problem = GraphSearch(self.graph_text)

        if self.heuristic != None:
            solution = alg(problem, self.heuristic)
        else:
            solution = alg(problem)

        if type(solution) != type([]):
            return None, None, 'The result of %s must be a list. (Instead, it is %s)' % (self.alg, type(solution))

        return solution, problem.getExpandedStates(), None

    # Run student code.  If an error message is returned, print error and return false.
    # If a good solution is returned, printn the solution and return true; otherwise,
    # print both the correct and student's solution and return false.
    def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']
        gold_solution = [str.split(dict_file_solution['solution']), str.split(dict_file_solution['rev_solution'])]
        gold_expanded_states = [str.split(dict_file_solution['expanded_states']),
                                str.split(dict_file_solution['rev_expanded_states'])]

        solution, expanded_states, error = self.getSolInfo()
        if error != None:
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('\t%s' % error)
            return False

        if solution in gold_solution and (not self.exactExpansionOrder or expanded_states in gold_expanded_states):
            grader.addMessage('PASS: %s' % self.path_file_test)
            grader.addMessage('\tsolution:\t\t%s' % solution)
            grader.addMessage('\texpanded_states:\t%s' % expanded_states)
            return True
        else:
            grader.addMessage('FAIL: %s' % self.path_file_test)
            grader.addMessage('\tgraph:')
            for line in self.diagram.split('\n'):
                grader.addMessage('\t    %s' % (line,))
            grader.addMessage('\tstudent solution:\t\t%s' % solution)
            grader.addMessage('\tstudent expanded_states:\t%s' % expanded_states)
            grader.addMessage('')
            grader.addMessage('\tcorrect solution:\t\t%s' % gold_solution[0])
            grader.addMessage('\tcorrect expanded_states:\t%s' % gold_expanded_states[0])
            grader.addMessage('\tcorrect rev_solution:\t\t%s' % gold_solution[1])
            grader.addMessage('\tcorrect rev_expanded_states:\t%s' % gold_expanded_states[1])
            return False

    def write_solution(self, path_file_solution: str) -> bool:
        # search = moduleDict['search']
        # searchAgents = moduleDict['searchAgents']
        # open file and write comments
        handle = open(path_file_solution, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path_file_test)
        handle.write('# This solution is designed to support both right-to-left\n')
        handle.write('# and left-to-right implementations.\n')

        # write forward solution
        solution, expanded_states, error = self.getSolInfo()
        if error != None: raise Exception("Error in solution code: %s" % error)
        handle.write('solution: "%s"\n' % ' '.join(solution))
        handle.write('expanded_states: "%s"\n' % ' '.join(expanded_states))

        # reverse and write backwards solution
        search.REVERSE_PUSH = not search.REVERSE_PUSH
        solution, expanded_states, error = self.getSolInfo()
        if error != None: raise Exception("Error in solution code: %s" % error)
        handle.write('rev_solution: "%s"\n' % ' '.join(solution))
        handle.write('rev_expanded_states: "%s"\n' % ' '.join(expanded_states))

        # clean up
        search.REVERSE_PUSH = not search.REVERSE_PUSH
        handle.close()
        return True


def parseHeuristic(heuristicText):  # FIXME: MOVE ME TO heuristic_function
    heuristic = {}
    for line in heuristicText.split('\n'):
        tokens = line.split()
        if len(tokens) != 2:
            print("Broken heuristic:")
            print('"""%s"""' % heuristicText)
            raise Exception("GraphSearch heuristic specification broken at tokens:" + str(tokens))
        state, h = tokens
        heuristic[state] = float(h)

    def graphHeuristic(state, problem=None):
        if state in heuristic:
            return heuristic[state]
        else:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            print("Heuristic:")
            pp.pprint(heuristic)
            raise Exception("Graph heuristic called with invalid state: " + str(state))

    return graphHeuristic
