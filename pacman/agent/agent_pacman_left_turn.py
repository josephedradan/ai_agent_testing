"""
Date created: 12/27/2022

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
from pacman.game.action_direction import Action
from pacman.game.action_direction import ActionDirection

if TYPE_CHECKING:
    from common.state import State


class AgentPacmanLeftTurn(AgentPacman):
    """
    An player that turns left at every opportunity

    """

    def getAction(self, state: State) -> Action:
        legal = state.getLegalActions(self)

        current = state.get_container_state_GHOST(self)._container_position_direction._direction

        if current == ActionDirection.STOP:
            current = ActionDirection.NORTH

        left = ActionDirection.LEFT[current]

        if left in legal:
            return left
        if current in legal:
            return current
        if ActionDirection.RIGHT[current] in legal:
            return ActionDirection.RIGHT[current]
        if ActionDirection.LEFT[left] in legal:
            return ActionDirection.LEFT[left]
        return ActionDirection.STOP
