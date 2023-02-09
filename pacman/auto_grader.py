"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/5/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
import argparse
import os
from pprint import pprint
from typing import List
from typing import Sequence
from typing import Union

from pacman import projectParams


def arg_parser(argv: Union[Sequence[str], None] = None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--test-directory',
                        dest='path_dir_containing_question',
                        default='test_cases',  # CHANGE THIS
                        help='Root test directory which contains subdirectories corresponding to each str_question')
    # parser.add_argument('--student-code',
    #                     dest='studentCode',
    #                     default=projectParams.STUDENT_CODE_DEFAULT,
    #                     help='comma separated list of student code files')
    # parser.add_argument('--code-directory',
    #                     dest='codeRoot',
    #                     default="",
    #                     help='Root directory containing the student and testClass code')
    # parser.add_argument('--test-case-code',
    #                     dest='testCaseCode',
    #                     default=projectParams.PROJECT_TEST_CLASSES,
    #                     help='class containing testClass classes for this name_project')
    # parser.add_argument('--generate-solutions',  # TODO: THIS IS FOR TEACHERS, WILL NOT WORK BECAUSE MISSING CLASS
    #                     dest='bool_generate_solutions',
    #                     action='store_true',
    #                     help='Write solutions generated to .solution file')
    parser.add_argument('--html-output',
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
    parser.add_argument('--test', '-t',
                        dest='runTest',
                        default=None,
                        help='Run one particular test.  Relative to test root.')
    parser.add_argument('--str_question', '-q',
                        dest='gradeQuestion',
                        default=None,
                        help='Grade one particular str_question.')
    parser.add_argument('--no-graphics',
                        dest='noGraphics',
                        # default=True,
                        # action='store_false',
                        action='store_true',
                        help='No graphics graphics for pacman games.')

    args = parser.parse_args(argv)


def evaluate_2(path_test_cases: str,
               bool_output_mute: bool = False,
               bool_output_html: bool = False,
               bool_output_json: bool = False,
               bool_print_test_case: bool = False,
               question_to_grade: Union[str, None] = None,
               display=None,
               ):
    dir_current: str
    list_dir: List[str]
    list_file_name: List[str]
    for dir_current, list_dir, list_file_name in os.walk(path_test_cases):

        for file_name in list_file_name:
            if file_name == "CONFIG":
                pass

        print(dir_current)
        for i in list_dir:
            print(i)


if __name__ == '__main__':
    # print(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # FIXME: GHETTO SOLUTION TO MISSING MODULE
    # pprint(sys.path)
    # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    arg_parser()

    #
    #
    # evaluate_2(
    #     options.path_dir_containing_question,
    #     bool_output_mute=options.bool_output_mute,
    #     bool_output_html=options.bool_output_html,
    #     bool_output_json=options.bool_output_json,
    #     bool_print_test_case=options.printTestCase,
    #     question_to_grade=options.gradeQuestion,
    #     graphics=getDisplay(options.gradeQuestion != None, options)
    # )
