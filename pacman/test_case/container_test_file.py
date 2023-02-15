"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/18/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import Any
from typing import Dict
from typing import Union


class ContainerFileTest:

    def __init__(self, dict_file_test: Dict[str, Any]):
        self.dict_file_test: Dict[str, Any] = dict_file_test

        self.path_file_test: str = dict_file_test.get('path_file_test')

        #####

        self.str_layout: Union[str, None] = dict_file_test.get('layout_text')

        self.name_layout: Union[str, None] = dict_file_test.get('layout_name')

        ##### EpsilonGreedyTest

    def __getitem__(self, item):
        return self.dict_file_test[item]