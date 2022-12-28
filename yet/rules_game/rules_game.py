"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/24/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
#
# class RulesGame:
#     def __init__(self, timeout=30):
#         self.timeout = timeout
#
#     def newGame(self,
#                 layout: _layout.Layout,
#                 pacmanAgent: Agent,
#                 ghostAgents: List[Agent],
#                 display: PacmanGraphics,
#                 quiet: bool = False,
#                 catchExceptions: bool = False
#                 ):
#
#         agents: List[Agent] = [pacmanAgent, *ghostAgents[:layout.getNumGhosts()]]
#         initState = GameState()
#         initState.initialize(layout, len(ghostAgents))
#         game = Game(agents, display, self, catchExceptions=catchExceptions)
#         game.state = initState
#         self.initialState = initState.deepCopy()
#         self.quiet = quiet
#         return game
#
#
#