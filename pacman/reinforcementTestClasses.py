# reinforcementTestClasses.py
# ---------------------------
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

#
# from pprint import PrettyPrinter
#
# pp = PrettyPrinter()
# VERBOSE = False
#
# LIVINGREWARD = -0.1
# NOISE = 0.2
#












#
# ### q7/q8
# ### =====
# ## Average wins of a pacman player
#
# class EvalAgentTest(TestCase):
#
#     def __init__(self, question, testDict):
#         super(EvalAgentTest, self).__init__(question, testDict)
#         self.pacmanParams = testDict['pacmanParams']
#
#         self.scoreMinimum = int(testDict['scoreMinimum']) if 'scoreMinimum' in testDict else None
#         self.nonTimeoutMinimum = int(testDict['nonTimeoutMinimum']) if 'nonTimeoutMinimum' in testDict else None
#         self.winsMinimum = int(testDict['winsMinimum']) if 'winsMinimum' in testDict else None
#
#         self.scoreThresholds = [int(s) for s in testDict.get('scoreThresholds', '').split()]
#         self.nonTimeoutThresholds = [int(s) for s in testDict.get('nonTimeoutThresholds', '').split()]
#         self.winsThresholds = [int(s) for s in testDict.get('winsThresholds', '').split()]
#
#         self.maxPoints = sum([len(t) for t in [self.scoreThresholds, self.nonTimeoutThresholds, self.winsThresholds]])
#
#     def execute(self, grader: Grader, dict_file_solution: Dict[str, Any]) -> bool:
#         self.addMessage('Grading player using command:  python pacman.py %s' % (self.pacmanParams,))
#
#         startTime = time.time()
#         games = pacman.runGames(**pacman.readCommand(self.pacmanParams.split(' ')))
#         totalTime = time.time() - startTime
#         numGames = len(games)
#
#         stats = {'time': totalTime, 'wins': [g.state_pacman.isWin() for g in games].count(True),
#                  'games': games, 'scores': [g.state_pacman.getScore() for g in games],
#                  'timeouts': [g.agentTimeout for g in games].count(True),
#                  'crashes': [g.agentCrashed for g in games].count(True)}
#
#         averageScore = sum(stats['scores']) / float(len(stats['scores']))
#         nonTimeouts = numGames - stats['timeouts']
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
#                    gradeThreshold(nonTimeouts, self.nonTimeoutMinimum, self.nonTimeoutThresholds,
#                                   "games not timed out"),
#                    gradeThreshold(wins, self.winsMinimum, self.winsThresholds, "wins")]
#
#         totalPoints = 0
#         for passed, points, value, minimum, thresholds, name in results:
#             if minimum == None and len(thresholds) == 0:
#                 continue
#
#             # print passed, points, value, minimum, thresholds, name
#             totalPoints += points
#             if not passed:
#                 assert points == 0
#                 self.addMessage("%s %s (fail: below minimum value %s)" % (value, name, minimum))
#             else:
#                 self.addMessage("%s %s (%s of %s points)" % (value, name, points, len(thresholds)))
#
#             if minimum != None:
#                 self.addMessage("    Grading scheme:")
#                 self.addMessage("     < %s:  fail" % (minimum,))
#                 if len(thresholds) == 0 or minimum != thresholds[0]:
#                     self.addMessage("    >= %s:  0 points" % (minimum,))
#                 for idx, threshold in enumerate(thresholds):
#                     self.addMessage("    >= %s:  %s points" % (threshold, idx + 1))
#             elif len(thresholds) > 0:
#                 self.addMessage("    Grading scheme:")
#                 self.addMessage("     < %s:  0 points" % (thresholds[0],))
#                 for idx, threshold in enumerate(thresholds):
#                     self.addMessage("    >= %s:  %s points" % (threshold, idx + 1))
#
#         if any([not passed for passed, _, _, _, _, _ in results]):
#             totalPoints = 0
#
#         return self.testPartial(grades, totalPoints, self.maxPoints)
#
#     def writeSolution(self, moduleDict, filePath):
#         with open(filePath, 'w') as handle:
#             handle.write('# This is the solution file for %s.\n' % self.path)
#             handle.write('# File intentionally blank.\n')
#         return True
#
#
