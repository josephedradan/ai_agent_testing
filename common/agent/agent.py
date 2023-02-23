"""
Date created: 12/24/2022

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
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Hashable
from typing import TYPE_CHECKING
from typing import Union

from pacman.game.actiondirection import Action

if TYPE_CHECKING:
    from common.state import State
    from common.player import Player


# T_PLAYER = TypeVar('T_PLAYER', bound=Player)  # TODO: MAYBE USE THIS, BUT IT WILL GET VERY COMPLEX


class Agent(ABC):
    """
    An player must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state: State): # inspects the starting state
    """
    player: Union[Player, None]
    kwargs: Dict[Hashable, Any]

    def __init_subclass__(cls, **kwargs):
        print("THINGY", cls)

    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.player = None

    def initialize(self, player: Player):
        self.player: Player = player

    @abstractmethod
    def getAction(self, state: State) -> Action:
        """
        The Agent will receive a State (from either {pacman, capture, sonar}.py) and
        must return an action from ActionDirection.{North, South, East, West, Stop}
        """
        pass

    def registerInitialState(self, state: State):
        """
        Hidden function used by test cases and stuff, use it if you know what you are doing

        """
        pass

    def get_player(self) -> Union[Player, None]:
        return self.player
