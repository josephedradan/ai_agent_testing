# autograder.py
# -------------
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
import imp
import optparse
import os
import random
import re
import sys
from typing import Callable
from typing import Sequence

print(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # FIXME: GHETTO SOLUTION TO MISSING MODULE
# pprint(sys.path_file_test)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pacman.test_case import TestCase
from pacman.test_case import get_subclass_test_case
from pacman.grader import Grader
from pacman.graphics.graphics_pacman import GraphicsPacman
from pacman.parser import ParseFile

# imports from python standard library
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type
from typing import Union

import projectParams
from pacman.question.question import Question
from pacman.question import get_class_question_subclass

random.seed(0)


# try:
#     from agent_pacman_ import GameState
# except:
#     pass

# register arguments and set default values
def arg_parser_autograder(argv: Union[Sequence[str], None] = None):
    parser = argparse.ArgumentParser(description='Run public tests on student code')

    parser.set_defaults(bool_generate_solutions=False,
                        # TODO: DONT USE BECAUSE ONLY TEACHERS CAN USE THIS BECAUSE I DONT HAVE THE CLASS
                        bool_output_html=False,  # Export as html
                        bool_output_json=False,  # Json output
                        bool_output_mute=False,  # bool_output_mute the tests in the terminal
                        bool_print_test_case=False,  # Print the .test file when running
                        noGraphics=False  # ONLY APPLICABLE WHEN USING --str_question OR -q
                        )
    parser.add_argument('--test-directory',
                        dest='path_dir_containing_question',
                        default='test_cases',  # CHANGE THIS
                        help='Root test directory which contains subdirectories corresponding to each str_question')
    parser.add_argument('--student-code',
                        dest='studentCode',
                        default=projectParams.STUDENT_CODE_DEFAULT,
                        help='comma separated list of student code files')
    parser.add_argument('--code-directory',
                        dest='codeRoot',
                        default="",
                        help='Root directory containing the student and testClass code')
    parser.add_argument('--test-case-code',
                        dest='testCaseCode',
                        default=projectParams.PROJECT_TEST_CLASSES,
                        help='class containing testClass classes for this name_project')
    parser.add_argument('--generate-solutions',  # TODO: THIS IS FOR TEACHERS, WILL NOT WORK BECAUSE MISSING CLASS
                        dest='bool_generate_solutions',
                        action='store_true',
                        help='Write solutions generated to .solution file')
    parser.add_argument('--edx-output',
                        dest='bool_output_html',
                        action='store_true',
                        help='Generate edX output files')
    parser.add_argument('--gradescope-output',
                        dest='bool_output_json',
                        action='store_true',
                        help='Generate GradeScope output files')
    parser.add_argument('--bool_output_mute',
                        dest='bool_output_mute',
                        action='store_true',
                        help='Mute output from executing tests')
    parser.add_argument('--print-tests', '-p',
                        dest='bool_print_test_case',
                        action='store_true',
                        help='Print each test case before running them.')
    parser.add_argument('--test', '-t',  # -t "test_cases/q1/grade-agent"
                        dest='path_file_test',
                        default=None,
                        help='Run one particular test. Relative to test root.')
    parser.add_argument('--str_question', '-q',
                        dest='str_question_to_be_graded',
                        default=None,
                        help='Grade one particular question.')
    parser.add_argument('--no-graphics',
                        dest='noGraphics',
                        # default=True,
                        # action='store_false',
                        action='store_true',
                        help='No graphics display for pacman games.')

    argparse_args = parser.parse_args(argv)

    print(argparse_args)
    return argparse_args


# confirm we should author solution files
def confirmGenerate():
    print('WARNING: this action will overwrite any solution files.')
    print('Are you sure you want to proceed? (yes/no)')
    while True:
        ans = sys.stdin.readline().strip()
        if ans == 'yes':
            break
        elif ans == 'no':
            sys.exit(0)
        else:
            print('please answer either "yes" or "no"')


# TODO: Fix this so that it tracebacks work correctly
# Looking at source of the traceback module, presuming it works
# the same as the intepreters, it uses co_filename.  This is,
# however, a readonly attribute.
def setModuleName(module, filename):
    functionType = type(confirmGenerate)
    classType = type(optparse.Option)

    for i in dir(module):
        o = getattr(module, i)
        if hasattr(o, '__file__'):
            continue

        if type(o) == functionType:
            setattr(o, '__file__', filename)
        elif type(o) == classType:
            setattr(o, '__file__', filename)
            # TODO: assign member __file__'s?
        # print i, type(o)


# from cStringIO import StringIO

# def loadModuleString(moduleSource):
#     # Below broken, imp doesn't believe its being passed a file:
#     #    ValueError: load_module arg#2 should be a file or None
#     #
#     # f = StringIO(moduleCodeDict[k])
#     # tmp = imp.load_module(k, f, k, (".py", "r", imp.PY_SOURCE))
#     tmp = imp.new_module(k)
#     exec(moduleCodeDict[k], tmp.__dict__)
#     setModuleName(tmp, k)
#     return tmp


def loadModuleFile(moduleName, filePath):
    with open(filePath, 'r') as f:
        return imp.load_module(moduleName, f, "%s.py" % moduleName, (".py", "r", imp.PY_SOURCE))


def readFile(path_file_test, root=""):
    "Read file from disk at specified path_file_test and return as string"
    with open(os.path.join(root, path_file_test), 'r') as handle:
        return handle.read()


#######################################################################
# Error Hint Map
#######################################################################

# TODO: use these
DICT_K_STR_QUESTION_V_STR_ERROR_HINT = {
    'q1': {
        "<type 'exceptions.IndexError'>": """
      We noticed that your name_project threw an IndexError on q1.
      While many things may cause this, it may have been from
      assuming a certain number of successors from a game_state space
      or assuming a certain number of actions available from a given
      game_state. Try making your code more general (no hardcoded indices)
      and submit again!
    """
    },
    'q3': {
        "<type 'exceptions.AttributeError'>": """
        We noticed that your name_project threw an AttributeError on q3.
        While many things may cause this, it may have been from assuming
        a certain size or structure to the game_state space. For example, if you have
        a line of code assuming that the game_state is (x, y) and we run your code
        on a game_state space with (x, y, z), this error could be thrown. Try
        making your code more general and submit again!

    """
    }
}

import pprint


def splitStrings(d):
    d2 = dict(d)
    for k in d:
        if k[0:2] == "__":
            del d2[k]
            continue
        if d2[k].find("\n") >= 0:
            d2[k] = d2[k].split("\n")
    return d2


def print_test(dict_file_test: Dict, dict_file_solution: Dict):
    pp = pprint.PrettyPrinter(indent=4)

    print("Test case:")
    for line in dict_file_test["__raw_lines__"]:
        print("   |", line)

    print("Solution:")
    for line in dict_file_solution["__raw_lines__"]:
        print("   |", line)


def run_path_test(path_file_test: str,
                  bool_print_test_cases: bool = False,
                  graphics_pacman: GraphicsPacman = None
                  ):

    dict_file_test = ParseFile(path_file_test + ".test").get_dict()
    dict_file_solution = ParseFile(path_file_test + ".solution").get_dict()
    file_test_output = os.path.join('%s.test_output' % path_file_test)
    dict_file_test['file_test_output'] = file_test_output
    class_test_case = get_subclass_test_case(dict_file_test['class'])

    path_directory_of_path_test = os.path.dirname(path_file_test)

    dict_question_config, question_object = get_question_stuff(path_directory_of_path_test, graphics_pacman)

    # class_question = get_class_question_subclass("Question")
    # str_question = class_question({'max_points': 0}, graphics_pacman)
    # test_case_object = class_test_case(str_question, dict_file_test)

    test_case_object = class_test_case(question_object, dict_file_test)

    print(f"DISPLAY FROM {run_path_test.__name__}", graphics_pacman)

    if bool_print_test_cases:
        print_test(dict_file_test, dict_file_solution)

    # This is a fragile hack to create a stub grader__ object
    grader = Grader(projectParams.PROJECT_NAME, [(None, 0)])
    test_case_object.execute(
        grader,
        # moduleDict,
        dict_file_solution
    )


#
def get_list_str_question_depends(path_dir_containing_question: str, str_question: str) -> List[str]:
    """
    Give the path of the dir containing questions

    returns all a lists of the names of questions you need to run in order to run the question str_question

    Notes:
        It looks like dependencies must have the same parent directory containing question directories, so different
        parent directories won't work such as between the 2 directories below:
            test_cases/search/
            test_cases/multiagent/

    :param path_dir_containing_question:
    :param str_question:
    :return:
    """
    list_str_question = [str_question]

    # Example: "test_cases/multiagent/", "q2", "CONFIG"
    dict_question = ParseFile(os.path.join(path_dir_containing_question, str_question, 'CONFIG')).get_dict()

    # The only CONFIG files that have 'depends' are in a question directory
    if 'depends' in dict_question:  #

        depends = dict_question['depends'].split()

        for name_question_ in depends:
            # run dependencies first
            list_str_question.extend(get_list_str_question_depends(path_dir_containing_question, name_question_))

    return list_str_question


def get_list_str_question(path_dir: str, str_question: str) -> List[str]:
    """
    get list of questions to grade

    :param path_dir:
    :param str_question:
    :return:
    """

    dict_problem = ParseFile(os.path.join(path_dir, 'CONFIG')).get_dict()

    if str_question is not None:
        list_str_question = get_list_str_question_depends(path_dir, str_question)

        if len(list_str_question) > 1:
            print('Note: due to dependencies, the following tests will be run: {}'.format(' '.join(list_str_question)))
        return list_str_question
    if 'order' in dict_problem:
        return dict_problem['order'].split()
    return sorted(os.listdir(path_dir))


# evaluate student code
def evaluate(bool_generate_solutions: bool,
             path_abs_test_cases: str,  # TODO: THIS IS RELATIVE PATH
             # moduleDict: Dict[string_given, ModuleType],
             # TODO: THIS IS THE THING THAT CONTAINS {"multiAgent": ..., multiAgentTestClass: ...}
             exceptionMap=DICT_K_STR_QUESTION_V_STR_ERROR_HINT,
             bool_output_html: bool = False,
             bool_output_mute: bool = False,
             bool_output_json: bool = False,
             bool_print_test_case: bool = False,
             str_question_to_grade: Union[str, None] = None,
             display=None
             ):
    # TODO: JOSEPH THIS IS WHERE ALL THE TESTS ARE DONE

    # imports of testbench code.  note that the testClasses import must follow
    # the import of student code due to dependencies
    # for module in moduleDict:
    #     print(sys.modules[__name__], module, moduleDict[module], sep=" | ")
    #     setattr(sys.modules[__name__], module, moduleDict[
    #         module])  # `x.y = v' # TODO: Add attribute 'module' to sys.modules[__name__] with value moduleDict[module]

    list_tuple__question_name__points_max: List[Tuple[str, int]] = []

    dict_k_name_question_v_dict_question_config: Dict[str, Dict[Any]] = {}

    dict_k_name_question_v_callable: Dict[str, Callable] = {}

    # TODO: THIS SHIT GETS MAKES THIS ['q1', 'q2', 'q3', 'q4', 'q5']
    list_str_question_to_grade = get_list_str_question(path_abs_test_cases, str_question_to_grade)
    print("FSDFSDF", list_str_question_to_grade)
    for str_question in list_str_question_to_grade:
        path_question = os.path.join(path_abs_test_cases, str_question)
        if not os.path.isdir(path_question) or str_question[0] == '.':
            continue

        dict_question_config: Dict[str, Any]
        question_object: Question
        dict_question_config, question_object = get_question_stuff(path_question, display)

        dict_k_name_question_v_dict_question_config[str_question] = dict_question_config

        # load test cases into str_question
        list_file_test_name = [t for t in os.listdir(path_question) if re.match('[^#~.].*\.test\Z', t)]

        list_file_test_name_no_ext = [re.match('(.*)\.test\Z', t).group(1) for t in list_file_test_name]

        for test_no_ext in sorted(list_file_test_name_no_ext):

            # TODO: THIS IS ACTUAL TEST 'test_cases\\q2\\8-pacman-game.test'
            path_test_test = os.path.join(path_question, '%s.test' % test_no_ext)

            # TODO: THIS IS  THE ANSWERS FILE 'test_cases\\q2\\8-pacman-game.solution'
            path_test_solution = os.path.join(path_question, '%s.solution' % test_no_ext)

            # TODO: 'test_cases\\q1\\grade-agent.test_output'  # NOT USED?
            path_test_output = os.path.join(path_question, '%s.test_output' % test_no_ext)
            ''
            # TODO: A DICT
            dict_file_test = ParseFile(path_test_test).get_dict()

            if dict_file_test.get("disabled", "false").lower() == "true":
                continue

            dict_file_test['path_test_output'] = path_test_output

            # TODO: dict_file_test['class'] will be EvalAgentTest ... SO IT WILL GET projectTestClasses.EvalAgentTest  OR projectTestClasses.GraphGameTreeTest ..... projectTestClasses MIGHT BE multiagentTestClasses
            subclass_test_case = get_subclass_test_case(dict_file_test['class'])

            # TODO: MIGHT BE EvalAgentTest, GraphGameTreeTest, PacmanGameTreeTest, IT IS A CLASS
            test_case: TestCase = subclass_test_case(question_object, dict_file_test)

            def makefun(test_case_: TestCase, path_test_solution_: str) -> Callable:
                grader_: Grader

                if bool_generate_solutions:
                    # write solution file to disk
                    return lambda grader__: test_case_.writeSolution(path_test_solution_)
                else:
                    # read in solution dictionary and pass as an argument
                    dict_file_test_ = ParseFile(path_test_test).get_dict()

                    dict_file_solution_ = ParseFile(path_test_solution_).get_dict()  # TODO: READ THE SOLUTIOn FILE

                    if bool_print_test_case:  # PRINT THE TEST CASE AND TEST THE PROBLEM

                        def _print_test_and_execute_test(grader__: Grader):
                            print_test(dict_file_test_, dict_file_solution_)
                            test_case_.execute(grader__, dict_file_solution_)

                        return _print_test_and_execute_test
                    else:
                        return lambda grader__: test_case_.execute(grader__, dict_file_solution_)

            question_object.add_test_case(test_case, makefun(test_case, path_test_solution))

        # Note extra function is necessary for scoping reasons
        def makefun(question):
            grader_: Grader
            return lambda grader_: question.execute(grader_)

        # print("makefun thingy", sys.modules[__name__], str_question, makefun(question_object))
        # setattr(sys.modules[__name__], str_question, makefun(question_object))

        dict_k_name_question_v_callable[str_question] = makefun(question_object)

        # TODO: LIST OF TUPLE:  ('Questison Nubmer', Max points int)
        list_tuple__question_name__points_max.append((str_question, question_object.get_points_max()))

    grader = Grader(
        projectParams.PROJECT_NAME,
        list_tuple__question_name__points_max,
        bool_output_json=bool_output_json,
        bool_output_html=bool_output_html,
        bool_output_mute=bool_output_mute
    )

    # TODO: THIS IF CONDITIONAL DOES NOTHING IMPORTANT -- WRONG
    if str_question_to_grade is None:
        for str_question in dict_k_name_question_v_dict_question_config:
            # pprint.pprint(dict_k_name_question_v_dict_question_config)
            # print("FAF",str_question_to_grade,  str_question,dict_k_name_question_v_dict_question_config[str_question])

            # TODO: str_depends DOES NOT EXIST? LOOK IS NEVER REACHED

            # TODO:  LOOK AT THIS MESS WITH NONE IN THE CONDITIONAL BELOW
            str_depends = dict_k_name_question_v_dict_question_config[str_question].get('depends', '')

            if str_depends is not None:

                for prereq in str_depends.split():
                    grader.addPrereq(str_question, prereq)

    # TODO: RUNNING THE TESTS ARE IN THIS CALL
    grader.grade(dict_k_name_question_v_callable, bool_display_picture_bonus=projectParams.BONUS_PIC)
    return grader.points


def get_graphics_pacman(graphicsByDefault: Union[bool, None], options=None) -> GraphicsPacman:
    # from multiagent.graphics import graphicsDisplay
    # return graphicsDisplay.GraphicsPacmanDisplayTkinter(1, frameTime=.05)

    graphics = graphicsByDefault
    if options is not None and options.noGraphics:
        graphics = False
    if graphics:
        try:
            from pacman.graphics import graphics_pacman_display_tkiner
            return graphics_pacman_display_tkiner.GraphicsPacmanDisplayTkinter(
                time_frame=0.05
            )
        except ImportError:
            pass

    from pacman.graphics import graphics_pacman_null
    return graphics_pacman_null.GraphicsPacmanNull()


def get_question_stuff(path_question: str, display: GraphicsPacman) -> Tuple[Dict[str, Any], Question]:
    dict_question_config: Dict[str, Any] = ParseFile(os.path.join(path_question, 'CONFIG')).get_dict()

    class_question_subclass: Type[Question] = get_class_question_subclass(dict_question_config['class'])
    question_object: Question = class_question_subclass(dict_question_config, display)

    return dict_question_config, question_object


if __name__ == '__main__':

    print(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # FIXME: GHETTO SOLUTION TO MISSING MODULE
    # pprint(sys.path)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    ##############################
    ##############################
    ##############################

    argparse_args = arg_parser_autograder(
        # sys.argv  # DONT USE THIS UNLESS USING optparse
        sys.argv[1:]
    )

    if argparse_args.bool_generate_solutions:
        confirmGenerate()
    codePaths = argparse_args.studentCode.split(',')  # TODO: ['multiAgents.py']

    print("codePaths", codePaths)

    # moduleCodeDict = {}
    # for cp in codePaths:
    #     moduleName = re.match('.*?([^/]*)\.py', cp).group(1)
    #     moduleCodeDict[moduleName] = readFile(cp, root=options.codeRoot)
    # moduleCodeDict['projectTestClasses'] = readFile(options.testCaseCode, root=options.codeRoot)
    # moduleDict = loadModuleDict(moduleCodeDict)
    #
    # print("codePaths", codePaths)
    # moduleDict = {}
    # for cp in codePaths:
    #     moduleName = re.match('.*?([^/]*)\.py', cp).group(1)
    #
    #     moduleDict[moduleName] = loadModuleFile(moduleName, os.path.join(options.codeRoot, cp))

    # moduleName = re.match('.*?([^/]*)\.py', options.testCaseCode).group(1)  # 'multiagentTestClasses'

    # print("moduleNameFFFFFFFFFF", moduleName)

    # moduleDict['projectTestClasses'] = loadModuleFile(moduleName, os.path.join(options.codeRoot, options.testCaseCode))

    if argparse_args.path_file_test != None:
        run_path_test(
            argparse_args.path_file_test,
            bool_print_test_cases=argparse_args.bool_print_test_case,
            graphics_pacman=get_graphics_pacman(True, argparse_args)
        )
    else:
        evaluate(
            argparse_args.bool_generate_solutions,
            # options.path_dir_containing_question,
            # 'test_cases/search',
            # 'test_cases/multiagent',
            # 'test_cases/reinforcement',
            'test_cases',
            # moduleDict,
            bool_output_json=argparse_args.bool_output_json,
            bool_output_html=argparse_args.bool_output_html,
            bool_output_mute=argparse_args.bool_output_mute,
            bool_print_test_case=argparse_args.bool_print_test_case,
            str_question_to_grade=argparse_args.str_question_to_be_graded,
            display=get_graphics_pacman(argparse_args.str_question_to_be_graded != None, argparse_args)
        )
