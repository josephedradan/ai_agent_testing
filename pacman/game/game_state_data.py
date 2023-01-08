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

from pacman.agent.state_agent import StateAgent
from pacman.game.container_vector import ContainerVector
from pacman.game.directions import Directions
from pacman.game.grid import Grid
from pacman.game.grid import reconstituteGrid
from pacman.game.layout import Layout
from pacman.util import nearestPoint


class GameStateData:

    def __init__(self, game_state_date_previous: Union[GameStateData, None] = None):
        """
        Generates a new data packet by copying information from its predecessor.
        """
        if game_state_date_previous is not None:
            self.food: Grid = game_state_date_previous.food.shallowCopy()
            self.list_capsule: List[Tuple[int, ...]] = game_state_date_previous.list_capsule[:]
            self.list_state_agent: List[StateAgent] = self.get_list_state_agent_copy(game_state_date_previous.list_state_agent)
            self.layout: Layout = game_state_date_previous.layout
            self._eaten = game_state_date_previous._eaten
            self.score = game_state_date_previous.score

        self._foodEaten = None
        self._foodAdded = None
        self._capsuleEaten = None
        self._agentMoved = None
        self._lose = False
        self._win = False
        self.scoreChange = 0

    def get_deep_copy(self) -> GameStateData:
        game_state_data = GameStateData(self)

        game_state_data.food = self.food.deepCopy()
        game_state_data.layout = self.layout.deepCopy()
        game_state_data._agentMoved = self._agentMoved
        game_state_data._foodEaten = self._foodEaten
        game_state_data._foodAdded = self._foodAdded
        game_state_data._capsuleEaten = self._capsuleEaten

        return game_state_data

    def get_list_state_agent_copy(self, list_state_agent: List[StateAgent]):
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
        if not self.food == other.food:
            return False
        if not self.list_capsule == other.list_capsule:
            return False
        if not self.score == other.score:
            return False
        return True

    def __hash__(self):
        """
        Allows states to be keys of dictionaries.
        """
        for i, state in enumerate(self.list_state_agent):
            try:
                int(hash(state))
            except TypeError as e:
                print(e)
                # hash(game_state)

        return int((hash(tuple(self.list_state_agent)) + 13 * hash(self.food) + 113 * hash(tuple(self.list_capsule)) + 7 * hash(
            self.score)) % 1048575)

    def __str__(self):
        width, height = self.layout.width, self.layout.height
        map = Grid(width, height)
        if type(self.food) == type((1, 2)):
            self.food = reconstituteGrid(self.food)
        for x in range(width):
            for y in range(height):
                food, walls = self.food, self.layout.walls
                map[x][y] = self._foodWallStr(food[x][y], walls[x][y])

        for agentState in self.list_state_agent:
            if agentState == None:
                continue
            if agentState.container_vector == None:
                continue
            x, y = [int(i) for i in nearestPoint(agentState.container_vector.position)]
            agent_dir = agentState.container_vector.direction
            if agentState.is_pacman:
                map[x][y] = self._pacStr(agent_dir)
            else:
                map[x][y] = self._ghostStr(agent_dir)

        for x, y in self.list_capsule:
            map[x][y] = 'o'

        return str(map) + ("\nScore: %d\n" % self.score)

    def _foodWallStr(self, hasFood, hasWall):
        if hasFood:
            return '.'
        elif hasWall:
            return '%'
        else:
            return ' '

    def _pacStr(self, dir):
        if dir == Directions.NORTH:
            return 'v'
        if dir == Directions.SOUTH:
            return '^'
        if dir == Directions.WEST:
            return '>'
        return '<'

    def _ghostStr(self, dir):
        return 'G'
        if dir == Directions.NORTH:
            return 'M'
        if dir == Directions.SOUTH:
            return 'W'
        if dir == Directions.WEST:
            return '3'
        return 'E'

    def initialize(self, layout, numGhostAgents):
        """
        Creates an initial game game_state from a layout array (see layout.py).
        """
        self.food = layout.food.copy()
        # self.list_capsule = []
        self.list_capsule = layout.list_capsule[:]
        self.layout = layout
        self.score = 0
        self.scoreChange = 0

        self.list_state_agent = []
        numGhosts = 0
        for isPacman, pos in layout.agentPositions:
            if not isPacman:
                if numGhosts == numGhostAgents:
                    continue  # Max list_agent_ghost reached already
                else:
                    numGhosts += 1
            self.list_state_agent.append(StateAgent(
                ContainerVector(pos, Directions.STOP), isPacman))
        self._eaten = [False for a in self.list_state_agent]
