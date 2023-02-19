"""
Date created: 1/19/2023

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
import random

from common.environment import Environment
from common.state import State
from pacman.agent import Agent


class EnvironmentGridworld(Environment):

    def __init__(self, gridWorld):
        self.gridWorld = gridWorld
        self.reset()

    def getCurrentState(self):
        return self.state

    def getPossibleActions(self, state: State, agent:Agent):
        return self.gridWorld.getPossibleActions(state)

    def doAction(self, action):
        state = self.getCurrentState()
        (nextState, reward) = self.getRandomNextState(state, action)
        self.state = nextState
        return (nextState, reward)

    def getRandomNextState(self, state, action, randObj=None):
        rand = -1.0
        if randObj is None:
            rand = random.random()
        else:
            rand = randObj.random()
        sum = 0.0
        successors = self.gridWorld.getTransitionStatesAndProbs(state, action)
        for nextState, prob in successors:
            sum += prob
            if sum > 1.0:
                raise Exception('Total transition probability more than one; sample failure.')
            if rand < sum:
                reward = self.gridWorld.getReward(state, action, nextState)
                return (nextState, reward)
        raise Exception('Total transition probability less than one; sample failure.')

    def reset(self):
        self.state = self.gridWorld.getStartState()
