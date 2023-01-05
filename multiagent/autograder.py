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


import imp
import optparse
import os
import random
import re
import sys

from multiagent import parse_file
from multiagent.parse_file import ParseFile

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

import grading
import projectParams
from multiagent._question import Question
from multiagent._question import get_class_question_subclass
from multiagent._test_case import TestCase
from multiagent._test_case import get_class_test_case_subclass

random.seed(0)


# try:
#     from pacman import GameState
# except:
#     pass

# register arguments and set default values
def readCommand(argv):
    parser = optparse.OptionParser(
        description='Run public tests on student code')
    parser.set_defaults(generateSolutions=False,  # TODO: DONT USE BECAUSE ONLY TEACHERS CAN USE THIS BECAUSE I DONT HAVE THE CLASS
                        edxOutput=False,
                        gsOutput=False,
                        muteOutput=False,
                        printTestCase=False,
                        noGraphics=False)
    parser.add_option('--test-directory',
                      dest='testRoot',
                      default='test_cases',
                      help='Root test directory which contains subdirectories corresponding to each question')
    parser.add_option('--student-code',
                      dest='studentCode',
                      default=projectParams.STUDENT_CODE_DEFAULT,
                      help='comma separated list of student code files')
    parser.add_option('--code-directory',
                      dest='codeRoot',
                      default="",
                      help='Root directory containing the student and testClass code')
    parser.add_option('--test-case-code',
                      dest='testCaseCode',
                      default=projectParams.PROJECT_TEST_CLASSES,
                      help='class containing testClass classes for this project')
    parser.add_option('--generate-solutions',  # TODO: THIS IS FOR TEACHERS, WILL NOT WORK BECAUSE MISSING CLASS
                      dest='generateSolutions',
                      action='store_true',
                      help='Write solutions generated to .solution file')
    parser.add_option('--edx-output',
                      dest='edxOutput',
                      action='store_true',
                      help='Generate edX output files')
    parser.add_option('--gradescope-output',
                      dest='gsOutput',
                      action='store_true',
                      help='Generate GradeScope output files')
    parser.add_option('--mute',
                      dest='muteOutput',
                      action='store_true',
                      help='Mute output from executing tests')
    parser.add_option('--print-tests', '-p',
                      dest='printTestCase',
                      action='store_true',
                      help='Print each test case before running them.')
    parser.add_option('--test', '-t',
                      dest='runTest',
                      default=None,
                      help='Run one particular test.  Relative to test root.')
    parser.add_option('--question', '-q',
                      dest='gradeQuestion',
                      default=None,
                      help='Grade one particular question.')
    parser.add_option('--no-graphics',
                      dest='noGraphics',
                      # default=True,
                      # action='store_false',
                      action='store_true',
                      help='No graphics display for pacman games.')
    (options, args) = parser.parse_args(argv)
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
      We noticed that your project threw an IndexError on q1.
      While many things may cause this, it may have been from
      assuming a certain number of successors from a game_state space
      or assuming a certain number of actions available from a given
      game_state. Try making your code more general (no hardcoded indices)
      and submit again!
    """
    },
    'q3': {
        "<type 'exceptions.AttributeError'>": """
        We noticed that your project threw an AttributeError on q3.
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


def runTest(testName, moduleDict, printTestCase=False, display=None):  # TODO: RUNS A SPECIFIC TEST GIVEN NAME
    import parse_file
    import _question
    for module in moduleDict:
        setattr(sys.modules[__name__], module, moduleDict[module])

    dict_test = parse_file.ParseFile(testName + ".test").get_dict()
    solutionDict = parse_file.ParseFile(testName + ".solution").get_dict()
    test_out_file = os.path.join('%s.test_output' % testName)
    dict_test['test_out_file'] = test_out_file
    class_test_case = get_class_test_case_subclass(dict_test['class'])

    # class_question_subclass: Type[Question] = get_class_question_subclass(dict_question['class'])
    # question: Question = class_question_subclass(dict_question, display)

    questionClass = get_class_question_subclass("Question")
    question = questionClass({'max_points': 0}, display)
    testCase = class_test_case(question, dict_test)

    if printTestCase:
        printTest(dict_test, solutionDict)

    # This is a fragile hack to create a stub grades object
    grades = grading.Grades(projectParams.PROJECT_NAME, [(None, 0)])
    testCase.execute(grades, moduleDict, solutionDict)


# returns all the tests you need to run in order to run question
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
def getTestSubdirs(testParser, testRoot, questionToGrade):
    problemDict = testParser.ParseFile(
        os.path.join(testRoot, 'CONFIG')).get_dict()
    if questionToGrade != None:
        questions = getDepends(testParser, testRoot, questionToGrade)
        if len(questions) > 1:
            print('Note: due to dependencies, the following tests will be run: %s' %
                  ' '.join(questions))
        return questions
    if 'order' in problemDict:
        return problemDict['order'].split()
    return sorted(os.listdir(testRoot))


