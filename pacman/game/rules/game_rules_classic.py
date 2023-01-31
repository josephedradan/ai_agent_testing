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
from typing import Dict
from typing import List
############################################################################
#                     THE HIDDEN SECRETS OF PACMAN                         #
#                                                                          #
# You shouldn't need to look through the code in this section of the file. #
############################################################################
from typing import Tuple
from typing import Type
from typing import Union

from common.game_state_pacman import GameStatePacman
from pacman.agent import AgentKeyboard
from pacman.agent import get_subclass_agent
from pacman.agent.agent import Agent
from pacman.game.game import Game
from pacman.game.layout import get_layout
from pacman.game.player import Player
from pacman.game.player_ghost import PlayerPacman
from pacman.game.player_pacman import PlayerGhost
from pacman.graphics import GraphicsPacman
from pacman.graphics import GraphicsPacmanDisplay


class ClassicGameRules:
    """
    These game rules manage the control flow of a game, deciding when
    and how the game starts and ends.
    """

    def __init__(self, timeout=30):
        self.timeout = timeout

    def get_players(self,
                    list_tuple__str_agent__dict_kwargs: List[Tuple[str, Dict[str, Union[str, int]]]],
                    subclass_player: Type[Player]) -> List[Player]:

        list_player: List[Player] = []

        for tuple__str_agent__dict_kwargs in list_tuple__str_agent__dict_kwargs:
            str_agent = tuple__str_agent__dict_kwargs[0]
            dict_kwargs = tuple__str_agent__dict_kwargs[1]

            subclass_agent = get_subclass_agent(str_agent)

            agent = subclass_agent(**dict_kwargs)

            player = subclass_player(agent)

            list_player.append(player)

        return list_player

    def create_and_get_game(self,
                            str_path_layout: str,
                            list_tuple__str_agent_pacman__dict_kwargs: List[Tuple[str, Dict[str, Union[str, int]]]],
                            list_tuple__str_agent_ghost__dict_kwargs: List[Tuple[str, Dict[str, Union[str, int]]]],
                            graphics_pacman: GraphicsPacman,
                            bool_quiet: bool = False,
                            bool_catch_exceptions: bool = False
                            ) -> Game:

        layout = get_layout(str_path_layout)

        list_player_pacman = self.get_players(list_tuple__str_agent_pacman__dict_kwargs, PlayerPacman)
        list_player_ghost = self.get_players(list_tuple__str_agent_ghost__dict_kwargs, PlayerGhost)

        list_player_all: List[Player] = [*list_player_pacman, *list_player_ghost]

        # list_agent: List[Agent] = [agent_pacman, *list_str_pacman_ghost_class_agent[:layout.getNumGhosts()]]



        # TODO JOSEPH SPEICAL
        # TODO: ALT GRAPHICS: GraphicsPacmanNull, GraphicsPacmanDisplay
        if isinstance(agent_pacman, AgentKeyboard) and isinstance(graphics_pacman, GraphicsPacmanDisplay):
            agent_pacman.set_display(graphics_pacman.get_display())

        for agent in list_agent:
            agent.set_graphics_pacman(graphics_pacman)

        game_state_start = GameStatePacman()
        game_state_start.initialize(layout, len(list_str_pacman_ghost_class_agent))

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

    def process(self, game_state: GameStatePacman, game: Game):
        """
        Checks to see whether it is time to end the game.
        """
        if game_state.isWin():
            self._win(game_state, game)
        if game_state.isLose():
            self._lose(game_state, game)

    def _win(self, game_state: GameStatePacman, game: Game):
        if not self.bool_quiet:
            print(f"Pacman emerges victorious! Score: {game_state.game_state_data.score}")
        game.gameOver = True

    def _lose(self, game_state: GameStatePacman, game: Game):
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
