# parser.py
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


import re
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Union


class ParseFile():

    def __init__(self, path_file_test):
        # save the path_file_test to the test file
        self.path_file_test = path_file_test

    @staticmethod
    def get_str_no_comments(list_str: List[str]) -> str:
        # remove any portion of a line following a '#' symbol
        list_str_new: List[str] = []

        line: str
        for line in list_str:
            index = line.find('#')  # Find index of "#" in string
            if index == -1:
                list_str_new.append(line)
            else:
                list_str_new.append(line[0:index])

        return '\n'.join(list_str_new)

    def get_dict(self) -> Dict[str, Any]:
        """
        Read in the test case and remove comments

        :return:
        """
        test = {}
        with open(self.path_file_test) as file:
            list_str = file.read().split("\n")

        str_file = self.get_str_no_comments(list_str)

        test['__raw_lines__'] = list_str
        test['path_file_test'] = self.path_file_test
        test['__emit__'] = []
        lines = str_file.split('\n')

        i = 0
        # read a property in each loop cycle
        while (i < len(lines)):
            # skip blank lines
            if re.match('\A\s*\Z', lines[i]):
                test['__emit__'].append(("raw", list_str[i]))
                i += 1
                continue
            match_ = re.match('\A([^"]*?):\s*"([^"]*)"\s*\Z', lines[i])
            if match_:
                test[match_.group(1)] = match_.group(2)
                test['__emit__'].append(("oneline", match_.group(1)))
                i += 1
                continue
            match_ = re.match('\A([^"]*?):\s*"""\s*\Z', lines[i])
            if match_:
                msg = []
                i += 1
                while (not re.match('\A\s*"""\s*\Z', lines[i])):
                    msg.append(list_str[i])
                    i += 1
                test[match_.group(1)] = '\n'.join(msg)
                test['__emit__'].append(("multiline", match_.group(1)))
                i += 1
                continue

            raise Exception("Error parsing test file: {}".format(self.path_file_test))
        return test


def get_dict_kwargs(string_given: Union[str, None]) -> Dict[str, Any]:
    if string_given is None:
        return {}

    list_string: List[str] = string_given.split(',')
    kwargs = {}

    for string in list_string:
        if '=' in string:
            key, val = string.split('=')
        else:
            key, val = string, 1

        kwargs[key] = val
    return kwargs

# TODO: JOSEPH NOT USED
# def emitTestDict(dict_file_test, handle):
#     for kind, data in dict_file_test['__emit__']:
#         if kind == "raw":
#             handle.write(data + "\n")
#         elif kind == "oneline":
#             handle.write('%s: "%s"\n' % (data, dict_file_test[data]))
#         elif kind == "multiline":
#             handle.write('%s: """\n%s\n"""\n' % (data, dict_file_test[data]))
#         else:
#             raise Exception("Bad __emit__")
