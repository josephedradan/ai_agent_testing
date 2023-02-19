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
from common import util
from pacman.feature_extractor_coordiate.feature_extrator import FeatureExtractor


class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[(state, action)] = 1.0
        return feats

