# gridworld.py
# ------------
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
import argparse
import os
import random
import sys
import time
from typing import Sequence
from typing import Union

from common.display_tkinter import DisplayTkinter

print("OS PATH APPENDED", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "FROM",
      __file__)  # FIXME: GHETTO SOLUTION TO MISSING MODULE
from pprint import pprint
pprint(sys.path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from gridworld_rename.grid import get_callable_get_grid_world
from gridworld_rename.gridworld_environment import GridworldEnvironment
from gridworld_rename.main_grid_world import Gridworld
from pacman.agent import qlearningAgents
from pacman.agent import valueIterationAgents
from gridworld_rename.graphics_gridworld_display import GraphicsGridworldDisplay
from gridworld_rename.textGridworldDisplay import TextGridworldDisplay


from common import mdp


def getUserAction(state, actionFunction):
    """
    Get an action from the user (rather than the agent).

    Used for debugging and lecture demos.
    """

    action = None
    while True:
        keys = graphicsUtils.wait_for_keys()
        if 'Up' in keys: action = 'north'
        if 'Down' in keys: action = 'south'
        if 'Left' in keys: action = 'west'
        if 'Right' in keys: action = 'east'
        if 'q' in keys: sys.exit(0)
        if action == None: continue
        break
    actions = actionFunction(state)
    if action not in actions:
        action = actions[0]
    return action


def printString(x): print(x)

# TODO: Main loop
def runEpisode(agent, environment, discount, decision, display, message, pause, episode, display_):
    returns = 0
    totalDiscount = 1.0
    environment.reset()
    if 'startEpisode' in dir(agent): agent.startEpisode()
    message("BEGINNING EPISODE: " + str(episode) + "\n")
    while True:

        # DISPLAY CURRENT STATE
        state = environment.getCurrentState()
        display(state)  # TODO: HERERERSR
        pause()

        print("state", state)

        display_.drawsss()
        # display_.pause()


        # END IF IN A TERMINAL STATE
        actions = environment.getPossibleActions(state)
        if len(actions) == 0:
            message("EPISODE " + str(episode) + " COMPLETE: RETURN WAS " + str(returns) + "\n")
            return returns


        # GET ACTION (USUALLY FROM AGENT)
        action = decision(state)
        if action == None:
            raise 'Error: Agent returned None action'

        # EXECUTE ACTION
        nextState, reward = environment.doAction(action)
        message("Started in state: " + str(state) +
                "\nTook action: " + str(action) +
                "\nEnded in state: " + str(nextState) +
                "\nGot reward: " + str(reward) + "\n")
        # UPDATE LEARNER
        if 'observeTransition' in dir(agent):
            agent.observeTransition(state, action, nextState, reward)

        returns += reward * totalDiscount
        totalDiscount *= discount

    if 'stopEpisode' in dir(agent):
        agent.stopEpisode()


def arg_parser_gridworld(argv: Union[Sequence[str], None] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--discount',
                        action='store',
                        type=float,
                        dest='discount',
                        default=0.9,
                        help='Discount on future (default %default)'
                        )
    parser.add_argument('-r', '--livingReward',
                        action='store',
                        type=float,
                        dest='livingReward',
                        default=0.0,
                        metavar="R",
                        help='Reward for living for a time step (default %default)'
                        )
    parser.add_argument('-n', '--noise',
                        action='store',
                        type=float,
                        dest='noise',
                        default=0.2,
                        metavar="P",
                        help='How often action results in ' + 'unintended direction (default %default)'
                        )
    parser.add_argument('-e', '--epsilon',
                        action='store',
                        type=float,
                        dest='epsilon',
                        default=0.3,
                        metavar="E",
                        help='Chance of taking a random action in q-learning (default %default)'
                        )
    parser.add_argument('-l', '--learningRate',
                        action='store',
                        type=float,
                        dest='learningRate',
                        default=0.5,
                        metavar="P",
                        help='TD learning rate (default %default)'
                        )
    parser.add_argument('-i', '--iterations',
                        action='store',
                        type=int,
                        dest='iters',
                        default=10,
                        metavar="K",
                        help='Number of rounds of value iteration (default %default)'
                        )
    parser.add_argument('-k', '--episodes',
                        action='store',
                        type=int,
                        dest='episodes',
                        default=1,
                        metavar="K",
                        help='Number of epsiodes of the MDP to run (default %default)'
                        )
    parser.add_argument('-g', '--grid',
                        action='store',
                        metavar="G",
                        type=str,
                        dest='grid',
                        default="BookGrid",
                        help='GridPacman to use (case sensitive; options are BookGrid, BridgeGrid, CliffGrid, MazeGrid, default %default)'
                        )
    parser.add_argument('-w', '--windowSize',
                        metavar="X",
                        type=int,
                        dest='gridSize',
                        default=150,
                        help='Request a window width of X pixels *per grid cell* (default %default)'
                        )
    parser.add_argument('-a', '--agent',
                        action='store',
                        metavar="A",
                        type=str,
                        dest='agent',
                        default="random",
                        help='Agent type (options are \'random\', \'value\' and \'q\', default %default)'
                        )
    parser.add_argument('-t', '--text',
                        action='store_true',
                        dest='textDisplay',
                        default=False,
                        help='Use text-only ASCII display'
                        )
    parser.add_argument('-p', '--pause',
                        action='store_true',
                        dest='pause',
                        default=False,
                        help='Pause GUI after each time step when running the MDP'
                        )
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        dest='quiet',
                        default=False,
                        help='Skip display of any learning episodes'
                        )
    parser.add_argument('-s', '--speed',
                        action='store',
                        metavar="S",
                        type=float,
                        dest='speed',
                        default=1.0,
                        help='Speed of animation, S > 1.0 is faster, 0.0 < S < 1.0 is slower (default %default)'
                        )
    parser.add_argument('-m', '--manual',
                        action='store_true',
                        dest='manual',
                        default=False,
                        help='Manually control agent'
                        )
    parser.add_argument('-v', '--valueSteps',
                        action='store_true',
                        default=False,
                        help='Display each step of value iteration'
                        )

    argparse_args = parser.parse_args(argv)

    if argparse_args.manual and argparse_args.agent != 'q':
        print('## Disabling Agents in Manual Mode (-m) ##')
        argparse_args.agent = None

    # MANAGE CONFLICTS
    if argparse_args.textDisplay or argparse_args.quiet:
        # if argparse_args.quiet:
        argparse_args.pause = False
        # argparse_args.manual = False

    if argparse_args.manual:
        argparse_args.pause = True

    return argparse_args


