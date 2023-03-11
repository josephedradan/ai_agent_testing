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
          linking in all the external parts (player functions, graphics).
          Check this section out to see all the options available to you.

To play your first game, type 'python pacman.py' from the command line.
The keys are 'a', 's', 'd', and 'w' to move (or arrow keys).  Have fun!
"""
from __future__ import annotations

import argparse
import os
import random
import sys
from typing import Any
from typing import Dict

from common.common import get_list_agent_from_list_container_object_construct
from pacman.agent import Agent
from pacman.parser import ContainerObjectConstruct
from pacman.parser import get_list_container_object_construct_from_implicit
from pacman.parser import get_list_container_object_construct_from_str

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pacman.agent import DICT_K_NAME_SUBCLASS_AGENT_V_SUBCLASS_AGENT

# print(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # FIXME: GHETTO SOLUTION TO MISSING MODULE
# pprint(sys.path_file_test)
from typing import Sequence
from typing import Union

from pacman.graphics import LIST_GRAPHICS_PACMAN
from pacman.graphics import get_class_graphics_pacman
from pacman.graphics import GraphicsPacmanNull

from pprint import pprint
from typing import List

from pacman.game.game import Game

from pacman.game.rules.game_rules_classic import ClassicGameRules
from pacman.graphics.graphics_pacman_gui import GraphicsPacmanGUI
from pacman.graphics.graphics_pacman import GraphicsPacman


#############################
# FRAMEWORK TO START A GAME #
#############################


def default(str):
    return str + ' [Default: %default]'


def get_argparse_namespace_for_pacman(argv: Union[Sequence[str], None] = None) -> argparse.Namespace:
    """
    Processes the command used to run pacman from the command line.
    """
    description = """
    USAGE:      python pacman.py <namespace>
    EXAMPLES:   (1) python pacman.py
                    - starts an interactive game
                (2) python pacman.py --str_path_layout smallClassic --zoom 2
                OR  python pacman.py -l smallClassic -z 2
                    - starts an interactive game on a smaller board, zoomed in
    """
    parser = argparse.ArgumentParser(description=description)

    group_pacman_selection = parser.add_mutually_exclusive_group()
    group_pacman_selection_explicit = group_pacman_selection.add_argument_group()
    group_pacman_selection_implicit = group_pacman_selection.add_argument_group()

    group_ghost_selection = parser.add_mutually_exclusive_group()
    group_ghost_selection_explicit = group_ghost_selection.add_argument_group()
    group_ghost_selection_implicit = group_ghost_selection.add_argument_group()

    parser.add_argument('-n', '--numGames',
                        dest='number_of_games',
                        type=int,
                        help='the number of GAMES to play',
                        metavar='GAMES',
                        default=1
                        )
    parser.add_argument('-l', '--layout_pacman',
                        dest='str_path_layout',
                        help='the LAYOUT_FILE from which to load the map str_path_layout',
                        metavar='LAYOUT_FILE',
                        default='mediumClassic'
                        )

    # ----- Pacman stuff -----

    # Explicit Pacman creation

    group_pacman_selection_explicit.add_argument('-aps', '--AgentPacmans',
                                                 dest='str_list_agent_pacman',
                                                 help='the player TYPE in the pacmanAgents module to use',
                                                 type=str,
                                                 default=None,
                                                 )

    # group_pacman_selection_explicit.add_argument('-apsa', '--AgentPacmansArgs',
    #                                              dest='str_list_agent_pacman_kwargs',
    #                                              help='Comma separated values sent to player. e.g. "opt1=val1,opt2,opt3=val3"')

    # Implicit Pacman creation is the default behavior

    group_pacman_selection_implicit.add_argument('-ap', '--AgentPacman',  # TODO: RENAME -ap to -ap
                                                 dest='str_agent_pacman',
                                                 help='the player TYPE in the pacmanAgents module to use',
                                                 choices=DICT_K_NAME_SUBCLASS_AGENT_V_SUBCLASS_AGENT.keys(),
                                                 type=str,
                                                 default='AgentKeyboard',
                                                 )
    group_pacman_selection_implicit.add_argument('-apa', '--AgentPacmanArgs',  # TODO: RENAME -a to -apa
                                                 dest='str_agent_pacman_kwargs',
                                                 help='Comma separated values sent to player. e.g. "opt1=val1,opt2,opt3=val3"',
                                                 type=str,
                                                 default="",
                                                 )

    group_pacman_selection_implicit.add_argument('-apn', '--AgentPacmanNum',  # TODO: RENAME -np to -apn
                                                 dest='num_of_agent_pacman',
                                                 help='The maximum number of pacman to use',
                                                 type=int,
                                                 default=1,
                                                 )

    # ----- Ghost stuff -----

    # Explicit Ghost creation

    group_ghost_selection_explicit.add_argument('-ags', '--AgentGhosts',
                                                dest='str_list_agent_ghost',
                                                help='Explicit ghost agents e.g "Agent("bob", stuff=123)" sd',
                                                type=str,
                                                default=None,
                                                )

    # group_ghost_selection_explicit.add_argument('-agsa', '--AgentGhostsArgs',
    #                                             dest='str_list_agent_ghost_kwargs',
    #                                             help='Comma separated values sent to player. e.g. "opt1=val1,opt2,opt3=val3"')

    # Implicit Ghost creation is default

    group_ghost_selection_implicit.add_argument('-ag', '--AgentPacmanGhost',  # TODO: RENAME -g to -ag
                                                dest='str_agent_ghost',
                                                help='the ghost player TYPE in the ghosts module to use',
                                                choices=DICT_K_NAME_SUBCLASS_AGENT_V_SUBCLASS_AGENT.keys(),
                                                type=str,
                                                default='AgentPacmanGhostRandom'
                                                )
    group_ghost_selection_implicit.add_argument('-aga', '--AgentGhostArgs',
                                                dest='str_agent_ghost_kwargs',
                                                help='Comma separated values sent to player. e.g. "opt1=val1,opt2,opt3=val3"',
                                                type=str,
                                                default="",
                                                )

    group_ghost_selection_implicit.add_argument('-agn', '--AgentGhostNum',
                                                dest='num_of_agent_ghost',
                                                help='The maximum number of ghosts to use',
                                                type=int,
                                                default=4
                                                )
    # GRAPHICS
    parser.add_argument('--graphics',
                        dest='graphics_pacman',
                        choices=[graphics_pacman_.__name__ for graphics_pacman_ in LIST_GRAPHICS_PACMAN],
                        help="What graphics to display the game with (default: %(default)s)",
                        type=str,
                        default=GraphicsPacmanGUI.__name__,
                        )
    parser.add_argument('-q', '--quietTextGraphics',
                        action='store_true',
                        dest='quietGraphics',
                        help='Generate minimal output and no graphics',
                        # default=False
                        )
    # parser.add_argument('-t', '--textGraphics',
    #                     action='store_true',
    #                     dest='textGraphics',
    #                     help='Graphics output as text only',
    #                     # default=False
    #                     )
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
    parser.add_argument('-x', '--numTraining',
                        dest='num_training',
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
                        help='Maximum length of time an player can spend computing in a single game',
                        default=30
                        )

    print("----- MAIN.py argv START -----")
    print(argv)
    print("-----MAIN.py argv END -----")

    namespace_ = parser.parse_args(argv)

    return namespace_


def get_dict_namespace(namespace: argparse.Namespace) -> Dict[str, Any]:
    print("----- get_dict_namespace VARS START -----")
    pprint(vars(namespace))
    print("----- get_dict_namespace VARS END -----")

    dict_k_name_arg_v_arg = {}

    # Fix the random seed
    if namespace.fixRandomSeed:
        random.seed('cs188')

    # Choose a str_path_layout
    dict_k_name_arg_v_arg['str_path_layout'] = namespace.str_path_layout

    if dict_k_name_arg_v_arg['str_path_layout'] == None:
        raise Exception("The str_path_layout " + namespace.layout + " cannot be found")

    # Choose a Pacman player
    # noKeyboard = namespace.path_game_to_replay == None and (namespace.textGraphics or namespace.quietGraphics)

    ##########
    """
    Pacman creation stuff
    """

    _list_container_object_construct_pacman: List[ContainerObjectConstruct]

    if namespace.str_list_agent_pacman is not None:
        _list_container_object_construct_pacman = get_list_container_object_construct_from_str(
            namespace.str_list_agent_pacman)

    else:  # Implicit is default

        _list_container_object_construct_pacman = get_list_container_object_construct_from_implicit(
            namespace.str_agent_pacman,
            namespace.str_agent_pacman_kwargs,
            namespace.num_of_agent_pacman
        )



    if namespace.num_training > 0:
        dict_k_name_arg_v_arg['num_training'] = namespace.num_training

        # Loop over container_object_construct_pacman and add the kwarg num_training is possible
        for container_object_construct_pacman in _list_container_object_construct_pacman:

            _dict_kwargs = container_object_construct_pacman.keyword_arguments

            if 'num_training' not in _dict_kwargs:
                _dict_kwargs['num_training'] = namespace.num_training

    _list_agent_pacman: List[Agent] = get_list_agent_from_list_container_object_construct(
        _list_container_object_construct_pacman)

    dict_k_name_arg_v_arg['list_agent_pacman'] = _list_agent_pacman

    #####

    # class_agent_pacman = get_subclass_agent(namespace.str_pacman_ghost_agent)  # FIXME: PACMAN AGENT HERE

    # FIXME: namespace.pacman IS A AgentKeyboard
    # print("str_pacman_ghost_agent", namespace.str_pacman_ghost_agent, type(namespace.str_pacman_ghost_agent))

    # _list_dict_pacman_pacman_agent_kwargs = get_dict_kwargs_from_string(namespace.str_agent_pacman_kwargs)

    # pacman = class_agent_pacman(
    #     **_str_agent_pacman_kwargs)  # Instantiate Pacman with _str_agent_pacman_kwargs

    # dict_k_name_arg_v_arg['list_tuple__str_agent_ghost__dict_kwargs'] = pacman

    # # Don't graphics training games  # FIXME: WTF IS THIS
    # if 'numTrain' in _list_dict_pacman_pacman_agent_kwargs:
    #     namespace.numQuiet = int(_list_dict_pacman_pacman_agent_kwargs['numTrain'])
    #     namespace.numIgnore = int(_list_dict_pacman_pacman_agent_kwargs['numTrain'])

    ##########

    """
    Ghost creation stuff
    """

    # if namespace.str_list_agent_ghost:
    #
    #     str_list_agent_ghost = str(namespace.str_list_agent_ghost)
    #     dict_k_name_arg_v_arg['list_str_pacman_ghost_agent'] = (
    #         [str_list_agent_ghost.strip().split(",")]
    #     )
    #     print("FFFFFFFFFFFFFFFFFU")
    #     print(dict_k_name_arg_v_arg['list_str_pacman_ghost_agent'])
    #
    # else:
    #     # Choose a ghost player
    #     str_pacman_ghost_agent = namespace.str_pacman_ghost_agent  # FIXME: GHOST AGENTS HERE
    #
    #     # print(namespace.str_pacman_ghost_agent,
    #     #       type(namespace.str_pacman_ghost_agent))  # FIXME: str_pacman_ghost_agent is AgentPacmanGhostRandom
    #
    #     dict_k_name_arg_v_arg['list_str_pacman_ghost_agent'] = (
    #         [str_pacman_ghost_agent for _ in range(namespace.num_of_agent_ghost)]
    #     )

    _list_container_object_construct_ghost: List[ContainerObjectConstruct]

    if namespace.str_list_agent_ghost is not None:

        _list_container_object_construct_ghost = get_list_container_object_construct_from_str(
            namespace.str_list_agent_ghost)

    else:  # Implicit is default

        _list_container_object_construct_ghost = get_list_container_object_construct_from_implicit(
            namespace.str_agent_ghost,
            namespace.str_agent_ghost_kwargs,
            namespace.num_of_agent_ghost
        )

    # TODO: THIS IS COPY FROM THE PACMAN VERSION ABOVE, NEED BETTER DESIGN
    if namespace.num_training > 0:
        # dict_k_name_arg_v_arg['num_training'] = namespace.num_training  # TODO: Already added from the pacman above

        for container_object_construct_ghost in _list_container_object_construct_ghost:

            _dict_kwargs = container_object_construct_ghost.keyword_arguments

            if 'num_training' not in _dict_kwargs:
                _dict_kwargs['num_training'] = namespace.num_training

    _list_agent_ghost: List[Agent] = get_list_agent_from_list_container_object_construct(
        _list_container_object_construct_ghost
    )

    dict_k_name_arg_v_arg['list_agent_ghost'] = _list_agent_ghost

    ##########

    class_graphics_pacman = get_class_graphics_pacman(namespace.graphics_pacman)

    if namespace.quietGraphics:
        dict_k_name_arg_v_arg['graphics_pacman'] = GraphicsPacmanNull(
            zoom=namespace.zoom,
            time_frame=namespace.time_frame
        )
    else:
        dict_k_name_arg_v_arg['graphics_pacman'] = class_graphics_pacman(
            zoom=namespace.zoom,
            time_frame=namespace.time_frame
        )

    # # Choose a graphics format
    # if namespace.quietGraphics:
    #     dict_k_name_arg_v_arg['graphics'] = GraphicsPacmanNull()
    # elif namespace.textGraphics:
    #     graphics_pacman_null.SLEEP_TIME = namespace.time_frame  # TODO: WTF THIS Y
    #     dict_k_name_arg_v_arg['graphics'] = GraphicsPacmanTerminal()
    # else:
    #     dict_k_name_arg_v_arg['graphics'] = GraphicsPacmanDisplay(
    #         zoom=namespace.zoom,
    #         time_frame=namespace.time_frame
    #     )

    # dict_k_name_arg_v_arg['graphics'] = textDisplay.GraphicsPacmanNull()
    # dict_k_name_arg_v_arg['graphics'] = GraphicsPacmanTerminal()

    dict_k_name_arg_v_arg['number_of_games'] = namespace.number_of_games
    dict_k_name_arg_v_arg['bool_record'] = namespace.bool_record
    dict_k_name_arg_v_arg['bool_catch_exceptions'] = namespace.catchExceptions
    dict_k_name_arg_v_arg['timeout'] = namespace.timeout

    # Special case: recorded games don't use the runGames method or dict_k_name_arg_v_arg structure
    if namespace.path_game_to_replay != None:
        print('Replaying recorded game %s.' % namespace.path_game_to_replay)
        import pickle
        f = open(namespace.path_game_to_replay)
        try:
            recorded = pickle.load(f)
        finally:
            f.close()
        recorded['graphics'] = dict_k_name_arg_v_arg['graphics']
        replay_game(**recorded)
        sys.exit(0)

    return dict_k_name_arg_v_arg


def replay_game(layout, actions, display):  # FIXME: FIGURE THSI OUT LATER
    # import pacmanAgents
    # import list_str_pacman_ghost_agent

    rules = ClassicGameRules()
    agents = [pacmanAgents.AgentPacmanGreedy()] + [ghostAgents.AgentPacmanGhostRandom(i + 1)
                                                   for i in range(layout.getNumGhosts())]
    game = rules.create_and_get_game(layout, agents[0], agents[1:], display)
    state = game.state_pacman
    display.initialize(state.state_data)

    for action in actions:
        # Execute the action
        state = state.get_container_position_direction_successor(*action)
        # Change the graphics
        display.update(state.state_data)
        # Allow for game specific conditions (winning, losing, etc.)
        rules.process(state, game)

    display.finish()


"""
def run_pacman_games(str_path_layout: _layout.LayoutPacman,
                     list_tuple__str_agent_ghost__dict_kwargs: Agent,  # FIXME: ADD MULTIPLE PLAYERS
                     list_str_pacman_ghost_agent: List[str],
                     graphics: Graphics,
                     number_of_games: int,
                     bool_record: bool,
                     num_training: int = 0,
                     bool_catch_exceptions: bool = False,
                     timeout: int = 30,
                     **kwargs,
                     ) -> List[Game]:

