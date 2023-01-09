"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/27/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import List

############################################################################
#                     THE HIDDEN SECRETS OF PACMAN                         #
#                                                                          #
# You shouldn't need to look through the code in this section of the file. #
############################################################################
from pacman.agent.agent import Agent
from pacman.game.game import Game
from pacman.game.game_state import GameState
from pacman.game.layout import Layout
from pacman.graphics.graphics_pacman_display_tkiner import GraphicsPacmanDisplayTkinter

# TODO: YOU GIVE GameState SHIT TO THIS AND IT WILL VALIDATE IF GAME WIN AND STUFF IDK
class ClassicGameRules:
    """
    These game rules manage the control flow of a game, deciding when
    and how the game starts and ends.
    """

    def __init__(self, timeout=30):
        self.timeout = timeout

    def create_and_get_game(self,
                            layout: Layout,
                            agent_pacman: Agent,
                            list_agent_ghost: List[Agent],
                            display: GraphicsPacmanDisplayTkinter,
                            bool_quiet: bool = False,
                            bool_catch_exceptions: bool = False
                            ) -> Game:

        agents: List[Agent] = [agent_pacman, *list_agent_ghost[:layout.getNumGhosts()]]

        for agent in agents:
            agent.set_graphics(display)

        initState = GameState()
        initState.initialize(layout, len(list_agent_ghost))
        game = Game(agents, display, self, bool_catch_exceptions=bool_catch_exceptions)
        game.state = initState
        self.initialState = initState.get_deep_copy()

        self.bool_quiet: bool = bool_quiet

        return game

    def process(self, game_state:GameState, game):
        """
        Checks to see whether it is time to end the game.
        """
        if game_state.isWin():
            self.win(game_state, game)
        if game_state.isLose():
            self.lose(game_state, game)

    def win(self, game_state:GameState, game):
        if not self.bool_quiet:
            print("Pacman emerges victorious! Score: %d" % game_state.data.score)
        game.gameOver = True

    def lose(self, game_state:GameState, game):
        if not self.bool_quiet:
            print("Pacman died! Score: %d" % game_state.data.score)
        game.gameOver = True

    def getProgress(self, game):
        return float(game.state.getNumFood()) / self.initialState.getNumFood()

    def agentCrash(self, game, agentIndex):
        if agentIndex == 0:
            print("Pacman crashed")
        else:
            print("A ghost crashed")

    def getMaxTotalTime(self, agentIndex):
        return self.timeout

    def getMaxStartupTime(self, agentIndex):
        return self.timeout

    def getMoveWarningTime(self, agentIndex):
        return self.timeout

    def getMoveTimeout(self, agentIndex):
        return self.timeout

    def getMaxTimeWarnings(self, agentIndex):
        return 0
