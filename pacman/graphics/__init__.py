"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/9/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import Type
from typing import Union

from common.graphics.graphics import Graphics
from pacman.graphics.graphics_pacman_gui import FirstPersonGraphicsPacman
from pacman.graphics.graphics_pacman_gui import GraphicsPacmanGUI
from pacman.graphics.graphics_pacman_null import GraphicsPacmanNull
from pacman.graphics.graphics_pacman_terminal import GraphicsPacmanTerminal

LIST_GRAPHICS_PACMAN = [
    # Graphics,  # This is abstract
    GraphicsPacmanNull,
    GraphicsPacmanTerminal,
    GraphicsPacmanGUI,
    FirstPersonGraphicsPacman,
]

DICT_K_NAME_GRAPHICS_PACMAN_V_GRAPHICS_PACMAN = {
    graphics_pacman_.__name__: graphics_pacman_ for graphics_pacman_ in LIST_GRAPHICS_PACMAN
}


def get_class_graphics_pacman(name_graphics_pacman: Union[str, Type[Graphics], None]) -> Type[Graphics]:
    graphics_pacman_ = name_graphics_pacman

    if isinstance(name_graphics_pacman, str):
        graphics_pacman_ = DICT_K_NAME_GRAPHICS_PACMAN_V_GRAPHICS_PACMAN.get(name_graphics_pacman)

    if graphics_pacman_ is None:
        Exception("{} is not an Graphics class".format(name_graphics_pacman))

    return graphics_pacman_
