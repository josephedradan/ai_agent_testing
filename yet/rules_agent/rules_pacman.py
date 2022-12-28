"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/23/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from yet.agent.agent import Agent
from yet.constants import Direction
from yet.game_state import GameState
from yet.rules_agent.rules_agent import RulesAgent


class RulesPacman(RulesAgent):

    def do_action(self, game_state: GameState, action: Direction, agent: Agent):
        pass

    def get_actions_legal(self, game_state: GameState):
        pass