"""
Date created: 1/13/2023

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
from abc import ABC
from abc import abstractmethod

from common.state import State


class FeatureExtractor(ABC):

    @abstractmethod
    def getFeatures(self, state: State, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        pass
