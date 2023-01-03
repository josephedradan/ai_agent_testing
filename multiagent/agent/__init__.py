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
from multiagent.agent.agent import Agent
from multiagent.agent.agent_ghost import AgentGhost
from multiagent.agent.agent_ghost_directional import AgentGhostDirectional
from multiagent.agent.agent_ghost_random import AgentGhostRandom
from multiagent.agent.agent_keyboard import AgentKeyboard
from multiagent.agent.agent_keyboard import AgentKeyboard2
from multiagent.agent.agent_pacman import AgentPacman
from multiagent.agent.agent_pacman_expectimax import AgentPacmanExpectimax
from multiagent.agent.agent_pacman_greedy import AgentPacmanGreedy
from multiagent.agent.agent_pacman_left_turn import AgentPacmanLeftTurn
from multiagent.agent.agent_pacman_minimax import AgentPacmanMinimax
from multiagent.agent.agent_pacman_minimax_alpha_beta import \
    AgentPacmanMinimaxAlphaBeta
from multiagent.agent.agent_pacman_reflex import AgentPacmanReflex
from multiagent.agent.agent_pacman_reflex import AgentPacmanReflex_Attempt_1
from multiagent.agent.agent_pacman_search import AStarCornersAgent
from multiagent.agent.agent_pacman_search import AStarFoodSearchAgent
from multiagent.agent.agent_pacman_search import AnyFoodSearchProblem
from multiagent.agent.agent_pacman_search import ClosestDotSearchAgent
from multiagent.agent.agent_pacman_search import SearchAgent
from multiagent.agent.agent_pacman_search import StayEastSearchAgent
from multiagent.agent.agent_pacman_search import StayWestSearchAgent

DICT_K_NAME_V_AGENT = {
    Agent.__name__: Agent,
    AgentGhost.__name__: AgentGhost,
    AgentGhostDirectional.__name__: AgentGhostDirectional,
    AgentGhostRandom.__name__: AgentGhostRandom,
    AgentKeyboard.__name__: AgentKeyboard,
    AgentKeyboard2.__name__: AgentKeyboard2,
    AgentPacman.__name__: AgentPacman,
    AgentPacmanGreedy.__name__: AgentPacmanGreedy,
    AgentPacmanLeftTurn.__name__: AgentPacmanLeftTurn,
    AgentPacmanReflex.__name__: AgentPacmanReflex,
    AgentPacmanReflex_Attempt_1.__name__: AgentPacmanReflex_Attempt_1,
    AgentPacmanMinimax.__name__: AgentPacmanMinimax,
    AgentPacmanMinimaxAlphaBeta.__name__: AgentPacmanMinimaxAlphaBeta,
    AgentPacmanExpectimax.__name__: AgentPacmanExpectimax,
    AStarCornersAgent.__name__: AStarCornersAgent,
    AStarFoodSearchAgent.__name__: AStarFoodSearchAgent,
    SearchAgent.__name__: SearchAgent,
    StayEastSearchAgent.__name__: StayEastSearchAgent,
    StayWestSearchAgent.__name__: StayWestSearchAgent,
    ClosestDotSearchAgent.__name__: ClosestDotSearchAgent

}
