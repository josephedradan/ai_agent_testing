# qlearningAgents.py
# ------------------
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
import random
from typing import Tuple, Union

from common import util
from pacman.agent.agent_value_estimation_reinforcement import ReinforcementAgent
from pacman.feature_extractor_coordiate import FeatureExtractor
from pacman.feature_extractor_coordiate import get_subclass_feature_extractor


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """

    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        r"""
        Question 6 (4 points): Q-Learning

        Execution:
            py -3.6 gridworld.py -a q -k 5 -m
            py -3.6 autograder.py -q q6
        
        Result:
            *** PASS: test_cases\q6\1-tinygrid.test
            *** PASS: test_cases\q6\2-tinygrid-noisy.test
            *** PASS: test_cases\q6\3-bridge.test
            *** PASS: test_cases\q6\4-discountgrid.test
            
            ### Question q6: 4/4 ###
            
            
            Finished at 21:55:45
            
            Provisional grades
            ==================
            Question q6: 4/4
            ------------------
            Total: 4/4
        """

        """
        Reference:
            Foundations of Q-Learning
                Notes:
                    Q-values are stored in a Q-table which has one row for each
                    possible state and one column for each possible action
                    
                    An optimal Q-table contains values that allow the AI agent to take the best
                    action in any possible state, thus providing the agent with the optimal path to the
                    highest reward
                    
                    The Q-table therefore represents the AI agent's policy for acting in the current 
                    environment
                    
                Reference:
                    https://youtu.be/__t2XRxXGxI?t=597
                    https://youtu.be/__t2XRxXGxI?t=757
        """

        # A Counter is a dict with default 0
        self.counter_q_table_k_state_action_v_value: util.Counter = util.Counter()

    def getQValue(self, state: Tuple[int, int], action: str) -> float:
        """
          Returns Q(state,action)
              Should return 0.0 if we have never seen a state
              or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        return self.counter_q_table_k_state_action_v_value.get((state, action), 0)

    def computeValueFromQValues(self, state: Tuple[int, int]) -> float:
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """
        Important: Make sure that in your computeValueFromQValues and computeActionFromQValues functions, you only 
        access Q values by calling getQValue . This abstraction will be useful for question 10 when you override 
        getQValue to use features of state-action pairs rather than state-action pairs directly.
        """

        actions = self.getLegalActions(state)

        if actions:
            return max([self.getQValue(state, action) for action in actions])
        return 0

    def computeActionFromQValues(self, state) -> Union[None, str]:
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """
        Important: Make sure that in your computeValueFromQValues and computeActionFromQValues functions, you only 
        access Q values by calling getQValue . This abstraction will be useful for question 10 when you override 
        getQValue to use features of state-action pairs rather than state-action pairs directly.
        """
        actions = self.getLegalActions(state)

        if actions:
            return max([action for action in actions],
                       key=lambda _action: self.getQValue(state, _action))
        return None

    def getAction(self, state) -> str:
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)

        # action = None
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """
        Question 7 (2 points): Epsilon Greedy
        
        Execution:
            py -3.6 gridworld.py -a q -k 100 
            py -3.6 gridworld.py -a q -k 100 --noise 0.0 -e 0.1
            py -3.6 gridworld.py -a q -k 100 --noise 0.0 -e 0.9
            py -3.6 autograder.py -q q7
            
            py -3.6 crawler.py

        
        Notes:
            Complete your Q-learning agent by implementing epsilon-greedy action selection in getAction, meaning it 
            chooses random actions an epsilon fraction of the time, and follows its current best Q-values otherwise. 
            Note that choosing a random action may result in choosing the best action - that is, you should not 
            choose a random sub-optimal action, but rather any random legal action.
            
            You can choose an element from a list uniformly at random by calling the random.choice function. You 
            can simulate a binary variable with probability p of success by using util.flipCoin(p), which returns 
            True with probability p and False with probability 1-p.
            
        """

        """
        Flip a coin and only allow the random number generated if less than self.epsilon
        
        Reference:
            Exploration vs. Exploitation - Learning the Optimal Reinforcement Learning Policy

                Notes:
                    If epsilon low then you will most likely do Exploitation
                    If epsilon high then you will most likely do Exploration
                
                Reference:
                    https://youtu.be/mo96Nqlo1L8?list=PLZbbT5o_s2xoWNVdDudn51XM8lOuZ_Njv&t=32
        
        
        """
        boolean: bool = util.flipCoin(self.epsilon)

        action_from_policy = self.getPolicy(state)

        # set_legalAction = set(legalActions)
        #
        # if action_from_policy in set_legalAction:
        #     set_legalAction.remove(action_from_policy)
        #
        # print(legalActions)

        if boolean:
            # Exploration
            # return random.choice(list(set_legalAction))  # Will Fail q7, but it's a better solution kind of
            return random.choice(legalActions)

        # Exploitation
        return action_from_policy

    def update(self, state, action, nextState, reward) -> None:
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        """

        Reference:
            Foundations of Q-Learning
                Notes:
                    Temporal Differences
                        Notes:
                            method of calculating how much Q-value for the action taken in teh previous state
                            should be changed based on what teh AI agent has learned about the Q-value for the current
                            state's actions
                            
                            Previous Q-values are therefore updated after each step
                            
                        Equation:
                            TD(s_t, a_t) = r_t + (gamma * max_a Q(s_t+1, a)) - Q(s_t, a_t)
        
                            TD =    Temporal Difference for the action taken in the previous state 
                            r_t =   Reward received for the action taken in the previous state
                            gamma = Discount factor (between 0 and 1)
                            max_a Q(s_t+1, a) = The largest Q-value available for any action in the current state
                                                (the largest predicted sum of future rewards)    
                            Q =     Quality of state and action
                    
                    Bellman Equation
                        Notes:
                            Tells what new value to use as the Q-value for the action taken in the previous state
                            
                            Relies on both old Q-value for the action taken in the previous state and what has
                            been learned after moving to the next state.
                            
                            Includes a learning rate parameter (alpha) that defines how quickly Q-values are adjusted
                            invented by Richard Bellman                    
                        
                        Equation:
                            Q^new(s_t, a_t) = Q^old(s_t, a_t) + alpha * TD(s_t, a_t)
                            
                            Q^new = New Q-value for the action taken in the previous state
                            Q^old = The old Q-value for the action taken in the previous state
                            alpha = The learning rate (between 0 and 1)
                            TD =    Temporal Difference
                    
                    Full Equation:
                        Q^new(s_t, a_t) =  Q^old(s_t, a_t) + alpha * (r_t + (gamma * max_a Q(s_t+1, a)) - Q(s_t, a_t))
                        
                        Q^new(s_t, a_t) =  
                        Q^old(s_t, a_t) + alpha * (r_t + (gamma * max_a Q(s_t+1, a)) - Q^old(s_t, a_t))
                        
                Reference:
                    https://youtu.be/__t2XRxXGxI?t=597
                    https://youtu.be/__t2XRxXGxI?t=757
                    
        """

        # max_a Q(s_t+1, a)
        q_state_current_max = self.computeValueFromQValues(nextState)

        # gamma
        gamma = self.discount

        # Q^old(s_t, a_t)
        q_state_previous = self.getQValue(state, action)

        #####

        # TD(s_t, a_t) = r_t + (gamma * max_a Q(s_t+1, a)) - Q(s_t, a_t)
        temporal_difference = reward + (gamma * q_state_current_max) - q_state_previous

        # Bellman Equation
        # Q^new(s_t, a_t) =  Q^old(s_t, a_t) + alpha * TD(s_t, a_t)
        q_state_new = q_state_previous + self.alpha * temporal_difference

        self.counter_q_table_k_state_action_v_value[(state, action)] = q_state_new

    def getPolicy(self, state) -> Union[None, str]:
        return self.computeActionFromQValues(state)

    def getValue(self, state) -> float:
        return self.computeValueFromQValues(state)


"""
Question 9 (1 point): Q-Learning and Pacman

Notes:
    Pacman not good at medium sized grid
    
Execution:
    py -3.6 pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid

    # Watch Training games
    py -3.6 pacman.py -p PacmanQAgent -n 10 -l smallGrid -a numTraining=10
    
    py -3.6 autograder.py -q q9

Results:
    ### Question q9: 1/1 ###
    
    
    Finished at 1:20:43
    
    Provisional grades
    ==================
    Question q9: 1/1
    ------------------
    Total: 1/1

"""


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


