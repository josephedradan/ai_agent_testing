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
# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from __future__ import annotations

from typing import TYPE_CHECKING

from pacman.agent.agent_pacman import AgentPacman
from pacman.game.directions import Action
from pacman.game.directions import Directions

if TYPE_CHECKING:
    from common.game_state import GameState


class AgentPacmanLeftTurn(AgentPacman):
    """
    An agent that turns left at every opportunity

    """

    def getAction(self, game_state: GameState) -> Action:
        legal = game_state.getLegalPacmanActions()

        current = game_state.getPacmanState().container_position_vector.direction

        if current == Directions.STOP:
            current = Directions.NORTH

        left = Directions.LEFT[current]

        if left in legal:
            return left
        if current in legal:
            return current
        if Directions.RIGHT[current] in legal:
            return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal:
            return Directions.LEFT[left]
        return Directions.STOP
