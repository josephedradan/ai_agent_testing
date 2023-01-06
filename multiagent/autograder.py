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

from multiagent.grader import Grader
from multiagent.graphics.graphics import Graphics

print(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # FIXME: GHETTO SOLUTION TO MISSING MODULE
# pprint(sys.path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# imports from python standard library
from types import ModuleType
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type
from typing import Union

import projectParams
from multiagent._question import Question
from multiagent._question import get_class_question_subclass
from multiagent._test_case import TestCase
from multiagent._test_case import get_class_test_case_subclass
from multiagent import parse_file

random.seed(0)


# try:
#     from pacman import GameState
# except:
#     pass

# register arguments and set default values
def readCommand(argv: Union[Sequence[str], None] = None):
    parser = argparse.ArgumentParser(description='Run public tests on student code')

    parser.set_defaults(bool_generate_solutions=False,
                        # TODO: DONT USE BECAUSE ONLY TEACHERS CAN USE THIS BECAUSE I DONT HAVE THE CLASS
                        bool_html_output=False,  # Export as html
                        bool_json_output=False,  # Json output
                        bool_mute_output=False,  # bool_mute_output the tests in the terminal
                        bool_print_test_case=False,  # Print the .test file when running
                        noGraphics=False  # ONLY APPLICABLE WHEN USING --name_question OR -q
                        )
    parser.add_argument('--test-directory',
                        dest='path_',
                        default='test_cases',  # CHANGE THIS
                        help='Root test directory which contains subdirectories corresponding to each name_question')
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
                        dest='bool_html_output',
                        action='store_true',
                        help='Generate edX output files')
    parser.add_argument('--gradescope-output',
                        dest='bool_json_output',
                        action='store_true',
                        help='Generate GradeScope output files')
    parser.add_argument('--bool_mute_output',
                        dest='bool_mute_output',
                        action='store_true',
                        help='Mute output from executing tests')
    parser.add_argument('--print-tests', '-p',
                        dest='bool_print_test_case',
                        action='store_true',
                        help='Print each test case before running them.')
    parser.add_argument('--test', '-t',  # -t "test_cases/q1/grade-agent"
                        dest='path_test',
                        default=None,
                        help='Run one particular test.  Relative to test root.')
    parser.add_argument('--name_question', '-q',
                        dest='str_question_to_be_graded',
                        default=None,
                        help='Grade one particular name_question.')
    parser.add_argument('--no-graphics',
                        dest='noGraphics',
                        # default=True,
                        # action='store_false',
                        action='store_true',
                        help='No graphics display for pacman games.')

    options = parser.parse_args(argv)

    print(options)
    return options


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


def readFile(path, root=""):
    "Read file from disk at specified path and return as string"
    with open(os.path.join(root, path), 'r') as handle:
        return handle.read()


#######################################################################
# Error Hint Map
#######################################################################

