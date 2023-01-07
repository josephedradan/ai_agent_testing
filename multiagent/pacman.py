# pacman.py
# ---------
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


"""
Pacman.py holds the logic for the classic pacman game along with the main
code to run a game.  This file is divided into three sections:

  (i)  Your interface to the pacman world:
          Pacman is a complex environment.  You probably don't want to
          read through all of the code we wrote to make the game runs
          correctly.  This section contains the parts of the code
          that you will need to understand in order to complete the
          name_project.  There is also some code in game.py that you should
          understand.

  (ii)  The hidden secrets of pacman:
          This section contains all of the logic code that the pacman
          environment uses to decide who can move where, who dies when
          things collide, etc.  You shouldn't need to read this section
          of code, but you can if you want.

  (iii) Framework to start a game:
          The final section contains the code for reading the command
          you use to set up the game, then starting up a new game, along with
          linking in all the external parts (agent functions, graphics).
          Check this section out to see all the options available to you.

To play your first game, type 'python pacman.py' from the command line.
The keys are 'a', 's', 'd', and 'w' to move (or arrow keys).  Have fun!
"""
import argparse
import os
import random
import sys
from pprint import pprint
from typing import List

from multiagent.parser import get_dict_kwargs

print(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # FIXME: GHETTO SOLUTION TO MISSING MODULE
# pprint(sys.path_file_test)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from multiagent.agent import *
# from multiagent.agent.agent_ghost_random import AgentGhostRandom
# from multiagent.agent.agent_keyboard import AgentKeyboard
from multiagent.game import layout as _layout
from multiagent.game.rules.game_rules_classic import ClassicGameRules
from multiagent.graphics.graphicsDisplay import PacmanGraphicsReal


#############################
# FRAMEWORK TO START A GAME #
#############################


def default(str):
    return str + ' [Default: %default]'


def readCommand(argv):
    """
    Processes the command used to run pacman from the command line.
    """
    usageStr = """
    USAGE:      python pacman.py <options>
    EXAMPLES:   (1) python pacman.py
                    - starts an interactive game
                (2) python pacman.py --layout smallClassic --zoom 2
                OR  python pacman.py -l smallClassic -z 2
                    - starts an interactive game on a smaller board, zoomed in
    """
    parser = argparse.ArgumentParser(description=usageStr)

    parser.add_argument('-n', '--numGames',
                        dest='number_of_games',
                        type=int,
                        help=default('the number of GAMES to play'),
                        metavar='GAMES',
                        default=1)
    parser.add_argument('-l', '--layout',
                        dest='layout',
                        help=default(
                            'the LAYOUT_FILE from which to load the map layout'),
                        metavar='LAYOUT_FILE',
                        default='mediumClassic')
    parser.add_argument('-p', '--pacman',
                        dest='agent_pacman',
                        help=default(
                            'the agent TYPE in the pacmanAgents module to use'),
                        metavar='TYPE',
                        default='AgentKeyboard')
    parser.add_argument('-t', '--textGraphics',
                        action='store_true',
                        dest='textGraphics',
                        help='Display output as text only',
                        default=False)
    parser.add_argument('-q', '--quietTextGraphics',
                        action='store_true',
                        dest='quietGraphics',
                        help='Generate minimal output and no graphics',
                        default=False)
    parser.add_argument('-g', '--ghosts',
                        dest='ghost',
                        help=default(
                            'the ghost agent TYPE in the ghostAgents module to use'),
                        metavar='TYPE',
                        default='AgentGhostRandom')
    parser.add_argument('-k', '--numGhosts',
                        type=int,
                        dest='list_agent_ghost',
                        help=default('The maximum number of ghosts to use'), default=4)
    parser.add_argument('-z', '--zoom',
                        type=float,
                        dest='zoom',
                        help=default('Zoom the size of the graphics window'), default=1.0)
    parser.add_argument('-f', '--fixRandomSeed',
                        action='store_true',
                        dest='fixRandomSeed',
                        help='Fixes the random seed to always play the same game',
                        default=False)
    parser.add_argument('-r', '--recordActions',
                        action='store_true',
                        dest='record',
                        help='Writes game histories to a file (named by the time they were played)', default=False)
    parser.add_argument('--replay',
                        dest='gameToReplay',
                        help='A recorded game file (pickle) to replay',
                        default=None)
    parser.add_argument('-a', '--agentArgs',
                        dest='agentArgs',
                        help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_argument('-x', '--numTraining',
                        dest='numTraining',
                        type=int,
                        help=default('How many episodes are training (suppresses output)'),
                        default=0)
    parser.add_argument('--frameTime', dest='frameTime',
                        type=float,
                        help=default('Time to delay between frames; <0 means keyboard'),
                        default=0.1)
    parser.add_argument('-c', '--catchExceptions',
                        action='store_true',
                        dest='catchExceptions',
                        help='Turns on exception handling and timeouts during games',
                        default=False)
    parser.add_argument('--timeout',
                        dest='timeout',
                        type=int,
                        help=default('Maximum length of time an agent can spend computing in a single game'),
                        default=30)

    options = parser.parse_args(argv)

    # if len(otherjunk) != 0:
    #     raise Exception('Command line input not understood: ' + str(otherjunk))

    args = dict()

    # Fix the random seed
    if options.fixRandomSeed:
        random.seed('cs188')

    # Choose a layout
    args['layout'] = _layout.getLayout(options.layout)
    if args['layout'] == None:
        raise Exception("The layout " + options.layout + " cannot be found")

    # Choose a Pacman agent
    noKeyboard = options.gameToReplay == None and (
            options.textGraphics or options.quietGraphics)
    class_agent_pacman = loadAgent(options.agent_pacman, noKeyboard)  # FIXME: PACMAN AGENT HERE
    print("class_agent_pacman", options.agent_pacman, type(options.agent_pacman))  # FIXME: options.pacman IS A AgentKeyboard

    agentOpts = get_dict_kwargs(options.agentArgs)
    if options.numTraining > 0:
        args['numTraining'] = options.numTraining
        if 'numTraining' not in agentOpts:
            agentOpts['numTraining'] = options.numTraining
    pacman = class_agent_pacman(**agentOpts)  # Instantiate Pacman with agentArgs
    args['agent_pacman'] = pacman

    # Don't display training games
    if 'numTrain' in agentOpts:
        options.numQuiet = int(agentOpts['numTrain'])
        options.numIgnore = int(agentOpts['numTrain'])

    # Choose a ghost agent
    ghostType = loadAgent(options.ghost, noKeyboard)  # FIXME: GHOST AGENTS HERE
    print(options.ghost, type(options.ghost))  # FIXME: ghostType is AgentGhostRandom
    args['list_agent_ghost'] = [ghostType(i + 1) for i in range(options.list_agent_ghost)]

    # Choose a display format
    if options.quietGraphics:
        from multiagent.graphics import textDisplay
        args['display'] = textDisplay.NullGraphics()
    elif options.textGraphics:
        from multiagent.graphics import textDisplay
        textDisplay.SLEEP_TIME = options.frameTime
        args['display'] = textDisplay.PacmanGraphics()
    else:
        from multiagent.graphics import graphicsDisplay
        args['display'] = graphicsDisplay.PacmanGraphicsReal(
            options.zoom, frameTime=options.frameTime)
    args['number_of_games'] = options.number_of_games
    args['record'] = options.record
    args['bool_catch_exceptions'] = options.catchExceptions
    args['timeout'] = options.timeout

    # Special case: recorded games don't use the runGames method or args structure
    if options.gameToReplay != None:
        print('Replaying recorded game %s.' % options.gameToReplay)
        import pickle
        f = open(options.gameToReplay)
        try:
            recorded = pickle.load(f)
        finally:
            f.close()
        recorded['display'] = args['display']
        replayGame(**recorded)
        sys.exit(0)

    return args


def loadAgent(agent_: str, nographics: bool) -> Type[Agent]:  # RETURNS A CLASS

    print(agent_, type(agent_))
    print(nographics, type(nographics))

    # FIXME: pacman IS AgentKeyboard <class 'string_given'> OR AgentGhostRandom <class 'string_given'>

    return get_class_agent(agent_)

    # if agent_ == "AgentKeyboard":
    #     return AgentKeyboard
    # elif agent_ == "AgentGhostRandom":
    #     return AgentGhostRandom

    # # Looks through all pythonPath Directories for the right module,
    # pythonPathStr = os.path_file_test.expandvars("$PYTHONPATH")
    # if pythonPathStr.find(';') == -1:
    #     pythonPathDirs = pythonPathStr.split(':')
    # else:
    #     pythonPathDirs = pythonPathStr.split(';')
    # pythonPathDirs.append('.')
    #
    # for moduleDir in pythonPathDirs:
    #     if not os.path_file_test.isdir(moduleDir):
    #         continue
    #     moduleNames = [f for f in os.listdir(
    #         moduleDir) if f.endswith('gents.py')]
    #     for modulename in moduleNames:
    #         try:
    #             module = __import__(modulename[:-3])
    #         except ImportError:
    #             continue
    #
    #         if pacman in dir(module):
    #             if nographics and modulename == 'keyboardAgents.py':
    #                 raise Exception(
    #                     'Using the keyboard requires graphics (not text display)')
    #
    #             print("FFFF", getattr(module, pacman))
    #
    #             # FIXME: <class 'keyboardAgents.AgentKeyboard'>  OR  <class 'ghostAgents.AgentGhostRandom'>
    #             return getattr(module, pacman)
    # raise Exception('The agent ' + pacman +
    #                 ' is not specified in any *Agents.py.')


def replayGame(layout, actions, display):
    # import pacmanAgents
    # import ghostAgents

    rules = ClassicGameRules()
    agents = [pacmanAgents.AgentPacmanGreedy()] + [ghostAgents.AgentGhostRandom(i + 1)
                                                   for i in range(layout.getNumGhosts())]
    game = rules.newGame(layout, agents[0], agents[1:], display)
    state = game.state
    display.initialize(state.data)

    for action in actions:
        # Execute the action
        state = state.generateSuccessor(*action)
        # Change the display
        display.update(state.data)
        # Allow for game specific conditions (winning, losing, etc.)
        rules.process(state, game)

    display.finish()


def run_games(layout: _layout.Layout,
              agent_pacman: Agent,  # FIXME: ADD MULTIPLE PLAYERS
              list_agent_ghost: List[Agent],
              display: PacmanGraphicsReal,
              number_of_games: int,
              record: bool,
              numTraining: int = 0,
              bool_catch_exceptions: bool = False,
              timeout: int = 30
              ):
    """
    Execute playing Pacman

    :param layout:
    :param agent_pacman:
    :param list_agent_ghost:
    :param display:
    :param number_of_games:
    :param record:
    :param numTraining:
    :param bool_catch_exceptions:
    :param timeout:
    :return:
    """
    # FIXME: IDK WHY THIS HERE
    # import __main__
    # __main__.__dict__['_display'] = display
    print("#" * 100)
    __ALL = (
        layout, agent_pacman, list_agent_ghost, display, number_of_games, record, numTraining, bool_catch_exceptions,
        timeout)

    # __DICT = {i: type(i) for i in __ALL}

    pprint(__ALL)
    print("#" * 100)

    rules = ClassicGameRules(timeout)
    games = []

    for i in range(number_of_games):
        beQuiet = i < numTraining
        if beQuiet:
            # Suppress output and graphics
            from multiagent.graphics import textDisplay
            gameDisplay = textDisplay.NullGraphics()
            rules.quiet = True
        else:
            gameDisplay = display
            rules.quiet = False

        #####
        # TODO JOSEPH SPEICAL
        # TODO: ALT GRAPHICS: NullGraphics, PacmanGraphicsReal
        if isinstance(agent_pacman, AgentKeyboard) and isinstance(gameDisplay, PacmanGraphicsReal):
            agent_pacman.set_graphics_actual(gameDisplay.get_graphics_actual())

        ####

        game = rules.newGame(layout,
                             agent_pacman,
                             list_agent_ghost,
                             gameDisplay,
                             beQuiet,
                             bool_catch_exceptions)

        game.run()  # FIXME: GAME RUNS HERE
        if not beQuiet:
            games.append(game)

        if record:
            import time
            import pickle
            fname = ('recorded-game-%d' % (i + 1)) + \
                    '-'.join([str(t) for t in time.localtime()[1:6]])
            f = file(fname, 'w')
            components = {'layout': layout, 'actions': game.moveHistory}
            pickle.dump(components, f)
            f.close()

    if (number_of_games - numTraining) > 0:
        scores = [game.state.getScore() for game in games]
        wins = [game.state.isWin() for game in games]
        winRate = wins.count(True) / float(len(wins))
        print('Average Score:', sum(scores) / float(len(scores)))
        print('Scores:       ', ', '.join([str(score) for score in scores]))
        print('Win Rate:      %d/%d (%.2f)' %
              (wins.count(True), len(wins), winRate))
        print('Record:       ', ', '.join(
            [['Loss', 'Win'][int(w)] for w in wins]))

    return games


if __name__ == '__main__':
    """
    The main function called when pacman.py is run
    from the command line:

    > python pacman.py

    See the usage string for more details.

    > python pacman.py --help
    """
    args = readCommand(sys.argv[1:])  # Get game components based on input
    pprint(args)
    run_games(**args)

    # import cProfile
    # cProfile.run("runGames( **args )")
    pass
