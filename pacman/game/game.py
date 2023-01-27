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
from typing import Union

from pacman.agent.agent import Agent
from pacman.game.game_state import GameState
from pacman.graphics.graphics_pacman import GraphicsPacman
from common.util import TimeoutFunction
from common.util import TimeoutFunctionException

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
                 list_agent: List[Agent],
                 graphics_pacman: GraphicsPacman,  # FIXME: CAN BE NO GRAPHCIS OR ACUTAL GRAPHICS
                 rules: ClassicGameRules,
                 index_starting: int = 0,
                 bool_mute_agents: bool = False,
                 bool_catch_exceptions: bool = False
                 ):

        self.agentCrashed: bool = False
        self.list_agent: List[Agent] = list_agent
        self.graphics_pacman: GraphicsPacman = graphics_pacman
        self.rules: ClassicGameRules = rules
        self.index_starting: int = index_starting
        self.gameOver: bool = False
        self.bool_mute_agents: bool = bool_mute_agents
        self.bool_catch_exceptions = bool_catch_exceptions
        self.moveHistory: List = []
        self.totalAgentTimes: List[int] = [0 for agent in list_agent]
        self.totalAgentTimeWarnings: List[int] = [0 for agent in list_agent]
        self.agentTimeout: bool = False

        import io
        self.agentOutput = [io.StringIO() for agent in list_agent]

        #####

        self.game_state: Union[GameState, None] = None


    def _get_progress(self) -> float:
        if self.gameOver:
            return 1.0
        else:
            return self.rules.getProgress(self)

    def _agentCrash(self, index_agent: int, quiet=False):
        "Helper method for handling agent crashes"
        if not quiet:
            traceback.print_exc()
        self.gameOver = True
        self.agentCrashed = True
        self.rules.agentCrash(self, index_agent)

    OLD_STDOUT = None
    OLD_STDERR = None

    def _mute(self, index_agent: int):
        # print(f"{self._mute.__name__}: self.bool_mute_agents {self.bool_mute_agents}")
        if not self.bool_mute_agents:
            return
        global OLD_STDOUT, OLD_STDERR
        OLD_STDOUT = sys.stdout
        OLD_STDERR = sys.stderr
        sys.stdout = self.agentOutput[index_agent]
        sys.stderr = self.agentOutput[index_agent]

        raise Exception("MUTE HAPPENED")

    def _unmute(self):
        # print(f"{self._unmute.__name__}: self.bool_mute_agents {self.bool_mute_agents}")

        if not self.bool_mute_agents:
            return
        global OLD_STDOUT, OLD_STDERR
        # Revert stdout/stderr to originals
        sys.stdout = OLD_STDOUT
        sys.stderr = OLD_STDERR

        raise Exception("UNMUTE HAPPENED")

    def run(self):
        """
        Main control loop for game play.
        """
        self.graphics_pacman.initialize(self.game_state.game_state_data)

        # print(self.state, type(self.state), "self.state", type(self.state.data))


        self.numMoves: int = 0

        self.game_state: GameState

        # self.graphics_pacman.initialize(self.game_state.makeObservation(1).data)
        # inform learning agents of the game start
        for i, agent in enumerate(self.list_agent):

            # TODO: JOSEPH - THIS SHOULD TECHNICALLY NEVER HIT
            # if not agent:
            #
            #     self._mute(i)
            #
            #     # this is a null agent, meaning it failed to load
            #     # the other team wins
            #     print("Agent %d failed to load" % i, file=sys.stderr)
            #     self._unmute()
            #     self._agentCrash(i, quiet=True)
            #     return

            if ("registerInitialState" in dir(agent)):  # Basically hasattr without the raising exception
                # print("registerInitialState IS HERE YO", dir(agent))
                self._mute(i)
                if self.bool_catch_exceptions:
                    try:
                        timed_func = TimeoutFunction(
                            agent.registerInitialState,
                            int(self.rules.getMaxStartupTime(i))
                        )
                        try:
                            time_start = time.time()
                            timed_func(self.game_state.get_deep_copy())
                            time_taken = time.time() - time_start
                            self.totalAgentTimes[i] += time_taken
                        except TimeoutFunctionException:
                            print("Agent %d ran out of time on startup!" %
                                  i, file=sys.stderr)
                            self._unmute()
                            self.agentTimeout = True
                            self._agentCrash(i, quiet=True)
                            return
                    except Exception as data:
                        self._agentCrash(i, quiet=False)
                        self._unmute()
                        return
                else:
                    agent.registerInitialState(self.game_state.get_deep_copy())

                # TODO: could this exceed the total time
                self._unmute()

        index_agent = self.index_starting
        number_of_agents:int  = len(self.list_agent)

        ##################################################
        # Main game Loop
        ##################################################
        while not self.gameOver:  # TODO: GAME LOOP IS RIGHT HERE
            # Fetch the next agent
            agent = self.list_agent[index_agent]
            move_time = 0
            skip_action = False

            ##################################################
            # Do operation related to Reinforcement learning
            ##################################################

            # Generate an observation of the game_state
            if 'observationFunction' in dir(agent):
                self._mute(index_agent)
                if self.bool_catch_exceptions:
                    try:
                        timed_func = TimeoutFunction(
                            agent.observationFunction,
                            int(self.rules.getMoveTimeout(index_agent))
                        )

                        time_start = time.time()
                        try:
                            observation = timed_func(self.game_state.get_deep_copy())
                        except TimeoutFunctionException:
                            skip_action = True

                        move_time += time.time() - time_start

                        self._unmute()
                    except Exception as data:
                        self._agentCrash(index_agent, quiet=False)
                        self._unmute()
                        return
                else:
                    observation = agent.observationFunction(self.game_state.get_deep_copy())
                self._unmute()

            ##################################################
            else:
                observation = self.game_state.get_deep_copy()

            ##################################################
            # Do operation related to autograder.py
            ##################################################

            # Solicit an action
            action = None
            self._mute(index_agent)

            if self.bool_catch_exceptions:  # TODO: THIS CODE IS NECESSARY JOSEPH, IT IS FOR THE autograder.py
                # raise Exception("ERROR CALLED IN GAME")
                try:
                    timed_func = TimeoutFunction(
                        agent.getAction,
                        int(self.rules.getMoveTimeout(index_agent)) - int(move_time)
                    )

                    try:
                        time_start = time.time()

                        if skip_action:  # TODO: DONT HAVE CONTROL OVER THIS JOSEPH
                            raise TimeoutFunctionException()

                        action = timed_func(observation)
                    except TimeoutFunctionException:
                        print("Agent {} timed out on a single move!".format(index_agent), file=sys.stderr)
                        self.agentTimeout = True
                        self._agentCrash(index_agent, quiet=True)
                        self._unmute()
                        return

                    move_time += time.time() - time_start

                    if move_time > self.rules.getMoveWarningTime(index_agent):
                        self.totalAgentTimeWarnings[index_agent] += 1
                        print("Agent %d took too long to make a move! This is warning %d" % (
                            index_agent, self.totalAgentTimeWarnings[index_agent]), file=sys.stderr)
                        if self.totalAgentTimeWarnings[index_agent] > self.rules.getMaxTimeWarnings(index_agent):
                            print("Agent %d exceeded the maximum number of warnings: %d" % (
                                index_agent, self.totalAgentTimeWarnings[index_agent]), file=sys.stderr)
                            self.agentTimeout = True
                            self._agentCrash(index_agent, quiet=True)
                            self._unmute()
                            return

                    self.totalAgentTimes[index_agent] += move_time
                    # print "Agent: %d, time: %f, total: %f" % (index_agent, move_time, self.totalAgentTimes[index_agent])
                    if self.totalAgentTimes[index_agent] > self.rules.getMaxTotalTime(index_agent):
                        print("Agent %d ran out of time! (time: %1.2f)" % (
                            index_agent, self.totalAgentTimes[index_agent]), file=sys.stderr)
                        self.agentTimeout = True
                        self._agentCrash(index_agent, quiet=True)
                        self._unmute()
                        return
                    self._unmute()
                except Exception as data:
                    self._agentCrash(index_agent)
                    self._unmute()
                    return
            else:
                action = agent.getAction(observation)  # # TODO: AGENT MOVES HERE

            ##################################################

            self._unmute()

            self.moveHistory.append((index_agent, action))

            # Execute the action
            if self.bool_catch_exceptions:
                try:
                    self.game_state = self.game_state.generateSuccessor(index_agent, action)
                except Exception as data:
                    # raise Exception("JOSEPH WTF")

                    self._mute(index_agent)
                    self._agentCrash(index_agent)
                    self._unmute()
                    return
            else:
                self.game_state = self.game_state.generateSuccessor(index_agent, action)

            # Change the graphics_pacman
            self.graphics_pacman.update(self.game_state.game_state_data)

            ###idx = index_agent - index_agent % 2 + 1
            ###self.graphics_pacman.update( self.game_state.makeObservation(idx).data )

            # Allow for game specific conditions (winning, losing, etc.)
            self.rules.process(self.game_state, self)  # TODO: CAN AFFECT gameOver

            # Track progress
            if index_agent == number_of_agents + 1:
                self.numMoves += 1

            # Next agent
            index_agent = (index_agent + 1) % number_of_agents

            if _BOINC_ENABLED:
                boinc.set_fraction_done(self._get_progress())

        #########################################################
        #########################################################

        # inform a learning agent of the game result
        for index_agent, agent in enumerate(self.list_agent):
            if "final" in dir(agent):
                try:
                    self._mute(index_agent)
                    agent.final(self.game_state)
                    self._unmute()
                except Exception as data:
                    if not self.bool_catch_exceptions:
                        raise
                    self._agentCrash(index_agent)
                    self._unmute()
                    return

        self.graphics_pacman.finish()
