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
from typing import Union

from common.state_pacman import StatePacman
from pacman.agent import Agent
from pacman.game.game import Game
from pacman.game.layoutpacman import LayoutPacman
from pacman.game.layoutpacman import get_layout_pacman
from pacman.game.player_pacman import PlayerPacman
from pacman.game.type_player_pacman import TypePlayerPacman
from pacman.graphics.graphics_pacman import GraphicsPacman


class ClassicGameRules:
    """
    These game rules manage the control flow of a game, deciding when
    and how the game starts and ends.
    """

    def __init__(self, timeout=30):
        self.timeout = timeout

        self._state_pacman_initial: Union[StatePacman, None] = None

    def get_players(self,
                    list_agent: List[Agent],
                    type_player: TypePlayerPacman,
                    graphics_pacman: GraphicsPacman
                    ) -> List[PlayerPacman]:

        list_player: List[PlayerPacman] = []

        for agent in list_agent:

            player = PlayerPacman(graphics_pacman.gui,
                                  graphics_pacman,
                                  agent,
                                  type_player)

            agent.initialize(player)

            list_player.append(player)

        return list_player

    def create_and_get_game(self,
                            str_path_layout: str,
                            list_agent_pacman: List[Agent],
                            list_agent_ghost: List[Agent],
                            graphics_pacman: GraphicsPacman,
                            bool_quiet: bool = False,
                            bool_catch_exceptions: bool = False
                            ) -> Game:

        layout_pacman: LayoutPacman = get_layout_pacman(str_path_layout)

        list_player_pacman = self.get_players(list_agent_pacman,
                                              TypePlayerPacman.PACMAN,
                                              graphics_pacman)

        list_player_ghost = self.get_players(list_agent_ghost,
                                             TypePlayerPacman.GHOST,
                                             graphics_pacman)

        list_player_all: List[PlayerPacman] = [*list_player_pacman, *list_player_ghost]
        # list_player: List[Agent] = [agent_pacman, *list_str_pacman_ghost_class_agent[:layout_pacman.getNumGhosts()]]

        # # TODO JOSEPH SPEICAL
        # # TODO: ALT GRAPHICS: GraphicsPacmanNull, GraphicsPacmanDisplay
        # if isinstance(agent_pacman, AgentKeyboard) and isinstance(graphics_pacman, GraphicsPacmanDisplay):
        #     agent_pacman.set_display(graphics_pacman.get_display())
        #
        # for agent in list_player:
        #     agent.set_graphics(graphics_pacman)

        state_pacman_start = StatePacman()
        state_pacman_start.initialize(layout_pacman, list_player_all)

        list_player_all_allowed_by_map: List[PlayerPacman] = list(  # TODO: FIX MOVE ME IN A GAME CREATOR OS SOMESHIT
            state_pacman_start.get_dict_k_player_v_container_state().keys()
        )
        # print("----- create_and_get_game ALL PLAYERS", list_player_all_allowed_by_map)
        game = Game(
            list_player_all_allowed_by_map,
            graphics_pacman,
            self,
            bool_catch_exceptions=bool_catch_exceptions
        )

        game.set_state_pacman(state_pacman_start)

        self._state_pacman_initial = state_pacman_start.get_deep_copy()

        self.bool_quiet: bool = bool_quiet

        return game

    def set_quiet(self, bool_quiet: bool):
        self.bool_quiet = bool_quiet

    def process(self, state: StatePacman, game: Game):
        """
        Checks to see whether it is time to end the game.
        """
        if state.isWin():
            self._win(state, game)
        if state.isLose():
            self._lose(state, game)

    def _win(self, state: StatePacman, game: Game):
        if not self.bool_quiet:
            print(f"Pacman emerges victorious! Score: {state.state_data.score}")
        game.gameOver = True

    def _lose(self, state: StatePacman, game: Game):
        if not self.bool_quiet:
            print(f"Pacman died! Score: {state.state_data.score}")
        game.gameOver = True

    def getProgress(self, game: Game):
        return float(game.state_pacman.getNumFood()) / self._state_pacman_initial.getNumFood()

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
