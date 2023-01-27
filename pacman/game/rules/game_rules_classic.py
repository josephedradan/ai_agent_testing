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
from pacman.graphics import GraphicsPacman


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
                            graphics_pacman: GraphicsPacman,
                            bool_quiet: bool = False,
                            bool_catch_exceptions: bool = False
                            ) -> Game:

        list_agent: List[Agent] = [agent_pacman, *list_agent_ghost[:layout.getNumGhosts()]]

        for agent in list_agent:
            agent.set_graphics_pacman(graphics_pacman)

        game_state_start = GameState()
        game_state_start.initialize(layout, len(list_agent_ghost))

        game = Game(
            list_agent,
            graphics_pacman,
            self,
            bool_catch_exceptions=bool_catch_exceptions
        )

        game.game_state = game_state_start

        self.initialState = game_state_start.get_deep_copy()

        self.bool_quiet: bool = bool_quiet

        return game

    def set_quiet(self, bool_quiet: bool):
        self.bool_quiet = bool_quiet

    def process(self, game_state: GameState, game: Game):
        """
        Checks to see whether it is time to end the game.
        """
        if game_state.isWin():
            self._win(game_state, game)
        if game_state.isLose():
            self._lose(game_state, game)

    def _win(self, game_state: GameState, game: Game):
        if not self.bool_quiet:
            print(f"Pacman emerges victorious! Score: {game_state.game_state_data.score}")
        game.gameOver = True

    def _lose(self, game_state: GameState, game: Game):
        if not self.bool_quiet:
            print(f"Pacman died! Score: {game_state.game_state_data.score}")
        game.gameOver = True

    def getProgress(self, game: Game):
        return float(game.game_state.getNumFood()) / self.initialState.getNumFood()

    def agentCrash(self, game: Game, agentIndex):
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
