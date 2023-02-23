"""
Date created: 2/16/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Contributors:
    https://github.com/josephedradan

Reference:

"""
from enum import Enum


class EnumPlayer(Enum):

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        return False
