# game.py
# -------
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

# game.py
# -------
# Licensing Information: Please do not distribute or publish solutions to this
# name_project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
# from util import *

from __future__ import annotations

import sys
import time
import traceback
from typing import List
from typing import TYPE_CHECKING

from pacman.agent.agent import Agent
from pacman.graphics.graphics import Graphics
from pacman.util import TimeoutFunction
from pacman.util import TimeoutFunctionException

if TYPE_CHECKING:
    from pacman.game.rules.game_rules_classic import ClassicGameRules

try:
    import boinc

    _BOINC_ENABLED = True
except:
    _BOINC_ENABLED = False


class Game:
    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self,
                 agents: List[Agent],
                 display: Graphics,  # FIXME: CAN BE NO GRAPHCIS OR ACUTAL GRAPHICS
                 rules: ClassicGameRules,
                 startingIndex: int = 0,
                 muteAgents: bool = False,
                 bool_catch_exceptions: bool = False):

        self.agentCrashed: bool = False
        self.agents: List[Agent] = agents
        self.display: Graphics = display
        self.rules: ClassicGameRules = rules
        self.startingIndex: int = startingIndex
        self.gameOver: bool = False
        self.muteAgents: bool = muteAgents
        self.catchExceptions = bool_catch_exceptions
        self.moveHistory: List = []
        self.totalAgentTimes : List[int] = [0 for agent in agents]
        self.totalAgentTimeWarnings: List[int] = [0 for agent in agents]
        self.agentTimeout: bool = False
        import io
        self.agentOutput = [io.StringIO() for agent in agents]

    def getProgress(self) -> float:
        if self.gameOver:
            return 1.0
        else:
            return self.rules.getProgress(self)

    def _agentCrash(self, agentIndex, quiet=False):
        "Helper method for handling agent crashes"
        if not quiet:
            traceback.print_exc()
        self.gameOver = True
        self.agentCrashed = True
        self.rules.agentCrash(self, agentIndex)

    OLD_STDOUT = None
    OLD_STDERR = None

    def mute(self, agentIndex):
        if not self.muteAgents:
            return
        global OLD_STDOUT, OLD_STDERR
        OLD_STDOUT = sys.stdout
        OLD_STDERR = sys.stderr
        sys.stdout = self.agentOutput[agentIndex]
        sys.stderr = self.agentOutput[agentIndex]

    def unmute(self):
        if not self.muteAgents:
            return
        global OLD_STDOUT, OLD_STDERR
        # Revert stdout/stderr to originals
        sys.stdout = OLD_STDOUT
        sys.stderr = OLD_STDERR

    def run(self):
        """
        Main control loop for game play.
        """
        self.display.initialize(self.state.data)
        self.numMoves = 0

        # self.display.initialize(self.game_state.makeObservation(1).data)
        # inform learning agents of the game start
        for i in range(len(self.agents)):
            agent = self.agents[i]
            if not agent:
                self.mute(i)
                # this is a null agent, meaning it failed to load
                # the other team wins
                print("Agent %d failed to load" % i, file=sys.stderr)
                self.unmute()
                self._agentCrash(i, quiet=True)
                return
            if ("registerInitialState" in dir(agent)):  # Basically hasattr without the raising exception
                print("registerInitialState IS HERE YO", dir(agent))
                self.mute(i)
                if self.catchExceptions:
                    try:
                        timed_func = TimeoutFunction(
                            agent.registerInitialState, int(self.rules.getMaxStartupTime(i)))
                        try:
                            start_time = time.time()
                            timed_func(self.state.deepCopy())
                            time_taken = time.time() - start_time
                            self.totalAgentTimes[i] += time_taken
                        except TimeoutFunctionException:
                            print("Agent %d ran out of time on startup!" %
                                  i, file=sys.stderr)
                            self.unmute()
                            self.agentTimeout = True
                            self._agentCrash(i, quiet=True)
                            return
                    except Exception as data:
                        self._agentCrash(i, quiet=False)
                        self.unmute()
                        return
                else:
                    agent.registerInitialState(self.state.deepCopy())
                # TODO: could this exceed the total time
                self.unmute()

        agentIndex = self.startingIndex
        numAgents = len(self.agents)

        while not self.gameOver:  # TODO: GAME LOOP IS RIGHT HERE
            # Fetch the next agent
            agent = self.agents[agentIndex]
            move_time = 0
            skip_action = False
            # Generate an observation of the game_state
            if 'observationFunction' in dir(agent):
                self.mute(agentIndex)
                if self.catchExceptions:
                    try:
                        timed_func = TimeoutFunction(agent.observationFunction, int(
                            self.rules.getMoveTimeout(agentIndex)))
                        try:
                            start_time = time.time()
                            observation = timed_func(self.state.deepCopy())
                        except TimeoutFunctionException:
                            skip_action = True
                        move_time += time.time() - start_time
                        self.unmute()
                    except Exception as data:
                        self._agentCrash(agentIndex, quiet=False)
                        self.unmute()
                        return
                else:
                    observation = agent.observationFunction(
                        self.state.deepCopy())
                self.unmute()
            else:
                observation = self.state.deepCopy()

            # Solicit an action
            action = None
            self.mute(agentIndex)
            if self.catchExceptions:  # TODO: THIS CODE IS NECESSARY JOSEPH, IT IS FOR THE autograder.py
                # raise Exception("ERROR CALLED IN GAME")
                try:
                    timed_func = TimeoutFunction(agent.getAction, int(
                        self.rules.getMoveTimeout(agentIndex)) - int(move_time))
                    try:
                        start_time = time.time()
                        if skip_action:
                            raise TimeoutFunctionException()
                        action = timed_func(observation)
                    except TimeoutFunctionException:
                        print("Agent %d timed out on a single move!" %
                              agentIndex, file=sys.stderr)
                        self.agentTimeout = True
                        self._agentCrash(agentIndex, quiet=True)
                        self.unmute()
                        return

                    move_time += time.time() - start_time

                    if move_time > self.rules.getMoveWarningTime(agentIndex):
                        self.totalAgentTimeWarnings[agentIndex] += 1
                        print("Agent %d took too long to make a move! This is warning %d" % (
                            agentIndex, self.totalAgentTimeWarnings[agentIndex]), file=sys.stderr)
                        if self.totalAgentTimeWarnings[agentIndex] > self.rules.getMaxTimeWarnings(agentIndex):
                            print("Agent %d exceeded the maximum number of warnings: %d" % (
                                agentIndex, self.totalAgentTimeWarnings[agentIndex]), file=sys.stderr)
                            self.agentTimeout = True
                            self._agentCrash(agentIndex, quiet=True)
                            self.unmute()
                            return

                    self.totalAgentTimes[agentIndex] += move_time
                    # print "Agent: %d, time: %f, total: %f" % (agentIndex, move_time, self.totalAgentTimes[agentIndex])
                    if self.totalAgentTimes[agentIndex] > self.rules.getMaxTotalTime(agentIndex):
                        print("Agent %d ran out of time! (time: %1.2f)" % (
                            agentIndex, self.totalAgentTimes[agentIndex]), file=sys.stderr)
                        self.agentTimeout = True
                        self._agentCrash(agentIndex, quiet=True)
                        self.unmute()
                        return
                    self.unmute()
                except Exception as data:
                    self._agentCrash(agentIndex)
                    self.unmute()
                    return
            else:

                action = agent.getAction(observation)
            self.unmute()

            # Execute the action
            self.moveHistory.append((agentIndex, action))
            if self.catchExceptions:
                try:
                    self.state = self.state.generateSuccessor(
                        agentIndex, action)
                except Exception as data:
                    self.mute(agentIndex)
                    self._agentCrash(agentIndex)
                    self.unmute()
                    return
            else:
                self.state = self.state.generateSuccessor(agentIndex, action)

            # Change the display
            self.display.update(self.state.data)
            ###idx = agentIndex - agentIndex % 2 + 1
            ###self.display.update( self.game_state.makeObservation(idx).data )

            # Allow for game specific conditions (winning, losing, etc.)
            self.rules.process(self.state, self)
            # Track progress
            if agentIndex == numAgents + 1:
                self.numMoves += 1
            # Next agent
            agentIndex = (agentIndex + 1) % numAgents

            if _BOINC_ENABLED:
                boinc.set_fraction_done(self.getProgress())

        # inform a learning agent of the game result
        for agentIndex, agent in enumerate(self.agents):
            if "final" in dir(agent):
                try:
                    self.mute(agentIndex)
                    agent.final(self.state)
                    self.unmute()
                except Exception as data:
                    if not self.catchExceptions:
                        raise
                    self._agentCrash(agentIndex)
                    self.unmute()
                    return
        self.display.finish()
