"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/28/2022

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

from pacman.agent.agent import Agent
from pacman.agent.agent_ghost import AgentGhost
from pacman.agent.agent_ghost_directional import AgentGhostDirectional
from pacman.agent.agent_ghost_random import AgentGhostRandom
from pacman.agent.agent_keyboard import AgentKeyboard
from pacman.agent.agent_keyboard import AgentKeyboard2
from pacman.agent.agent_pacman import AgentPacman
from pacman.agent.agent_pacman_expectimax import AgentPacmanExpectimax
from pacman.agent.agent_pacman_greedy import AgentPacmanGreedy
from pacman.agent.agent_pacman_left_turn import AgentPacmanLeftTurn
from pacman.agent.agent_pacman_minimax import AgentPacmanMinimax
from pacman.agent.agent_pacman_minimax_alpha_beta import \
    AgentPacmanMinimaxAlphaBeta
from pacman.agent.agent_pacman_reflex import AgentPacmanReflex
from pacman.agent.agent_pacman_reflex import AgentPacmanReflex_Attempt_1
from pacman.agent.agent_pacman_search import AStarCornersAgent
from pacman.agent.agent_pacman_search import AStarFoodSearchAgent
from pacman.agent.agent_pacman_search import ClosestDotSearchAgent
from pacman.agent.agent_pacman_search import SearchAgent
from pacman.agent.agent_pacman_search import StayEastSearchAgent
from pacman.agent.agent_pacman_search import StayWestSearchAgent

LIST_AGENT = [
    Agent,
    AgentGhost,
    AgentGhostDirectional,
    AgentGhostRandom,
    AgentKeyboard,
    AgentKeyboard2,
    AgentPacman,
    AgentPacmanGreedy,
    AgentPacmanLeftTurn,
    AgentPacmanReflex,
    AgentPacmanReflex_Attempt_1,
    AgentPacmanMinimax,
    AgentPacmanMinimaxAlphaBeta,
    AgentPacmanExpectimax,
    AStarCornersAgent,
    AStarFoodSearchAgent,
    SearchAgent,
    StayEastSearchAgent,
    StayWestSearchAgent,
    ClosestDotSearchAgent,
]

DICT_K_NAME_V_AGENT = {
    agent_.__name__: agent_ for agent_ in LIST_AGENT
}


def get_class_agent(name_agent: Union[str, Type[Agent], None]) -> Type[Agent]:
    agent_ = name_agent

    if isinstance(name_agent, str):
        agent_ = DICT_K_NAME_V_AGENT.get(name_agent)

    if agent_ is None:
        Exception("{} is not an agent".format(name_agent))

    return agent_
