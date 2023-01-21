# featureExtractors.py
# --------------------
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

"Feature extractors for Pacman game states"


# class FeatureExtractor(ABC):
#     def getFeatures(self, state, action):
#         """
#           Returns a dict from features to counts
#           Usually, the count will just be 1.0 for
#           indicator functions.
#         """
#         pass
#
#
# class IdentityExtractor(FeatureExtractor):
#     def getFeatures(self, state, action):
#         feats = util.Counter()
#         feats[(state, action)] = 1.0
#         return feats
#
#
