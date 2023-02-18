"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/16/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from enum import Enum


class TypePlayer(Enum):

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        return False
