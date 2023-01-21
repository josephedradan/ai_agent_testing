"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/21/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from common import util
from pacman.agent import PacmanQAgent
from pacman.feature_extractor_coordiate import FeatureExtractor
from pacman.feature_extractor_coordiate import get_subclass_feature_extractor


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """

    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor: FeatureExtractor = get_subclass_feature_extractor(extractor)()

        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self) -> util.Counter:
        return self.weights

    def getQValue(self, state, action) -> float:
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        r"""
        Question 10 (3 points): Approximate Q-Learning

        Notes:

        Execution:
            py -3.6 pacman.py -p ApproximateQAgent -x 2000 -n 2010 -l smallGrid 
            py -3.6 pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumGrid 
            py -3.6 pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic 
            py -3.6 autograder.py -q q10

        Results:
            *** PASS: test_cases\q10\1-tinygrid.test
            *** PASS: test_cases\q10\2-tinygrid-noisy.test
            *** PASS: test_cases\q10\3-bridge.test
            *** PASS: test_cases\q10\4-discountgrid.test
            *** PASS: test_cases\q10\5-coord-extractor.test

            ### Question q10: 3/3 ###


            Finished at 1:22:22

            Provisional grades
            ==================
            Question q10: 3/3
            ------------------
            Total: 3/3

        """

        """

        Notes:
            Q(s,a) = summation from 1 to n of f_i(s,a)*(w_i)  # Note: * = dot product     
        """

        # print("self.getWeights()", self.getWeights())
        # print("self.featExtractor.getFeatures(state, action)", self.featExtractor.getFeatures(state, action))

        dict_k_feature_v_feature_value: dict = self.featExtractor.getFeatures(state, action)

        summation = 0

        for feature, feature_value in dict_k_feature_v_feature_value.items():
            # summation += f_i(s,a) * (w_i)
            summation += feature_value * self.weights.get(feature, 0)

        return summation

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """

        Notes:
            Similar to:
                Q^new(s_t, a_t) = Q^old(s_t, a_t) + alpha * TD(s_t, a_t)
                TD(s_t, a_t) = r_t + (gamma * max_a Q(s_t+1, a)) - Q(s_t, a_t)

                Q^new(s_t, a_t) = Q^old(s_t, a_t) + alpha * (r_t + (gamma * max_a Q(s_t+1, a)) - Q^old(s_t, a_t))   

            What we are given:
                w_i <- w_i + (alpha * TD(s_t, a_t) * f_i(s,a))
                TD(s,a) = r + (gamma * max_a Q(s', a')) - Q(s,a)
                TD(s,a) = (r + (gamma * max_a Q(s', a'))) - Q(s,a)
                TD(s,a) = ((r + (gamma * max_a Q(s', a'))) - Q(s,a))

                w_i <- w_i + (alpha * ((r_t + (gamma * max_a Q(s', a'))) - Q(s,a)) * f_i(s,a))

                OR

                TD(s,a) = r + (gamma * max_a Q(s', a')) - Q(s,a)
                w_i = w_i + (alpha * TD(s,a) * f_i(s,a))

        """
        dict_k_feature_v_feature_value: dict = self.featExtractor.getFeatures(state, action)

        # max_a Q(s', a'))
        q_state_current_max = self.computeValueFromQValues(nextState)

        # gamma
        gamma = self.discount

        # Q(s,a)
        q_state_previous = self.getQValue(state, action)

        #####

        # TD(s,a) = r + (gamma * max_a Q(s',a')) - Q(s,a)
        temporal_difference = reward + (gamma * q_state_current_max) - q_state_previous

        # w_i <- w_i + (alpha * (TD(s,a)) * f_i(s,a))
        for feature, feature_value in dict_k_feature_v_feature_value.items():
            # w_i old
            w_i_old = self.weights.get(feature, 0)

            # w_i = w_i + (alpha * TD(s,a) * f_i(s,a))
            self.weights[feature] = w_i_old + (self.alpha * temporal_difference * feature_value)

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            # pprint(self.weights)
            pass