if __name__ == '__main__':

    argparse_args = arg_parser_gridworld(
        # sys.argv  # DONT USE THIS UNLESS USING optparse
        sys.argv[1:]
    )
    print("argparse_args")
    print(argparse_args)
    print("#" * 100)

    ###########################
    # GET THE GRIDWORLD
    ###########################

    mdpFunction = get_callable_get_grid_world("get" + argparse_args.grid)
    print("mdpFunction", mdpFunction)
    mdp: Gridworld = mdpFunction()
    mdp.setLivingReward(argparse_args.livingReward)
    mdp.setNoise(argparse_args.noise)
    env = GridworldEnvironment(mdp)

    ###########################
    # GET THE DISPLAY ADAPTER
    ###########################

    display = TextGridworldDisplay(mdp)
    if not argparse_args.textDisplay:

        tkinter_display = DisplayTkinter()  # TODO: JOSEPH CUSTOM

        display: GraphicsGridworldDisplay= GraphicsGridworldDisplay(mdp, argparse_args.gridSize, argparse_args.speed,tkinter_display)


    try:
        display.start()
    except KeyboardInterrupt:
        sys.exit(0)

    ###########################
    # GET THE AGENT
    ###########################

    a = None
    if argparse_args.agent == 'value':
        a = valueIterationAgents.ValueIterationAgent(mdp, argparse_args.discount, argparse_args.iters)
    elif argparse_args.agent == 'q':
        # env.getPossibleActions, argparse_args.discount, argparse_args.learningRate, argparse_args.epsilon
        # simulationFn = lambda agent, state: simulation.GridworldSimulation(agent,state,mdp)
        gridWorldEnv = GridworldEnvironment(mdp)
        actionFn = lambda state: mdp.getPossibleActions(state)
        qLearnOpts = {'gamma': argparse_args.discount,
                      'alpha': argparse_args.learningRate,
                      'epsilon': argparse_args.epsilon,
                      'actionFn': actionFn}
        a = qlearningAgents.QLearningAgent(**qLearnOpts)
    elif argparse_args.agent == 'random':
        # # No reason to use the random agent without episodes
        if argparse_args.episodes == 0:
            argparse_args.episodes = 10


        class RandomAgent:
            def getAction(self, state):
                return random.choice(mdp.getPossibleActions(state))

            def getValue(self, state):
                return 0.0

            def getQValue(self, state, action):
                return 0.0

            def getPolicy(self, state):
                "NOTE: 'random' is a special policy value; don't use it in your code."
                return 'random'

            def update(self, state, action, nextState, reward):
                pass


        a = RandomAgent()
    elif argparse_args.agent == 'asynchvalue':
        a = valueIterationAgents.AsynchronousValueIterationAgent(mdp, argparse_args.discount, argparse_args.iters)
    elif argparse_args.agent == 'priosweepvalue':
        a = valueIterationAgents.PrioritizedSweepingValueIterationAgent(mdp, argparse_args.discount,
                                                                        argparse_args.iters)
    else:
        if not argparse_args.manual: raise Exception('Unknown agent type: ' + argparse_args.agent)

    ###########################
    # RUN EPISODES
    ###########################
    # DISPLAY Q/V VALUES BEFORE SIMULATION OF EPISODES
    try:
        if not argparse_args.manual and argparse_args.agent in ('value', 'asynchvalue', 'priosweepvalue'):
            if argparse_args.valueSteps:
                for i in range(argparse_args.iters):
                    tempAgent = valueIterationAgents.ValueIterationAgent(mdp, argparse_args.discount, i)
                    display.displayValues(tempAgent, message="VALUES AFTER " + str(i) + " ITERATIONS")
                    display.pause()

            display.displayValues(a, message="VALUES AFTER " + str(argparse_args.iters) + " ITERATIONS")
            display.pause()
            print("PAUSE DONE 1")
            display.displayValues(a, message="FFFFFFFFFFFF " + str(argparse_args.iters) + " ITERATIONS")
            display.pause()
            print("PAUSE DONE 2")

            display.displayQValues(a, message="Q-VALUES AFTER " + str(argparse_args.iters) + " ITERATIONS")
            display.pause()
            print("PAUSE DONE 3")

    except KeyboardInterrupt:
        sys.exit(0)

    # FIGURE OUT WHAT TO DISPLAY EACH TIME STEP (IF ANYTHING)
    displayCallback = lambda x: None
    if not argparse_args.quiet:
        if argparse_args.manual and argparse_args.agent == None:
            displayCallback = lambda state: display.displayNullValues(state)
        else:
            if argparse_args.agent in ('random', 'value', 'asynchvalue', 'priosweepvalue'):
                displayCallback = lambda state: display.displayValues(a, state, "CURRENT VALUES")  # TODO: THE CALLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
            if argparse_args.agent == 'q': displayCallback = lambda state: display.displayQValues(a, state,
                                                                                                  "CURRENT Q-VALUES")

    messageCallback = lambda x: printString(x)
    if argparse_args.quiet:
        messageCallback = lambda x: None

    # FIGURE OUT WHETHER TO WAIT FOR A KEY PRESS AFTER EACH TIME STEP
    pauseCallback = lambda: None
    if argparse_args.pause:
        pauseCallback = lambda: display.pause()

    # FIGURE OUT WHETHER THE USER WANTS MANUAL CONTROL (FOR DEBUGGING AND DEMOS)
    if argparse_args.manual:
        decisionCallback = lambda state: getUserAction(state, mdp.getPossibleActions)
    else:
        decisionCallback = a.getAction

    # RUN EPISODES
    if argparse_args.episodes > 0:
        print()
        print("RUNNING", argparse_args.episodes, "EPISODES")
        print()
    returns = 0
    for episode in range(1, argparse_args.episodes + 1):
        returns += runEpisode(a, env, argparse_args.discount, decisionCallback, displayCallback, messageCallback,
                              pauseCallback,
                              episode,
                              display
                              )
    if argparse_args.episodes > 0:
        print()
        print("AVERAGE RETURNS FROM START STATE: " + str((returns + 0.0) / argparse_args.episodes))
        print()
        print()

    # DISPLAY POST-LEARNING VALUES / Q-VALUES
    if argparse_args.agent == 'q' and not argparse_args.manual:
        try:
            display.displayQValues(a, message="Q-VALUES AFTER " + str(argparse_args.episodes) + " EPISODES")
            display.pause()
            display.displayValues(a, message="VALUES AFTER " + str(argparse_args.episodes) + " EPISODES")
            display.pause()
        except KeyboardInterrupt:
            sys.exit(0)
