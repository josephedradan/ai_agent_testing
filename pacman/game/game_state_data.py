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

from typing import List
from typing import Tuple
from typing import Union

from common.grid import reconstituteGrid
from pacman.agent.state_agent import StateAgent
from pacman.game.container_vector import ContainerVector
from pacman.game.directions import Directions
from pacman.game.grid_pacman import GridPacman
from pacman.game.layout import Layout
from common.util import nearestPoint


class GameStateData:

    def __init__(self, game_state_date_previous: Union[GameStateData, None] = None):
        """
        Generates a new data packet by copying information from its predecessor.
        """
        if game_state_date_previous is not None:
            self.grid_food: GridPacman = game_state_date_previous.grid_food.shallowCopy()
            self.list_capsule: List[Tuple[int, ...]] = game_state_date_previous.list_capsule.copy()
            self.list_state_agent: List[StateAgent] = self.get_list_state_agent_copy(
                game_state_date_previous.list_state_agent
            )
            self.layout: Layout = game_state_date_previous.layout
            self._eaten: List[bool] = game_state_date_previous._eaten
            self.score: int = game_state_date_previous.score

        self._foodEaten = None
        self._foodAdded = None
        self._capsuleEaten = None
        self._agentMoved = None
        self._lose: bool = False
        self._win: bool = False
        self.scoreChange = 0

    def get_deep_copy(self) -> GameStateData:
        game_state_data = GameStateData(self)

        game_state_data.grid_food = self.grid_food.deepCopy()
        game_state_data.layout = self.layout.deepCopy()
        game_state_data._agentMoved = self._agentMoved
        game_state_data._foodEaten = self._foodEaten
        game_state_data._foodAdded = self._foodAdded
        game_state_data._capsuleEaten = self._capsuleEaten

        return game_state_data

    def get_list_state_agent_copy(self, list_state_agent: List[StateAgent]) -> List[StateAgent]:
        return [state_agent.copy() for state_agent in list_state_agent]

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        if other == None:
            return False

        # TODO Check for type of other
        if not self.list_state_agent == other.list_state_agent:
            return False
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
        # for i, state in enumerate(self.list_state_agent):
        #     try:
        #         int(hash(state))
        #     except TypeError as e:
        #         print(e)
        #         # hash(game_state)

        # return int(
        #     (hash(tuple(self.list_state_agent)) +
        #      13 * hash(self.grid_food) +
        #      113 * hash(tuple(self.list_capsule)) +
        #      7 * hash(self.score)) % 1048575
        # )

        hash_ = hash(
            (hash(tuple(self.list_state_agent)),
             hash(self.grid_food),
             hash(tuple(self.list_capsule)),
             hash(self.score),
             )
        )
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

        for staet_agent in self.list_state_agent:
            if staet_agent is None:
                continue
            if staet_agent.container_vector is None:
                continue
            x, y = [int(i) for i in nearestPoint(staet_agent.container_vector.position)]
            agent_dir = staet_agent.container_vector.direction
            if staet_agent.is_pacman:
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

    def initialize(self, layout: Layout, number_of_agent_ghost: int):
        """
        Creates an initial game game_state from a layout array (see layout.py).
        """
        self.grid_food: GridPacman = layout.food.copy()

        # self.list_capsule = []
        self.list_capsule: List[Tuple[int, ...]] = layout.list_capsule[:]
        self.layout: Layout = layout
        self.score: int = 0
        self.scoreChange: int = 0

        self.list_state_agent: List[StateAgent] = []

        count_number_of_agent_ghosts = 0
        for isPacman, pos in layout.agentPositions:
            if not isPacman:
                if count_number_of_agent_ghosts == number_of_agent_ghost:
                    continue  # Max list_agent_ghost reached already
                else:
                    count_number_of_agent_ghosts += 1
            self.list_state_agent.append(
                StateAgent(ContainerVector(pos, Directions.STOP), isPacman)
            )
        self._eaten = [False for a in self.list_state_agent]
