"""
Date created: 1/14/2023

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
from pacman.agent import AgentPacmanExpectimax
from pacman.agent import AgentPacmanMinimaxAlphaBeta
from pacman.agent.evaluation_function import evaluation_function_better


class ContestAgent(AgentPacmanMinimaxAlphaBeta):
    def __init__(self):
        super().__init__( evaluation_function=evaluation_function_better, depth=2)