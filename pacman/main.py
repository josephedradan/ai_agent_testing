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
from __future__ import annotations

import argparse
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# print(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # FIXME: GHETTO SOLUTION TO MISSING MODULE
# pprint(sys.path_file_test)
from typing import Sequence
from typing import Union

from pacman.agent import Agent
from pacman.agent import AgentKeyboard
from pacman.agent import get_subclass_agent
from pacman.graphics import LIST_GRAPHICS_PACMAN
from pacman.graphics import get_class_graphics_pacman
from pacman.graphics import GraphicsPacmanNull

from pprint import pprint
from typing import List

from pacman.game.game import Game
from pacman.graphics.graphics_pacman import GraphicsPacman
from pacman.parser import get_dict_kwargs

from pacman.game import layout as _layout
from pacman.game.rules.game_rules_classic import ClassicGameRules
from pacman.graphics.graphics_pacman_display_tkiner import GraphicsPacmanDisplayTkinter


#############################
# FRAMEWORK TO START A GAME #
#############################


def default(str):
    return str + ' [Default: %default]'


def arg_parser_pacman(argv: Union[Sequence[str], None] = None):
    """
    Processes the command used to run pacman from the command line.
    """
    description = """
    USAGE:      python pacman.py <argparse_args>
    EXAMPLES:   (1) python pacman.py
                    - starts an interactive game
                (2) python pacman.py --layout smallClassic --zoom 2
                OR  python pacman.py -l smallClassic -z 2
                    - starts an interactive game on a smaller board, zoomed in
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-n', '--numGames',
                        dest='number_of_games',
                        type=int,
                        help='the number of GAMES to play',
                        metavar='GAMES',
                        default=1
                        )
    parser.add_argument('-l', '--layout',
                        dest='layout',
                        help='the LAYOUT_FILE from which to load the map layout',
                        metavar='LAYOUT_FILE',
                        default='mediumClassic'
                        )
    parser.add_argument('-p', '--pacman',
                        dest='str_class_agent_pacman',
                        help='the agent TYPE in the pacmanAgents module to use',
                        metavar='TYPE',
                        default='AgentKeyboard'
                        )

    # GRAPHICS

    parser.add_argument('--graphics',
                        dest='graphics_pacman',
                        choices=[graphics_pacman_.__name__ for graphics_pacman_ in LIST_GRAPHICS_PACMAN],
                        type=str,
                        default=GraphicsPacmanDisplayTkinter.__name__,
                        help="What graphics to display the game with (default: %(default)s)"
                        )
    # parser.add_argument('-t', '--textGraphics',
    #                     action='store_true',
    #                     dest='textGraphics',
    #                     help='GraphicsPacman output as text only',
    #                     # default=False
    #                     )
    parser.add_argument('-q', '--quietTextGraphics',
                        action='store_true',
                        dest='quietGraphics',
                        help='Generate minimal output and no graphics',
                        # default=False
                        )

    parser.add_argument('-g', '--ghost',
                        dest='str_class_agent_ghost',
                        help='the ghost agent TYPE in the list_agent_ghost module to use',
                        metavar='TYPE',
                        default='AgentGhostRandom'
                        )
    parser.add_argument('-k', '--numGhosts',
                        type=int,
                        dest='list_agent_ghost',
                        help='The maximum number of ghosts to use',
                        default=4
                        )
    parser.add_argument('-z', '--zoom',
                        type=float,
                        dest='zoom',
                        help='Zoom the size of the graphics window',
                        default=1.0
                        )
    parser.add_argument('-f', '--fixRandomSeed',
                        action='store_true',
                        dest='fixRandomSeed',
                        help='Fixes the random seed to always play the same game',
                        default=False
                        )
    parser.add_argument('-r', '--recordActions',
                        action='store_true',
                        dest='bool_record',
                        help='Writes game histories to a file (named by the time they were played)',
                        default=False
                        )
    parser.add_argument('--replay',
                        dest='path_game_to_replay',
                        help='A recorded game file (pickle) to replay',
                        default=None
                        )
    parser.add_argument('-a', '--agentArgs',
                        dest='agent_pacman_kwargs',
                        help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_argument('-x', '--numTraining',
                        dest='numTraining',
                        type=int,
                        help='How many episodes are training (suppresses output)',
                        default=0
                        )
    parser.add_argument('--frameTime',
                        dest='time_frame',
                        type=float,
                        help='Time to delay between frames; <0 means keyboard',
                        default=0.1
                        )
    parser.add_argument('-c', '--catchExceptions',
                        action='store_true',
                        dest='catchExceptions',
                        help='Turns on exception handling and timeouts during games',
                        default=False
                        )
    parser.add_argument('--timeout',
                        dest='timeout',
                        type=int,
                        help='Maximum length of time an agent can spend computing in a single game',
                        default=30
                        )

    argparse_args = parser.parse_args(argv)

    print("VARS")
    pprint(vars(argparse_args))
    print("=------=")

    # if len(otherjunk) != 0:
    #     raise Exception('Command line input not understood: ' + str(otherjunk))

    dict_k_name_arg_v_arg = {}

    # Fix the random seed
    if argparse_args.fixRandomSeed:
        random.seed('cs188')

    # Choose a layout
    dict_k_name_arg_v_arg['layout'] = _layout.get_layout(argparse_args.layout)

    if dict_k_name_arg_v_arg['layout'] == None:
        raise Exception("The layout " + argparse_args.layout + " cannot be found")

    # Choose a Pacman agent
    # noKeyboard = argparse_args.path_game_to_replay == None and (argparse_args.textGraphics or argparse_args.quietGraphics)

    class_agent_pacman = get_subclass_agent(argparse_args.str_class_agent_pacman)  # FIXME: PACMAN AGENT HERE

    # FIXME: argparse_args.pacman IS A AgentKeyboard
    # print("str_class_agent_pacman", argparse_args.str_class_agent_pacman, type(argparse_args.str_class_agent_pacman))

    agent_pacman_kwargs = get_dict_kwargs(argparse_args.agent_pacman_kwargs)

    if argparse_args.numTraining > 0:
        dict_k_name_arg_v_arg['numTraining'] = argparse_args.numTraining
        if 'numTraining' not in agent_pacman_kwargs:
            agent_pacman_kwargs['numTraining'] = argparse_args.numTraining

    agent_pacman_ = class_agent_pacman(**agent_pacman_kwargs)  # Instantiate Pacman with agent_pacman_kwargs
    dict_k_name_arg_v_arg['agent_pacman'] = agent_pacman_

    # Don't graphics_pacman training games  # FIXME: WTF IS THIS
    if 'numTrain' in agent_pacman_kwargs:
        argparse_args.numQuiet = int(agent_pacman_kwargs['numTrain'])
        argparse_args.numIgnore = int(agent_pacman_kwargs['numTrain'])

    # Choose a ghost agent
    class_agent_ghost = get_subclass_agent(argparse_args.str_class_agent_ghost)  # FIXME: GHOST AGENTS HERE
    print(argparse_args.str_class_agent_ghost,
          type(argparse_args.str_class_agent_ghost))  # FIXME: class_agent_ghost is AgentGhostRandom

    dict_k_name_arg_v_arg['list_agent_ghost'] = [class_agent_ghost(i + 1) for i in
                                                 range(argparse_args.list_agent_ghost)]

    class_graphics_pacman = get_class_graphics_pacman(argparse_args.graphics_pacman)

    if argparse_args.quietGraphics:
        dict_k_name_arg_v_arg['graphics_pacman'] = GraphicsPacmanNull(
            zoom=argparse_args.zoom,
            time_frame=argparse_args.time_frame
        )
    else:
        dict_k_name_arg_v_arg['graphics_pacman'] = class_graphics_pacman(
            zoom=argparse_args.zoom,
            time_frame=argparse_args.time_frame
        )

    # # Choose a graphics_pacman format
    # if argparse_args.quietGraphics:
    #     dict_k_name_arg_v_arg['graphics_pacman'] = GraphicsPacmanNull()
    # elif argparse_args.textGraphics:
    #     graphics_pacman_null.SLEEP_TIME = argparse_args.time_frame  # TODO: WTF THIS Y
    #     dict_k_name_arg_v_arg['graphics_pacman'] = GraphicsPacmanTerminal()
    # else:
    #     dict_k_name_arg_v_arg['graphics_pacman'] = GraphicsPacmanDisplayTkinter(
    #         zoom=argparse_args.zoom,
    #         time_frame=argparse_args.time_frame
    #     )

    # dict_k_name_arg_v_arg['graphics_pacman'] = textDisplay.GraphicsPacmanNull()
    # dict_k_name_arg_v_arg['graphics_pacman'] = GraphicsPacmanTerminal()

    dict_k_name_arg_v_arg['number_of_games'] = argparse_args.number_of_games
    dict_k_name_arg_v_arg['bool_record'] = argparse_args.bool_record
    dict_k_name_arg_v_arg['bool_catch_exceptions'] = argparse_args.catchExceptions
    dict_k_name_arg_v_arg['timeout'] = argparse_args.timeout

    # Special case: recorded games don't use the runGames method or dict_k_name_arg_v_arg structure
    if argparse_args.path_game_to_replay != None:
        print('Replaying recorded game %s.' % argparse_args.path_game_to_replay)
        import pickle
        f = open(argparse_args.path_game_to_replay)
        try:
            recorded = pickle.load(f)
        finally:
            f.close()
        recorded['graphics'] = dict_k_name_arg_v_arg['graphics_pacman']
        replay_game(**recorded)
        sys.exit(0)

    return dict_k_name_arg_v_arg


# def loadAgent(agent_: str, nographics: bool) -> Type[Agent]:  # RETURNS A CLASS
#
#     print(agent_, type(agent_))
#     print(nographics, type(nographics))
#
#     # FIXME: pacman IS AgentKeyboard <class 'string_given'> OR AgentGhostRandom <class 'string_given'>
#
#     return get_class_agent(agent_)
#
#     # if agent_ == "AgentKeyboard":
#     #     return AgentKeyboard
#     # elif agent_ == "AgentGhostRandom":
#     #     return AgentGhostRandom
#
#     # # Looks through all pythonPath Directories for the right module,
#     # pythonPathStr = os.path_file_test.expandvars("$PYTHONPATH")
#     # if pythonPathStr.find(';') == -1:
#     #     pythonPathDirs = pythonPathStr.split(':')
#     # else:
#     #     pythonPathDirs = pythonPathStr.split(';')
#     # pythonPathDirs.append('.')
#     #
#     # for moduleDir in pythonPathDirs:
#     #     if not os.path_file_test.isdir(moduleDir):
#     #         continue
#     #     moduleNames = [f for f in os.listdir(
#     #         moduleDir) if f.endswith('gents.py')]
#     #     for modulename in moduleNames:
#     #         try:
#     #             module = __import__(modulename[:-3])
#     #         except ImportError:
#     #             continue
#     #
#     #         if pacman in dir(module):
#     #             if nographics and modulename == 'keyboardAgents.py':
#     #                 raise Exception(
#     #                     'Using the keyboard requires graphics (not text graphics_pacman)')
#     #
#     #             print("FFFF", getattr(module, pacman))
#     #
#     #             # FIXME: <class 'keyboardAgents.AgentKeyboard'>  OR  <class 'list_agent_ghost.AgentGhostRandom'>
#     #             return getattr(module, pacman)
#     # raise Exception('The agent ' + pacman +
#     #                 ' is not specified in any *Agents.py.')


def replay_game(layout, actions, display):
    # import pacmanAgents
    # import list_agent_ghost

    rules = ClassicGameRules()
    agents = [pacmanAgents.AgentPacmanGreedy()] + [ghostAgents.AgentGhostRandom(i + 1)
                                                   for i in range(layout.getNumGhosts())]
    game = rules.create_and_get_game(layout, agents[0], agents[1:], display)
    state = game.game_state
    display.initialize(state.game_state_data)

    for action in actions:
        # Execute the action
        state = state.get_container_vector_successor(*action)
        # Change the graphics_pacman
        display.update(state.game_state_data)
        # Allow for game specific conditions (winning, losing, etc.)
        rules.process(state, game)

    display.finish()


def run_pacman_games(layout: _layout.Layout,
                     agent_pacman: Agent,  # FIXME: ADD MULTIPLE PLAYERS
                     list_agent_ghost: List[Agent],
                     graphics_pacman: GraphicsPacman,
                     number_of_games: int,
                     bool_record: bool,
                     numTraining: int = 0,
                     bool_catch_exceptions: bool = False,
                     timeout: int = 30,
                     **kwargs,
                     ) -> List[Game]:
    """
    Execute playing Pacman

    :param layout:
    :param agent_pacman:
    :param list_agent_ghost:
    :param graphics_pacman:
    :param number_of_games:
    :param bool_record:
    :param numTraining:
    :param bool_catch_exceptions:
    :param timeout:
    :return:
    """
    # FIXME: IDK WHY THIS HERE
    # import __main__
    # __main__.__dict__['_display'] = graphics_pacman
    print("#" * 100)
    __ALL = (
        layout, agent_pacman, list_agent_ghost, graphics_pacman, number_of_games, bool_record, numTraining,
        bool_catch_exceptions,
        timeout)

    # __DICT = {i: type(i) for i in __ALL}

    pprint(__ALL)
    print("#" * 100)

    classic_game_rules: ClassicGameRules = ClassicGameRules(timeout)
    list_game: List[Game] = []

    for i in range(number_of_games):
        bool_quiet = i < numTraining

        if bool_quiet:
            # Suppress output and graphics
            display_game = GraphicsPacmanNull()
            classic_game_rules.set_quiet(True)
        else:
            display_game = graphics_pacman
            classic_game_rules.set_quiet(False)

        #####
        # TODO JOSEPH SPEICAL
        # TODO: ALT GRAPHICS: GraphicsPacmanNull, GraphicsPacmanDisplayTkinter
        if isinstance(agent_pacman, AgentKeyboard) and isinstance(display_game, GraphicsPacmanDisplayTkinter):
            agent_pacman.set_display(display_game.get_display())

        ####

        game = classic_game_rules.create_and_get_game(
            layout,
            agent_pacman,
            list_agent_ghost,
            display_game,
            bool_quiet,
            bool_catch_exceptions
        )

        game.run()

        if not bool_quiet:
            list_game.append(game)

        if bool_record:
            import time
            import pickle
            filename_recorded = ('recorded-game-%d' % (i + 1)) + '-'.join([str(t) for t in time.localtime()[1:6]])

            # f = file(filename_recorded, 'w')
            with open(filename_recorded, 'w') as f:
                components = {'layout': layout, 'actions': game.moveHistory}
                pickle.dump(components, f)

    if (number_of_games - numTraining) > 0:
        scores = [game.game_state.getScore() for game in list_game]
        wins = [game.game_state.isWin() for game in list_game]
        winRate = wins.count(True) / float(len(wins))

        print('Average Score:', sum(scores) / float(len(scores)))
        print('Scores:       ', ', '.join([str(score) for score in scores]))
        print('Win Rate:      {}/{} ({:.2f})'.format(wins.count(True), len(wins), winRate))
        print('Record:       ', ', '.join([['Loss', 'Win'][int(w)] for w in wins]))

    return list_game


if __name__ == '__main__':
    """
    The main function called when pacman.py is run
    from the command line:

    > python pacman.py

    See the usage string for more details.

    > python pacman.py --help
    """
    # from code_analyzer import code_analyzer

    # code_analyzer.start()

    kwargs = arg_parser_pacman(sys.argv[1:])  # Get game components based on input

    # code_analyzer.stop()
    # code_analyzer.get_code_analyzer_printer().export_rich_to_html()

    pprint(kwargs)
    run_pacman_games(**kwargs)

    # import cProfile
    # cProfile.run("runGames( **args )")
    pass