# evaluate student code
def evaluate(generate_solutions: bool,
             path_abs_test_cases: str,  # TODO: THIS IS RELATIVE PATH
             moduleDict: Dict[str, ModuleType],
             # TODO: THIS IS THE THING THAT CONTAINS {"multiAgent": ..., multiAgentTestClass: ...}
             exceptionMap=ERROR_HINT_MAP,
             edxOutput: bool = False,
             muteOutput: bool = False,
             gsOutput: bool = False,
             printTestCase: bool = False,
             questionToGrade: Union[str, None] = None,
             display=None):
    # TODO: JOSEPH THIS IS WHERE ALL THE TESTS ARE DONE

    # imports of testbench code.  note that the testClasses import must follow
    # the import of student code due to dependencies
    for module in moduleDict:
        print(sys.modules[__name__], module, moduleDict[module], sep=" | ")
        setattr(sys.modules[__name__], module, moduleDict[
            module])  # `x.y = v' # TODO: Add attribute 'module' to sys.modules[__name__] with value moduleDict[module]

    questions: List[Tuple[str, int]] = []
    dict_k_name_quesiton_v_dict_question_config: Dict[str, Dict[Any]] = {}

    # TODO: THIS SHIT GETS MAKES THIS ['q1', 'q2', 'q3', 'q4', 'q5']
    test_subdirs = getTestSubdirs(parse_file, path_abs_test_cases, questionToGrade)
    for q in test_subdirs:
        subdir_path = os.path.join(path_abs_test_cases, q)
        if not os.path.isdir(subdir_path) or q[0] == '.':
            continue

        dict_question_config, question_object = get_question_stuff(subdir_path, display)

        dict_k_name_quesiton_v_dict_question_config[q] = dict_question_config

        # load test cases into question
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

            def makefun(testCase, solution_file):
                if generate_solutions:
                    # write solution file to disk
                    return lambda grades: testCase.writeSolution(moduleDict, solution_file)
                else:
                    # read in solution dictionary and pass as an argument
                    testDict = parse_file.ParseFile(path_test_test).get_dict()
                    solutionDict = parse_file.ParseFile(solution_file).get_dict()  # TODO: READ THE TEST FILE

                    if printTestCase:  # PRINT THE TEST CASE AND TEST THE PROBLEM
                        return lambda grades: printTest(testDict, solutionDict) or testCase.execute(grades,
                                                                                                    moduleDict,
                                                                                                    solutionDict)
                    else:
                        return lambda grades: testCase.execute(grades, moduleDict, solutionDict)

            question_object.add_test_case(test_case, makefun(test_case, path_test_solution))

        # Note extra function is necessary for scoping reasons
        def makefun(question):
            return lambda grades: question.execute(grades)

        print("FFASD",sys.modules[__name__], q, makefun(question_object))
        setattr(sys.modules[__name__], q, makefun(question_object))
        questions.append((q, question_object.get_max_points()))  # TODO: LIST OF TUPLE:  ('Questison Nubmer', Max points int)

    grades = grading.Grades(projectParams.PROJECT_NAME,
                            questions,
                            gsOutput=gsOutput,
                            edxOutput=edxOutput,
                            muteOutput=muteOutput)

    # TODO: THIS IF CONDITIONAL DOES NOTHING IMPORTANT
    if questionToGrade == None:
        for q in dict_k_name_quesiton_v_dict_question_config:
            # print("AAAA1")
            pprint.pprint(dict_k_name_quesiton_v_dict_question_config)
            for prereq in dict_k_name_quesiton_v_dict_question_config[q].get('depends', '').split():  # TODO: depends DOES NOT EXIST? LOOK IS NEVER REACHED
                # print("AAAA2",(q, prereq))

                grades.addPrereq(q, prereq)

    # TODO: RUNNING THE TESTS ARE IN THIS CALL
    grades.grade(sys.modules[__name__], bonusPic=projectParams.BONUS_PIC)
    return grades.points



def evaluate_2():
    pass

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



def get_question_stuff(path_question: str, display) -> Tuple[Dict[str, Any], Question]:

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

    options = readCommand(sys.argv)
    if options.generateSolutions:
        confirmGenerate()
    codePaths = options.studentCode.split(',')
    # moduleCodeDict = {}
    # for cp in codePaths:
    #     moduleName = re.match('.*?([^/]*)\.py', cp).group(1)
    #     moduleCodeDict[moduleName] = readFile(cp, root=options.codeRoot)
    # moduleCodeDict['projectTestClasses'] = readFile(options.testCaseCode, root=options.codeRoot)
    # moduleDict = loadModuleDict(moduleCodeDict)

    moduleDict = {}
    for cp in codePaths:
        moduleName = re.match('.*?([^/]*)\.py', cp).group(1)

        moduleDict[moduleName] = loadModuleFile(moduleName, os.path.join(options.codeRoot, cp))

    # moduleName = re.match('.*?([^/]*)\.py', options.testCaseCode).group(1)  # 'multiagentTestClasses'

    print("moduleNameFFFFFFFFFF", moduleName)

    moduleDict['projectTestClasses'] = loadModuleFile(moduleName, os.path.join(options.codeRoot, options.testCaseCode))

    if options.runTest != None:
        runTest(options.runTest, moduleDict, printTestCase=options.printTestCase,
                display=getDisplay(True, options))
    else:
        evaluate(
            options.generateSolutions,
            options.testRoot,
            moduleDict,
            gsOutput=options.gsOutput,
            edxOutput=options.edxOutput,
            muteOutput=options.muteOutput,
            printTestCase=options.printTestCase,
            questionToGrade=options.gradeQuestion,  #
            display=getDisplay(options.gradeQuestion != None, options)
        )
