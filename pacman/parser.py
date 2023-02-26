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
import ast
import re
from typing import Any
from typing import Dict
from typing import Hashable
from typing import List
from typing import Tuple
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


class ContainerObjectConstruct:

    def __init__(self,
                 name_class: str,
                 arguments: List[Any],
                 keyword_arguments: Dict[Hashable, Any]):
        self.name_class = name_class
        self.arguments = arguments
        self.keyword_arguments = keyword_arguments

    def __repr__(self):
        return "{}({})".format(
            self.name_class,
            ", ".join([
                *[str(arg) for arg in self.arguments],
                *["{}={}".format(k, v) for k, v in self.keyword_arguments.items()]
            ])
        )


TYPE_RETURNED = Union[int, float, str,
                      Dict[Hashable, "TYPE_RETURNED"],
                      List["TYPE_RETURNED"],
                      Tuple["TYPE_RETURNED", ...]
]


def _get_value_representation_of_ast_node(node: ast.AST) -> TYPE_RETURNED:
    """
    Get the literal value of a ast node. Only a subset of ast node types are allowed to checked
    to prevent arbitrary code execution.

    Notes:
        This does not use ast.unparse(...) because it will return the string representation of the node's value
        and not that the literal value with its corresponding correct type


    :param node:
    :return:
    """
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Tuple):
        return tuple((_get_value_representation_of_ast_node(elt) for elt in node.elts))
    elif isinstance(node, ast.List):
        return [_get_value_representation_of_ast_node(elt) for elt in node.elts]
    elif isinstance(node, ast.Dict):
        return {_get_value_representation_of_ast_node(key): _get_value_representation_of_ast_node(value)
                for key, value in zip(node.keys, node.values)}

    raise Exception("Prohibited arg/kwarg of type {} with value {} found "
                    "this type is banned to prevent potential arbitrary code "
                    "execution.".format(type(node), ast.unparse(node)))


def get_list_container_object_construct_from_str(str_object_construction: str) -> List[ContainerObjectConstruct]:
    """
    Get a list of objects that contains a class name, its args, and its kwargs that are required
    to make a instance of the class name

    FIXME: THE BELOW IS A TESTING STRING
    code = '''
    [Bob('sdfsdf',x=23),Bob('sdfsdf', 'AAAA',
    \"BBBB\",
    'dude = 44',x=23),
    Bob('sdfsdf',x=23.2, man='cool'),
    Person( {"Hello": 123} ,joseph, 'school="None"', "car='Cool'", name="bob", quote="Fake kwarg age=24",
    age=21, a=b, d=2323,
    random_dict = {"World": {1: {"lol": "Cool Man"}}}
    )
    ]'''

    :param str_object_construction:
    :return:
    """
    ##
    """
    Old regex that parses Class name and its kwargs + args, but parsing args from kwargs is very complex
    due to string arguments looking like keyword arguments even though those string arguments should not be
    keyword arguments.

    Example:
        Person('school="None"', "car='Cool'",
                name="bob", quote="Fake kwarg age=24",
                age=21
                )

    The example above is hard to parse args and kwargs correctly plus there are newlines, spaces, and tabs that
    need to be accounted for
    """
    # pattern_class_instantiation_ = re.compile(r"(\b\w+)\((.*?)\)")
    # list_class_instantiation = re.findall(pattern_class_instantiation_, str_object_construction)

    str_object_construction = str_object_construction.strip()  # Clean up unnecessary spacing

    ast_parse = ast.parse(str_object_construction)

    list_ast_object = [ast_object for ast_object in ast.walk(ast_parse) if isinstance(ast_object, ast.Call)]

    list_container_object_construct: List[ContainerObjectConstruct] = []

    for ast_object in list_ast_object:
        name_class: str = ast_object.func.id

        args: List[Any] = [_get_value_representation_of_ast_node(arg) for arg in ast_object.args]

        # The below will make everything into strings
        # kwargs: Dict[Hashable, Any] = {
        #     keyword_arg.arg: ast.unparse(keyword_arg.value)
        #     for keyword_arg in ast_object.keywords
        # }

        kwargs: Dict[Hashable, Any] = {
            keyword_arg.arg: _get_value_representation_of_ast_node(keyword_arg.value)
            for keyword_arg in ast_object.keywords
        }

        # print("Name Class:", name_class)
        # print("args:", args)
        # print("kwargs:", kwargs)
        # for i in kwargs.values():
        #     print(type(i))
        # print()

        list_container_object_construct.append(ContainerObjectConstruct(name_class, args, kwargs))

    return list_container_object_construct


def get_list_container_object_construct_from_implicit(
        name_class: str,
        str_args_kwargs: str,
        amount_to_create: int) -> List[ContainerObjectConstruct]:
    """

    :param name_class:
    :param str_args_kwargs:
    :param amount_to_create:
    :return:
    """
    _str_agent = str(name_class)

    args, kwargs = get_tuple__args__kwargs___from_str(str_args_kwargs)
    _list_list_container_object_construct = (
        [ContainerObjectConstruct(name_class, args, kwargs) for _ in range(amount_to_create)]
    )

    return _list_list_container_object_construct


def get_list_container_object_construct_from_space_separated(
        name_class_space_separated: str,
        str_args_kwargs_space_separated: str) -> List[ContainerObjectConstruct]:
    """

    :param name_class_space_separated:
    :param str_args_kwargs_space_separated:
    :return:
    """
    # Example: "AgentKeyboard AgentKeyboard AgentKeyboard"
    _list_str_agent = name_class_space_separated.split(" ")

    # Example: "name=Bob,age=21 name=Steve,age=22"
    _list_str_agent_args_kwargs = str_args_kwargs_space_separated.split(" ")

    _list_tuple__args__kwargs___from_str: List[Tuple[List, Dict[Hashable, Any]]] = (
        [get_tuple__args__kwargs___from_str(_kwargs) for _kwargs in _list_str_agent_args_kwargs]
    )

    _list_list_container_object_construct = [
        ContainerObjectConstruct(name_class, arguments, keyword_arguments)
        for name_class, arguments, keyword_arguments in
        zip(_list_str_agent, *_list_tuple__args__kwargs___from_str)
    ]

    return _list_list_container_object_construct


def get_tuple__args__kwargs___from_str(string_given: Union[str, None]) -> Tuple[List, Dict[Hashable, Any]]:
    """
    Get a tuple containing args and kwargs parsed from a string

    :param string_given:
    :return:
    """
    # if string_given is None:
    #     return {}
    #
    # list_string: List[str] = string_given.split(',')
    # kwargs = {}
    #
    # for string in list_string:
    #     if '=' in string:
    #         key, val = string.split('=')
    #     else:
    #         key, val = string, 1
    #
    #     kwargs[key] = val

    _str_parsable_fake = "_({})".format(string_given)

    list_container_object_construct = get_list_container_object_construct_from_str(_str_parsable_fake)

    _container_object_construct = list_container_object_construct[0]

    return _container_object_construct.arguments, _container_object_construct.keyword_arguments


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

if __name__ == '__main__':
    code = '''
    [Bob('sdfsdf',x=23),Bob('sdfsdf', 'AAAA',
    \"BBBB\",
    'dude = 44',x=23),
    Bob('sdfsdf',x=23.2, man='cool'),
    Person( {"Hello": 123} ,joseph, 'school="None"', "car='Cool'", name="bob", quote="Fake kwarg age=24", 
    age=21, a=b, d=2323,
    random_dict = {"World": {1: {"lol": "Cool Man"}}}
    )
    ]'''
    print(get_list_container_object_construct_from_str(code))
