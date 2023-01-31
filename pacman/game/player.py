"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/30/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from pacman.agent import Agent


class Player:

    def __init__(self, agent: Agent):
        self.agent = agent


    def get_agent(self) -> Agent:
        return self.agent

