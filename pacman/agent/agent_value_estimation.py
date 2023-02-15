"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/13/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from abc import abstractmethod

from pacman.agent import AgentPacman


class ValueEstimationAgent(AgentPacman):
    """
      Abstract player which assigns values to (state_pacman,action)
      Q-Values for an environment. As well as a value to a
      state_pacman and a policy given respectively by,

      V(s) = max_{a in actions} Q(s,a)
      policy(s) = arg_max_{a in actions} Q(s,a)

      Both ValueIterationAgent and QLearningAgent inherit
      from this player. While a ValueIterationAgent has
      a model of the environment via a MarkovDecisionProcess
      (see mdp.py) that is used to estimate Q-Values before
      ever actually acting, the QLearningAgent estimates
      Q-Values while acting in the environment.
    """

    def __init__(self, alpha=1.0, epsilon=0.05, gamma=0.8, num_training=10, **kwargs):
        super().__init__(**kwargs)
        """
        Sets options, which can be passed in via the Pacman command line using -a alpha=0.5,...
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        num_training - number of training episodes, i.e. no learning after these many episodes
        """
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.discount = float(gamma)
        self.num_training = int(num_training)

    ####################################
    #    Override These Functions      #
    ####################################
    @abstractmethod
    def getQValue(self, state, action):
        """
        Should return Q(state_pacman,action)
        """
        pass

    @abstractmethod
    def getValue(self, state):
        """
        What is the value of this state_pacman under the best action?
        Concretely, this is given by

        V(s) = max_{a in actions} Q(s,a)
        """
        pass

    @abstractmethod
    def getPolicy(self, state):
        """
        What is the best action to take in the state_pacman. Note that because
        we might want to explore, this might not coincide with getAction
        Concretely, this is given by

        policy(s) = arg_max_{a in actions} Q(s,a)

        If many actions achieve the maximal Q-value,
        it doesn't matter which is selected.
        """
        pass

    @abstractmethod
    def getAction(self, state):
        """
        state_pacman: can call state_pacman.getLegalActions()
        Choose an action and return it.
        """
        pass