"""


def run_pacman_games(str_path_layout: str,
                     list_agent_pacman: List[Agent],
                     list_agent_ghost: List[Agent],
                     graphics_pacman: GraphicsPacman,
                     number_of_games: int,
                     bool_record: bool,
                     num_training: int = 0,
                     bool_catch_exceptions: bool = False,
                     timeout: int = 30,
                     **kwargs,
                     ) -> List[Game]:
    """
    Execute playing Pacman

    :param str_path_layout:
    :param list_agent_pacman:
    :param list_agent_ghost:
    :param _graphics_pacman:
    :param number_of_games:
    :param bool_record:
    :param num_training:
    :param bool_catch_exceptions:
    :param timeout:
    :return:
    """

    print("#" * 100, run_pacman_games.__name__)
    __ALL = (
        str_path_layout,
        list_agent_pacman,
        list_agent_ghost,
        graphics_pacman,
        number_of_games,
        bool_record,
        num_training,
        bool_catch_exceptions,
        timeout)
    pprint(__ALL)
    print("#" * 100)

    classic_game_rules: ClassicGameRules = ClassicGameRules(timeout)
    list_game: List[Game] = []

    for i in range(number_of_games):
        bool_quiet = i < num_training

        if bool_quiet:
            # Suppress output and graphics
            _graphics_pacman = GraphicsPacmanNull()
            classic_game_rules.set_quiet(True)
        else:

            # Set the current graphics pacman to the given graphics_pacman
            _graphics_pacman = graphics_pacman

            # _graphics_pacman = GraphicsPacmanGUI()  # TODO: NEED TO GIVE ARG IF YOU WANT TO DISPLAY GAME IN TEH FUNCTION CALL run_pacman_games
            # _graphics_pacman = GraphicsPacmanNull()
            classic_game_rules.set_quiet(False)

        #####

        ####
        game = classic_game_rules.create_and_get_game(
            str_path_layout,
            list_agent_pacman,
            list_agent_ghost,
            _graphics_pacman,
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
                components = {'str_path_layout': str_path_layout, 'actions': game.moveHistory}
                pickle.dump(components, f)

    if (number_of_games - num_training) > 0:
        scores = [game.state_pacman.getScore() for game in list_game]
        wins = [game.state_pacman.isWin() for game in list_game]
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

    namespace = get_argparse_namespace_for_pacman(sys.argv[1:])  # Get game components based on input

    dict_namespace = get_dict_namespace(namespace)

    print("----- pprint(dict_namespace) START -----")
    pprint(dict_namespace)
    print("----- pprint(dict_namespace) END -----")
    run_pacman_games(**dict_namespace)

    # import cProfile
    # cProfile.run("runGames( **kwargs )")
    pass
