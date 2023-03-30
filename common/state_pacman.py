"""
Date created: 1/29/2023

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

from typing import Dict
from typing import List
from typing import TYPE_CHECKING
from typing import Union

from common.state import State
from common.state_data_pacman import StateDataPacman
from pacman.agent import Agent
from pacman.agent.container_state import ContainerState
from pacman.game.rules.common import TIME_PENALTY
from pacman.game.rules.rules_pacman import RulesPacman
from pacman.game.rules.rules_pacman_ghost import RulesPacmanGhost
from pacman.game.rules.rules_pacman_pacman import RulesPacmanPacman
from pacman.game.type_player_pacman import EnumPlayerPacman

if TYPE_CHECKING:
    from pacman.types_ import TYPE_VECTOR
    from pacman.game.player_pacman import PlayerPacman
    from pacman.game.action_direction import Action
    from pacman.game.layout_pacman import LayoutPacman


class StatePacman(State):
    dict_k_type_player_pacman_v_rules_pacman: Dict[EnumPlayerPacman, RulesPacman] = {
        EnumPlayerPacman.PACMAN: RulesPacmanPacman,
        EnumPlayerPacman.GHOST: RulesPacmanGhost
    }


    state_data_pacman: StateDataPacman

    def __init__(self, state_previous: Union[StatePacman, None] = None):
        """
        Generates a new StatePacman by copying information from its predecessor.
        """

        if isinstance(state_previous, StatePacman):
            self.state_data_pacman = StateDataPacman(state_previous.state_data_pacman)
        else:
            self.state_data_pacman = StateDataPacman()

    def initialize(self, layout: LayoutPacman, list_player: List[PlayerPacman]):
        """
        Initializes self.state_data, this should be called once

        """
        self.state_data_pacman.initialize(layout, list_player)

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        # return hasattr(other, 'state_data') and self.state_data == other.state_data

        if isinstance(other, StatePacman):
            return self.state_data_pacman == other.state_data_pacman
        return False

    def __hash__(self):
        """
        Allows states to be keys of dictionaries.
        """
        return hash(self.state_data_pacman)

    def __str__(self):
        return str(self.state_data_pacman)

    def get_deep_copy(self) -> StatePacman:

        # state_pacman_new = type(self)(self)
        state_pacman_new = StatePacman(self)

        state_pacman_new.state_data_pacman = self.state_data_pacman.get_deep_copy()

        return state_pacman_new

    def get_agent_by_index(self, index: int) -> Union[Agent, None]:
        return self.state_data_pacman.get_agent_by_index(index)

    def get_index_by_agent(self, agent: Agent) -> Union[int, None]:
        return self.state_data_pacman.get_index_by_agent(agent)

    #####

    def get_dict_k_player_v_container_state(self) -> Dict[PlayerPacman, ContainerState]:
        return self.state_data_pacman.get_dict_k_player_v_container_state()

    def get_dict_k_agent_v_player(self) -> Dict[Agent, PlayerPacman]:
        return self.state_data_pacman.get_dict_k_agent_v_player()

    def get_player_from_agent(self, agent: Agent) -> Union[PlayerPacman, None]:
        return self.state_data_pacman.get_player_from_agent(agent)

    ####################################################
    # Accessor methods: use these to access State data #
    ####################################################

    def getLegalActions(self, agent: Agent) -> List[Action]:
        """
        Returns the legal actions for the player_pacman specified.
        """
        #        State.set_state_explored.add(self)
        if self.isWin() or self.isLose():  # TODO: ADDED or agent is None BECAUSE  TEMPED
            return []

        # return PacmanRules.getLegalActions(self, agent)  # TODO: JOSEPH COMMENT JOSEPH JUMP
        # print("FFFFFF", agent)
        # for k, v in self.state_data.dict_k_agent_v_player.items():
        #     print(k, v)
        # TODO: ULTRA CHEAP SOLUTION TO GET AGENT TYPE (GHOST OR PLAYER)
        player_pacman: PlayerPacman = self.state_data_pacman.get_player_from_agent(agent)
        # print("---- getLegalActions agent", agent, player_pacman)

        # list_actions = RulesPacman.getLegalActions(self, player_pacman)

        # list_actions = player_pacman.get_agent().get_actions_legal(self)


        list_actions = StatePacman.dict_k_type_player_pacman_v_rules_pacman.get(
            player_pacman.get_type_player_pacman(),
            RulesPacman  # TODO: Can crash since Abstract method FIX ME
        ).getLegalActions(self, player_pacman)

        # if player_pacman.get_type_player_pacman() == EnumPlayerPacman.PACMAN:
        #     list_actions = RulesPacmanPacman.getLegalActions(self, player_pacman)
        # else:
        #     list_actions = RulesPacmanGhost.getLegalActions(self, player_pacman)

        return list_actions

    def generate_successor(self, agent: Agent, action: Action) -> StatePacman:
        """
        Returns the successor state after the specified player_pacman takes the action.
        """
        # Check that successors exist
        if self.isWin() or self.isLose():
            raise Exception('Can\'t generate a successor of a terminal state.')

        # Copy current state
        # state_pacman_new = type(self)(self)
        state_pacman_new = StatePacman(self)

        player_pacman: PlayerPacman = state_pacman_new.get_player_from_agent(agent)

        # # Let player_pacman's logic deal with its action's effects on the board
        # if player_pacman.get_type_player_pacman() == EnumPlayerPacman.PACMAN:
        #
        #     _dict_k_player_v_bool_eaten = state_pacman_new.state_data._dict_k_player_v_bool_eaten
        #
        #     # TODO: JOSEPH NOTE: THE CODE MAKES THE GHOST NOT SCARED I THINK, I DONT THINK THE CODE IS NEEDED
        #     # state_pacman_new.state_data._dict_k_player_v_bool_eaten = (
        #     #     {player: False for player in _dict_k_player_v_bool_eaten}
        #     # )
        #
        #     RulesPacmanPacman.applyAction(state_pacman_new, action, player_pacman)
        # else:  # A ghost is moving
        #     RulesPacmanGhost.applyAction(state_pacman_new, action, player_pacman)

        rules_pacman: RulesPacman = StatePacman.dict_k_type_player_pacman_v_rules_pacman.get(
            player_pacman.get_type_player_pacman(),
            RulesPacman  # TODO: Can crash since Abstract method FIX ME
        )

        rules_pacman.applyAction(state_pacman_new, action, player_pacman)

        # Time passes TODO: THE BELOW rules_pacman.update_state_pacman_and_player_pacman DOES THIS
        # if player_pacman.get_type_player_pacman() == EnumPlayerPacman.PACMAN:
        #     state_pacman_new.state_data.scoreChange += -TIME_PENALTY  # Penalty for waiting around
        # else:
        #
        #     container_state_ghost = state_pacman_new.state_data.dict_k_player_v_container_state.get(player_pacman)
        #
        #     RulesPacmanGhost._decrementTimer(container_state_ghost)

        # Update the new StatePacman and PlayerPacman
        rules_pacman.update_state_pacman_and_player_pacman(state_pacman_new, player_pacman)

        # Resolve multi-player_pacman effects
        rules_pacman.process_state_pacman_and_player_position(state_pacman_new, player_pacman)

        # Book keeping
        state_pacman_new.state_data_pacman.set_agent_moved(player_pacman.get_agent())
        state_pacman_new.state_data_pacman.score += state_pacman_new.state_data_pacman.scoreChange

        # type(self).set_state_explored.add(self)
        # type(self).set_state_explored.add(state_pacman_new)

        StatePacman.set_state_explored.add(self)
        StatePacman.set_state_explored.add(state_pacman_new)
        return state_pacman_new

    # TODO: DONT NEED NO MORE Use getLegalAction
    # def getLegalPacmanActions(self) -> List[Action]:
    #     return self.getLegalActions(0)

    # TODO: DONT USE, USE THIS -> self.generate_successor
    # def generatePacmanSuccessor(self, action: Action):
    #     """
    #     Generates the successor state after the specified pacman move
    #     """
    #     return self.generate_successor(self.state_data.pacamn, action)

    # TODO: DONT NEED NO MORE Use get_container_state_GHOST
    # def getPacmanState(self, agent: TYPE_REPRESENTATIVE):
    #     """
    #     Returns an ContainerState object for pacman (in game.py)
    #
    #     state._position gives the current _position
    #     state._direction gives the travel vector
    #     """
    #     return self.state_data.dict_k_player_v_container_state[0].copy()

    def getPacmanPosition(self, agent: Agent = None) -> Union[TYPE_VECTOR, None]:

        if agent is None:
            return self.get_position_of_agent(
                self.state_data_pacman._player_pacman.get_agent())  # TODO: ULTRA BYPASS REMOVE ME TO GET PACMAN POSITION

        return self.get_position_of_agent(agent)

    def get_list_container_state_ghost(self) -> List[ContainerState]:
        # return self.state_data.dict_k_player_v_container_state[1:]

        return [container_state_ghost for player, container_state_ghost in
                self.state_data_pacman.dict_k_player_v_container_state.items()
                if player.get_type_player_pacman() == EnumPlayerPacman.GHOST]

    # TODO: POSSIBLY RENAME
    def get_container_state_GHOST(self, agent: Agent) -> Union[ContainerState, None]:

        player = self.get_dict_k_agent_v_player().get(agent)

        return self.state_data_pacman.dict_k_player_v_container_state.get(player)

        # if agent == 0 or agent >= self.getNumAgents():
        #     raise Exception("Invalid index passed to getGhostState")
        # return self.state_data.dict_k_player_v_container_state[agent]   # TODO: LOOK IN state_data.dict_k_player_v_container_state BASED ON INDEX

    def get_position_of_agent(self, agent: Agent) -> Union[TYPE_VECTOR, None]:

        player = self.state_data_pacman.dict_k_agent_v_player.get(agent)

        container_state = self.state_data_pacman.dict_k_player_v_container_state.get(player)

        if container_state:
            return container_state.get_vector_position()

        return None

        # if agent == 0:
        #     raise Exception("Pacman's index passed to getGhostPosition")
        # return self.state_data.dict_k_player_v_container_state[agent].get_position()

    def get_list_position_ghost(self) -> List[TYPE_VECTOR]:
        return [s.get_vector_position() for s in self.get_list_container_state_ghost()]

    def getNumAgents(self):
        return len(self.state_data_pacman.dict_k_player_v_container_state)

    def getScore(self):
        return float(self.state_data_pacman.score)

    def getCapsules(self):
        """
        Returns a list of positions (x,y) of the remaining list_capsule.
        """
        return self.state_data_pacman.list_capsule

    def getNumFood(self):
        return self.state_data_pacman.grid_food.count()

    def getFood(self):
        """
        Returns a GridPacman of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = state.getFood()
        if currentFood[x][y] == True: ...
        """
        return self.state_data_pacman.grid_food

    def getWalls(self):
        """
        Returns a GridPacman of boolean wall indicator variables.

        Grids can be accessed via list notation, so to check
        if there is a wall at (x,y), just call

        walls = state.getWalls()
        if walls[x][y] == True: ...
        """
        return self.state_data_pacman.layout_pacman.walls

    def hasFood(self, x: int, y: int):
        return self.state_data_pacman.grid_food[x][y]

    def hasWall(self, x: int, y: int):
        return self.state_data_pacman.layout_pacman.walls[x][y]

    def isLose(self):
        return self.state_data_pacman._lose

    def isWin(self):
        return self.state_data_pacman._win