# TODO: use these
ERROR_HINT_MAP = {
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


def printTest(testDict, solutionDict):
    pp = pprint.PrettyPrinter(indent=4)
    print("Test case:")
    for line in testDict["__raw_lines__"]:
        print("   |", line)
    print("Solution:")
    for line in solutionDict["__raw_lines__"]:
        print("   |", line)


def run_path_test(path_test: str, moduleDict, printTestCase: bool = False,
                  display: Graphics = None):  # TODO: RUNS A SPECIFIC TEST GIVEN NAME
    import parse_file
    for module in moduleDict:
        setattr(sys.modules[__name__], module, moduleDict[module])

    dict_test = parse_file.ParseFile(path_test + ".test").get_dict()
    dict_solution = parse_file.ParseFile(path_test + ".solution").get_dict()
    test_out_file = os.path.join('%s.test_output' % path_test)
    dict_test['test_out_file'] = test_out_file
    class_test_case = get_class_test_case_subclass(dict_test['class'])

    # class_question_subclass: Type[Question] = get_class_question_subclass(dict_question['class'])
    # name_question: Question = class_question_subclass(dict_question, display)

    path_directory_of_path_test = os.path.dirname(path_test)

    dict_question_config, question_object = get_question_stuff(path_directory_of_path_test, display)

    # class_question = get_class_question_subclass("Question")
    # name_question = class_question({'max_points': 0}, display)
    # test_case_object = class_test_case(name_question, dict_test)

    test_case_object = class_test_case(question_object, dict_test)

    print(f"DISPLAY FROM {run_path_test.__name__}", display)

    if printTestCase:
        printTest(dict_test, dict_solution)

    # This is a fragile hack to create a stub grader_ object
    grader = Grader(projectParams.PROJECT_NAME, [(None, 0)])
    test_case_object.execute(grader, moduleDict, dict_solution)


# returns all the tests you need to run in order to run name_question
def getDepends(testParser, testRoot, question):
    allDeps = [question]
    questionDict = testParser.ParseFile(
        os.path.join(testRoot, question, 'CONFIG')).get_dict()
    if 'depends' in questionDict:
        depends = questionDict['depends'].split()
        for d in depends:
            # run dependencies first
            allDeps = getDepends(testParser, testRoot, d) + allDeps
    return allDeps


# get list of questions to grade
def getTestSubdirs(parser, path_: str, str_question_to_grade: str):
    problemDict = parser.ParseFile(os.path.join(path_, 'CONFIG')).get_dict()

    if str_question_to_grade != None:
        questions = getDepends(parser, path_, str_question_to_grade)

        if len(questions) > 1:
            print('Note: due to dependencies, the following tests will be run: %s' %
                  ' '.join(questions))
        return questions
    if 'order' in problemDict:
        return problemDict['order'].split()
    return sorted(os.listdir(path_))


# evaluate student code
def evaluate(AgentPacmanMinimaxAlphaBeta: bool,
             path_abs_test_cases: str,  # TODO: THIS IS RELATIVE PATH
             moduleDict: Dict[str, ModuleType],
             # TODO: THIS IS THE THING THAT CONTAINS {"multiAgent": ..., multiAgentTestClass: ...}
             exceptionMap=ERROR_HINT_MAP,
             bool_html_output: bool = False,
             bool_mute_output: bool = False,
             bool_json_output: bool = False,
             bool_print_test_case: bool = False,
             question_to_grade: Union[str, None] = None,
             display=None
             ):
    # TODO: JOSEPH THIS IS WHERE ALL THE TESTS ARE DONE

    # imports of testbench code.  note that the testClasses import must follow
    # the import of student code due to dependencies
    for module in moduleDict:
        print(sys.modules[__name__], module, moduleDict[module], sep=" | ")
        setattr(sys.modules[__name__], module, moduleDict[
            module])  # `x.y = v' # TODO: Add attribute 'module' to sys.modules[__name__] with value moduleDict[module]

    list_tuple__question_name__points_max: List[Tuple[str, int]] = []

    dict_k_name_question_v_dict_question_config: Dict[str, Dict[Any]] = {}

    dict_k_name_question_v_callable: Dict[str, Callable] = {}

    # TODO: THIS SHIT GETS MAKES THIS ['q1', 'q2', 'q3', 'q4', 'q5']
    test_subdirs = getTestSubdirs(parse_file, path_abs_test_cases, question_to_grade)
    for q in test_subdirs:
        subdir_path = os.path.join(path_abs_test_cases, q)
        if not os.path.isdir(subdir_path) or q[0] == '.':
            continue

        dict_question_config: Dict[str, Any]
        question_object: Question
        dict_question_config, question_object = get_question_stuff(subdir_path, display)

        dict_k_name_question_v_dict_question_config[q] = dict_question_config

        # load test cases into name_question
        list_file_test_name = [t for t in os.listdir(subdir_path) if re.match('[^#~.].*\.test\Z', t)]

        list_file_test_name_no_ext = [re.match('(.*)\.test\Z', t).group(1) for t in list_file_test_name]

        for test_no_ext in sorted(list_file_test_name_no_ext):

            # TODO: THIS IS ACTUAL TEST 'test_cases\\q2\\8-pacman-game.test'
            path_test_test = os.path.join(subdir_path, '%s.test' % test_no_ext)

            # TODO: THIS IS  THE ANSWERS FILE 'test_cases\\q2\\8-pacman-game.solution'
            path_test_solution = os.path.join(subdir_path, '%s.solution' % test_no_ext)

            # TODO: 'test_cases\\q1\\grade-agent.test_output'  # NOT USED?
            path_test_output = os.path.join(subdir_path, '%s.test_output' % test_no_ext)
            ''
            # TODO: A DICT
            dict_test = parse_file.ParseFile(path_test_test).get_dict()

            if dict_test.get("disabled", "false").lower() == "true":
                continue

            dict_test['path_test_output'] = path_test_output

            # TODO: dict_test['class'] will be EvalAgentTest ... SO IT WILL GET projectTestClasses.EvalAgentTest  OR projectTestClasses.GraphGameTreeTest ..... projectTestClasses MIGHT BE multiagentTestClasses
            class_test_case = get_class_test_case_subclass(dict_test['class'])
            print("class_test_case", class_test_case)

            # TODO: MIGHT BE EvalAgentTest, GraphGameTreeTest, PacmanGameTreeTest, IT IS A CLASS
            test_case: TestCase = class_test_case(question_object, dict_test)

            def makefun(testCase, solution_file) -> Callable:
                grader_: Grader

                if AgentPacmanMinimaxAlphaBeta:
                    # write solution file to disk
                    return lambda grader_: testCase.writeSolution(moduleDict, solution_file)
                else:
                    # read in solution dictionary and pass as an argument
                    testDict = parse_file.ParseFile(path_test_test).get_dict()
                    solutionDict = parse_file.ParseFile(solution_file).get_dict()  # TODO: READ THE TEST FILE

                    if bool_print_test_case:  # PRINT THE TEST CASE AND TEST THE PROBLEM
                        return lambda grades: printTest(testDict, solutionDict) or testCase.execute(grades,
                                                                                                    moduleDict,
                                                                                                    solutionDict)
                    else:
                        return lambda grader_: testCase.execute(grader_, moduleDict, solutionDict)

            question_object.add_test_case(test_case, makefun(test_case, path_test_solution))

        # Note extra function is necessary for scoping reasons
        def makefun(question):
            grader_: Grader
            return lambda grader_: question.execute(grader_)

        # print("makefun thingy", sys.modules[__name__], q, makefun(question_object))
        # setattr(sys.modules[__name__], q, makefun(question_object))

        dict_k_name_question_v_callable[q] = makefun(question_object)

        # TODO: LIST OF TUPLE:  ('Questison Nubmer', Max points int)
        list_tuple__question_name__points_max.append((q, question_object.get_points_max()))

    grader = Grader(
        projectParams.PROJECT_NAME,
        list_tuple__question_name__points_max,
        bool_json_output=bool_json_output,
        bool_html_output=bool_html_output,
        bool_mute_output=bool_mute_output
    )

    # TODO: THIS IF CONDITIONAL DOES NOTHING IMPORTANT
    if question_to_grade == None:
        for q in dict_k_name_question_v_dict_question_config:
            pprint.pprint(dict_k_name_question_v_dict_question_config)
            for prereq in dict_k_name_question_v_dict_question_config[q].get('depends',
                                                                             '').split():  # TODO: depends DOES NOT EXIST? LOOK IS NEVER REACHED

                grader.addPrereq(q, prereq)

    # TODO: RUNNING THE TESTS ARE IN THIS CALL
    grader.grade(dict_k_name_question_v_callable, bool_display_picture_bonus=projectParams.BONUS_PIC)
    return grader.points


def getDisplay(graphicsByDefault: Union[bool, None], options=None):
    # from multiagent.graphics import graphicsDisplay
    # return graphicsDisplay.PacmanGraphicsReal(1, frameTime=.05)
    graphics = graphicsByDefault
    if options is not None and options.noGraphics:
        graphics = False
    if graphics:
        try:
            from multiagent.graphics import graphicsDisplay
            return graphicsDisplay.PacmanGraphicsReal(1, frameTime=.05)
        except ImportError:
            pass
    from multiagent.graphics import textDisplay
    return textDisplay.NullGraphics()


def get_question_stuff(path_question: str, display: Graphics) -> Tuple[Dict[str, Any], Question]:
    dict_question_config: Dict[str, Any] = parse_file.ParseFile(os.path.join(path_question, 'CONFIG')).get_dict()

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

    options = readCommand(
        # sys.argv  # DONT USE THIS UNLESS USING optparse
    )
    if options.bool_generate_solutions:
        confirmGenerate()
    codePaths = options.studentCode.split(',')
    # moduleCodeDict = {}
    # for cp in codePaths:
    #     moduleName = re.match('.*?([^/]*)\.py', cp).group(1)
    #     moduleCodeDict[moduleName] = readFile(cp, root=options.codeRoot)
    # moduleCodeDict['projectTestClasses'] = readFile(options.testCaseCode, root=options.codeRoot)
    # moduleDict = loadModuleDict(moduleCodeDict)
    print("codePaths", codePaths)
    moduleDict = {}
    for cp in codePaths:
        moduleName = re.match('.*?([^/]*)\.py', cp).group(1)

        moduleDict[moduleName] = loadModuleFile(moduleName, os.path.join(options.codeRoot, cp))

    # moduleName = re.match('.*?([^/]*)\.py', options.testCaseCode).group(1)  # 'multiagentTestClasses'

    print("moduleNameFFFFFFFFFF", moduleName)

    moduleDict['projectTestClasses'] = loadModuleFile(moduleName, os.path.join(options.codeRoot, options.testCaseCode))

    if options.path_test != None:
        run_path_test(options.path_test,
                      moduleDict,
                      printTestCase=options.bool_print_test_case,
                      display=getDisplay(True, options))
    else:
        evaluate(
            options.bool_generate_solutions,
            # options.path_,
            'test_cases/multiagent',
            moduleDict,
            bool_json_output=options.bool_json_output,
            bool_html_output=options.bool_html_output,
            bool_mute_output=options.bool_mute_output,
            bool_print_test_case=options.bool_print_test_case,
            question_to_grade=options.str_question_to_be_graded,
            display=getDisplay(options.str_question_to_be_graded != None, options)
        )
