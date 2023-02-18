"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/19/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import Callable
from typing import Tuple

from common.grader import Grader

TYPE_CALLABLE_THAT_NEEDS_GRADER = Callable[[Grader], bool]


TYPE_VECTOR = Tuple[float,...]