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
from __future__ import annotations

from functools import cache
from functools import cached_property
from functools import lru_cache
from pprint import pprint
from typing import Dict
from typing import List
from typing import TYPE_CHECKING
from typing import Tuple
from typing import Union

from common.grid import reconstituteGrid
from common.util import nearestPoint
from pacman.agent.container_state import ContainerState
from pacman.game.container_position_vector import ContainerPositionVector
from pacman.game.directions import Directions
from pacman.game.grid_pacman import GridPacman
from pacman.game.type_player import TypePlayerPacman

if TYPE_CHECKING:
    from pacman.game.player_pacman import PlayerPacman
    from pacman.game.layoutpacman import LayoutPacman
    from pacman.agent import Agent


class StateDataPacman:

    def __init__(self, state_date_previous: Union[StateDataPacman, None] = None):
        """
        Generates a new data packet by copying information from its predecessor.
        """
        if isinstance(state_date_previous, StateDataPacman):
            self.grid_food: GridPacman = state_date_previous.grid_food.shallowCopy()
            self.list_capsule: List[Tuple[int, ...]] = state_date_previous.list_capsule.copy()

            self.dict_k_player_v_container_state: Dict[PlayerPacman, ContainerState] = (
                self._get_dict_k_player_v_container_state_copy(
                    state_date_previous.dict_k_player_v_container_state
                )
            )

            self.layout: LayoutPacman = state_date_previous.layout
            self._dict_k_player_v_bool_eaten: Dict[PlayerPacman, bool] = (
                state_date_previous._dict_k_player_v_bool_eaten
            )
            self.score: int = state_date_previous.score

            ###

            self.dict_k_agent_v_player: Dict[Agent, PlayerPacman] = state_date_previous.dict_k_agent_v_player

            # FIXME: UGLY DESIGN
            self.dict_k_agent_v_index: Dict[Agent, int] = state_date_previous.dict_k_agent_v_index
            self.dict_k_index_v_agent: Dict[int, Agent] = state_date_previous.dict_k_index_v_agent

            self._player_pacman = state_date_previous._player_pacman  # TODO: DIRTY TRICK BYPASS
        else:
            self.dict_k_agent_v_player: Dict[Agent, PlayerPacman] = {}

            self.dict_k_agent_v_index = {}
            self.dict_k_index_v_agent = {}

            self._player_pacman: PlayerPacman = None  # TODO: DIRTY TRICK BYPASS

        self._foodEaten = None
        self._foodAdded = None
        self._capsuleEaten = None
        self._agentMoved: Union[Agent, None] = None
        self._lose: bool = False
        self._win: bool = False
        self.scoreChange = 0

        ######

        self.__hash_calculated = None


    def get_agent_by_index(self, index: int) -> Union[Agent, None]:
        return self.dict_k_index_v_agent.get(index)

    def get_index_by_agent(self, agent: Agent) -> Union[int, None]:
        return self.dict_k_agent_v_index.get(agent)

    def get_dict_k_player_v_container_state(self) -> Dict[PlayerPacman, ContainerState]:
        return self.dict_k_player_v_container_state

    def get_dict_k_agent_v_player(self) -> Dict[Agent, PlayerPacman]:
        return self.dict_k_agent_v_player

    def get_player_from_agent(self, agent: Agent) -> Union[PlayerPacman, None]:
        return self.dict_k_agent_v_player.get(agent)

    def get_deep_copy(self) -> StateDataPacman:
        state_data_new = StateDataPacman(self)

        state_data_new.grid_food = self.grid_food.deepCopy()
        state_data_new.layout = self.layout.deepCopy()

        state_data_new._agentMoved = self._agentMoved
        state_data_new._foodEaten = self._foodEaten
        state_data_new._foodAdded = self._foodAdded
        state_data_new._capsuleEaten = self._capsuleEaten

        # # COPY BY REFERENCE JOSEPH CUSTOM  # TODO: ALREADY CALLED IN TEH
        # state_data_new.dict_k_agent_v_player = self.dict_k_agent_v_player
        # state_data_new.dict_k_agent_v_index = self.dict_k_agent_v_index
        # state_data_new.dict_k_index_v_agent = self.dict_k_index_v_agent
        # state_data_new._player_pacman = self._player_pacman

        return state_data_new

    def _get_dict_k_player_v_container_state_copy(self,
                                                  dict_k_player_v_container_state: Dict[PlayerPacman, ContainerState]
                                                  ) -> Dict[PlayerPacman, ContainerState]:

        # return [state_agent.copy() for state_agent in dict_k_player_v_container_state]
        return {player: container_state.copy() for player, container_state
                in dict_k_player_v_container_state.items()}

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        if other == None:
            return False

        # TODO Check for type of other
        # if not self.dict_k_player_v_container_state == other.dict_k_player_v_container_state:  # TODO: ACTUALLY WRONG
        #     return False
        if not self.grid_food == other.grid_food:
            return False
        if not self.list_capsule == other.list_capsule:
            return False
        if not self.score == other.score:
            return False
        return True

    def __hash__(self):  # FIXME: FIX THIS UGLY
        """
        Allows states to be keys of dictionaries.
        """
        # for i, state_pacman in enumerate(self.dict_k_player_v_container_state):
        #     try:
        #         int(hash(state_pacman))
        #     except TypeError as e:
        #         print(e)
        #         # hash(state_pacman)

        # return int(
        #     (hash(tuple(self.dict_k_player_v_container_state)) +
        #      13 * hash(self.grid_food) +
        #      113 * hash(tuple(self.list_capsule)) +
        #      7 * hash(self.score)) % 1048575
        # )

        # pprint(tuple(self.dict_k_player_v_container_state.values()))
        # print(self.grid_food)
        # print(self.list_capsule)
        # print(self.score)
        # print()


        if self.__hash_calculated:  # TODO: THIS IS ULTRA DANGEROUS CACHING HASH
            return self.__hash_calculated

        # # IMPORTANT: USE .values() OR ELSE HAS WILL BE SLOW
        hash_ = hash((
            tuple(self.dict_k_player_v_container_state.values()),
            self.grid_food,
            tuple(self.list_capsule),
            self.score,
        ))

        self.__hash_calculated = hash_

        return hash_


    def __str__(self):
        width, height = self.layout.width, self.layout.height
        map = GridPacman(width, height)
        if type(self.grid_food) == type((1, 2)):
            self.grid_food = reconstituteGrid(self.grid_food)
        for x in range(width):
            for y in range(height):
                walls: GridPacman
                food: GridPacman
                food, walls = self.grid_food, self.layout.walls
                map[x][y] = self._get_str_food_or_wall_from_bool_food_or_wall(food[x][y], walls[x][y])

        for player, container_state in self.dict_k_player_v_container_state.items():
            if container_state is None:
                continue
            if container_state.container_position_vector is None:
                continue
            x, y = [int(i) for i in nearestPoint(container_state.container_position_vector.position)]
            agent_dir = container_state.container_position_vector.direction

            if player.get_type_player_pacman() == TypePlayerPacman.PACMAN:
                map[x][y] = self._get_str_pacman_from_direction(agent_dir)
            else:
                map[x][y] = self._get_str_ghost_from_direction(agent_dir)

        for x, y in self.list_capsule:
            map[x][y] = 'o'

        return str(map) + ("\nScore: %d\n" % self.score)

    def _get_str_food_or_wall_from_bool_food_or_wall(self, bool_food: bool, bool_wall: bool) -> str:
        if bool_food:
            return '.'
        elif bool_wall:
            return '%'
        else:
            return ' '

    def _get_str_pacman_from_direction(self, direction: Directions) -> str:
        if direction == Directions.NORTH:
            return 'v'
        if direction == Directions.SOUTH:
            return '^'
        if direction == Directions.WEST:
            return '>'
        return '<'

    def _get_str_ghost_from_direction(self, direction: Directions) -> str:
        return 'G'

        if direction == Directions.NORTH:
            return 'M'
        if direction == Directions.SOUTH:
            return 'W'
        if direction == Directions.WEST:
            return '3'
        return 'E'

    def initialize(self, layout: LayoutPacman, list_player: List[PlayerPacman]):
        """
        Creates an initial game state_pacman from a str_path_layout array (see str_path_layout.py).

        Notes:
            Should be called once.
        """
        self.grid_food: GridPacman = layout.food.copy()

        # self.list_capsule = []
        self.list_capsule: List[Tuple[int, ...]] = layout.list_capsule[:]
        self.layout: LayoutPacman = layout
        self.score: int = 0
        self.scoreChange: int = 0

        self.dict_k_player_v_container_state: Dict[PlayerPacman, ContainerState] = {}

        # PlayerType
        count_number_of_agent_ghosts = 0  # TODO: REMOVE THIS

        list_player_temp = list_player.copy()  # Shallow copy

        # print("_____LAY", layout.list_tuple__type_player__position)
        for type_player, position in layout.list_tuple__type_player__position:

            # # Ghost adder
            # if not type_player:
            #     if count_number_of_agent_ghosts == number_of_agent_ghost:
            #         continue  # Max ghosts reached already
            #     else:
            #         count_number_of_agent_ghosts += 1
            #
            # self.dict_k_player_v_container_state.append(
            #     ContainerState(ContainerPositionVector(position, Directions.STOP), is_pacman)  # TODO: CONSTRUCTOR HERE
            # )

            for index_player, player in enumerate(list_player_temp):

                if player.get_type_player_pacman() == type_player:
                    list_player_temp.pop(index_player)

                    container_position_vector = ContainerPositionVector(position, Directions.STOP)

                    self.dict_k_player_v_container_state[player] = (
                        ContainerState(container_position_vector)
                    )

                    self.dict_k_agent_v_player[player.get_agent()] = player

                    _index_agent = len(self.dict_k_agent_v_player) - 1

                    self.dict_k_agent_v_index[player.get_agent()] = _index_agent
                    self.dict_k_index_v_agent[_index_agent] = player.get_agent()

                    #############
                    # FUCK ULTRA BYPASS  # TODO: FIX ME TO SUPPORT MORE PACMAN

                    if player.get_type_player_pacman() == TypePlayerPacman.PACMAN:
                        self._player_pacman = player

                    break

        # self._dict_k_player_v_bool_eaten = [False for a in self.dict_k_player_v_container_state]  # TODO: THIS FIX PLS
        self._dict_k_player_v_bool_eaten = {player: False for player in self.dict_k_player_v_container_state}
