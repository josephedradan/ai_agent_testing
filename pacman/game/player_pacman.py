"""
Date created: 1/30/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Contributors: 
    https://github.com/josephedradan

Reference:

"""
from typing import TYPE_CHECKING

from common.graphics.gui import GUI
from common.player import Player
from pacman.agent import Agent
from pacman.game.type_player_pacman import TypePlayerPacman
from pacman.graphics.graphics_pacman import GraphicsPacman

if TYPE_CHECKING:
    pass


class PlayerPacman(Player[GUI, GraphicsPacman]):
    type_player: TypePlayerPacman
    __counter = 1

    def __init__(self, gui: GUI, graphics: GraphicsPacman, agent: Agent, type_player: TypePlayerPacman):
        super().__init__(gui, graphics, agent)

        self.type_player = type_player

        # DIRTY COLORING TRICK

        self.index = PlayerPacman.__counter
        PlayerPacman.__counter += 1

    def set_type_player_pacman(self, type_player: TypePlayerPacman):
        self.type_player = type_player

    def get_type_player_pacman(self) -> TypePlayerPacman:
        return self.type_player

