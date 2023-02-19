# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


# import mdp
from collections import defaultdict
from typing import Union, Tuple



# import collections
from gridworld.main_grid_world import Gridworld
from common import util
from pacman.agent.agent_value_estimation import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration player should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp: Gridworld = mdp
        self.discount: float = discount
        self.iterations: int = iterations
        self.values: util.Counter = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()
        # print("self.values")
        # pprint(self.values)

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"


        r"""
        Question 1 (4 points): Value Iteration

        MDP 
        
        Execution:
            python gridworld.py -a value -i 100 -ng 10
            python gridworld.py -a value -i 5
            python autograder.py -q q1

            py -3.6 gridworld.py -a value -i 100 -ng 10
            py -3.6 gridworld.py -a value -i 5
            py -3.6 autograder.py -q q1
        
        Results:
            *** PASS: test_cases\q1\1-tinygrid.test
            *** PASS: test_cases\q1\2-tinygrid-noisy.test
            *** PASS: test_cases\q1\3-bridge.test
            *** PASS: test_cases\q1\4-discountgrid.test
            
            ### Question q1: 4/4 ###
            
            
            Finished at 22:02:35
            
            Provisional grades
            ==================
            Question q1: 4/4
            ------------------
            Total: 4/4
            
        Contributors: 
    https://github.com/josephedradan

Reference:
            COMPSCI 188 - 2018-09-18
                Notes:
                    
                    Optimal Quantities
                        V =     Value
                        V* =    Optimal Value (Value you achieve on average if you start on state s)
                                * It is the value of being in a state and acting optimally    
                        
                        V_k =   ** Optimal value of a state and play optimally.
                                ** It is the expected value of starting in that state and playing optimally if the
                                game is going to end in k more time steps (Makes the tree not inf)
                                If you save repeatedly you have an even better algo
                        
                        Q =     Q State (chance node), there are good and bad ones
                                Their values have to do with what happens from that Q state you act optimally 
                                in the future
                        
                        Q* =    Optimal Q State (Best state)
                        
                        s =     state
                        a =     action
                        s' =    state_future
                        
                    # computeQValueFromValues
                    Q*(s, a) = Summation from 0 to s' of T(s, a, s') * (R(s, a, s') + gamma * V*(s'))
                    
                    # The value of computeActionFromValues (computeActionFromValues returns an action)
                    V*(s) = max_a Q*(s, a)
                    V*(s) = max_a Summation from 0 to s' of T(s, a, s') * (R(s, a, s') + gamma * V*(s'))
                    
                    # Almost looks like the bellman equations
                    V_k+1(s) = max_a Summation from 0 to s' of (T(s, a, s')[R(s, a, s') + gamma * V_k(s')])
                                        
                    Space Complexity:
                        S^2 * A
                            1. Visit each S, 
                            2. For each S you do Expectimax which is (max Summation from 0 to s') as you
                            consider each action which is A
                            3. Foe each action you need to consider every possible state that results which is S
                    
                    **  Remember you only get score if you transition to the state from another state
                    
                Contributors: 
    https://github.com/josephedradan

Reference:
                    https://www.youtube.com/watch?v=4LW3H_Jinr4&list=PLsOUugYMBBJENfZ3XAToMsg44W7LeUVhF&index=9
        
        """

        for i in range(self.iterations):

            """
            Notes:
                Use the "batch" version of value iteration where each vector Vk is computed from a fixed vector Vk-1 
                (like in lecture), not the "online" version where one single weight vector is updated in place. This
                means that when a state's value is updated in iteration k based on the values of its successor states,
                the successor state values used in the value update computation should be those from iteration k-1 
                (even if some of the successor states had already been updated in iteration k).
                
                    Must copy counter because autograder will check during iteration.
                    Basically copy the counter (self.values)
            """

            # This is the "batch" version
            counter_temp = self.values.copy()

            state: Tuple[int, int]
            for state in self.mdp.getStates():

                if self.mdp.isTerminal(state):
                    continue

                actions_possible = self.mdp.getPossibleActions(state)

                """
                It is the expected value of starting in that state and playing optimally 
                if the game is going to end in k steps
                """
                v_star = max([self.computeQValueFromValues(state, action) for action in actions_possible])

                counter_temp[state] = v_star

            self.values = counter_temp

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action) -> float:
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """
        Solve for Q* then return Q*
        
        Notes:
            Bellman equation
            
            Q*(s, a) = Summation from 0 to s' of T(s, a, s') * (R(s, a, s') + gamma * V*(s'))
                                
            1. summation_of_expected_value = 0
            2. Solve for reward                     Equation: R(s, a, s')
            3. Solve for value Utility * gamma      Equation: gamma * V*(s')
            4. Solve for probability                Equation: T(s, a, s') or P(s'|s,a)
            5. Solve for Summation from to s' of T(s, a, s') * (R(s, a, s') + gamma * V*(s'))
            6. Return the Summation from step 5
            
        Contributors: 
    https://github.com/josephedradan

Reference:
            Lecture 8: Markov Decision Processes (MDPs)
                Contributors: 
    https://github.com/josephedradan

Reference:
                    https://youtu.be/i0o-ui1N35U?t=3136

            COMPSCI 188 - 2018-09-18
                Notes:
                
                    Why is Gamma exponential?
                        When you talk about sequences being converted into a single number, you use exponentiation 
                        because it's mathematically very convenient, it reflects real world things like interest in 
                        money and it has something to do with stationary preferences which only holds for the 
                        exponential case
                    
                Contributors: 
    https://github.com/josephedradan

Reference:
                    https://www.youtube.com/watch?v=4LW3H_Jinr4&list=PLsOUugYMBBJENfZ3XAToMsg44W7LeUVhF&index=9
            
            What do Reinforcement Learning Algorithms Learn - Optimal Policies
                Notes:
                    Optimal state-value function
                        V* gives the largest expected return achievable by any policy pi for each state.
                    
                    Optimal action-value function
                        Q* gives the largest expected return achievable by any policy pi for each possible 
                        state-action pair
                    
                    Bellman Optimality equation for q*
                        Q* (s, a) = E*[R_t+1 + gamma*max Q*(s', a')]
                    
                    
                Contributors: 
    https://github.com/josephedradan

Reference:
                    https://www.youtube.com/watch?v=rP4oEpQbDm4&list=PLZbbT5o_s2xoWNVdDudn51XM8lOuZ_Njv&index=5
            
            Foundations of Q-Learning
                Notes:
                    Q-value indicate the quality of a particular action a in a given state s Q(s, a)
                    Q-value are our current estimate of the sum of future rewards
                        Q-values estimate how much additional reward we can accumulate through
                        all remaining steps in the current episode if the AI player is in state s and takes action a
                        Q values therefore increase as the AI player gets closer and closer to the highest reward
                    
                    Q-values are stored in a Q-table, which has one row for each possible state, and one
                    column for each possible action
                        An optimal Q-table contains values that allow the AI player to take the best action
                        in any possible state, thus providing the player with the optimal path to the highest reward'
                        *The Q-table therefore represents the AI player's policy for acting in the current environment
                    
                Contributors: 
    https://github.com/josephedradan

Reference:
                    https://www.youtube.com/watch?v=__t2XRxXGxI

        """

        # print(self.computeQValueFromValues.__name__)
        # print("State: {}\nAction: {}".format(state, action))
        # print()

        # Q*
        summation_of_expected_value = 0

        for state_possible, probability in self.mdp.getTransitionStatesAndProbs(state, action):
            # R(s, a, s')
            reward = self.mdp.getReward(state, action, state_possible)

            # gamma * V*(s')
            utility_best_times_gamma = self.discount * self.getValue(state_possible)

            # P(s'|s,a)  # Probably of s' given s, a  # Probably is also known as the weighted sum
            expected_value = probability * (reward + utility_best_times_gamma)

            summation_of_expected_value += expected_value

        # Return Q*
        return summation_of_expected_value

    def computeActionFromValues(self, state: tuple) -> Union[None, str]:
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # print(type(self.mdp))
        # print(type(self.discount))
        # print(type(self.iterations))
        # print(type(self.values))
        """
        Contributors: 
    https://github.com/josephedradan

Reference:
            COMPSCI 188 - 2018-09-18
                Notes:
                    *** THIS IS A POLICY (GIVE A STATE, GET AN ACTION)*** 

                    pi* == optimal policy
                    Policy: Committed to an action, but not resulted is called a Q state
                    
                    Defining MDPs
                        Markov Decision Processes:
                            s           Set of states
                            s_0         State start
                            A           Set of actions
                            
                            Transitions P(s'|s,a) or (T(s,a,s'))
                        
                        
                        MDP Quantities so far:
                            Policy = Choice of action for each state
                            Utility = Sum of (discounted) rewards
                   
                    Optimal Quantities
                        V =     Value
                        V* =    Optimal Value (Value you achieve on average if you start on state s)
                                * It is the value of being in a state and acting optimally    
                        
                        V_k =   ** Optimal value of a state and play optimally.
                                ** It is the expected value of starting in that state and playing optimally if the
                                game is going to end in k more time steps (Makes the tree not inf)
                                If you save repeatedly you have an even better algo
                        
                        Q =     Q State (chance node), there are good and bad ones
                                Their values have to do with what happens from that Q state you act optimally 
                                in the future
                        
                        Q* =    Optimal Q State (Best state)
                        
                        pi*(s) = Optimal action from State s (Example: In this state, go north)

                    Racing Search Tree
                        Too much work for expectimax
                        Problem state are repeated (You can cache it)
                        Tree goes forever (You can truncate the tree at level 100)
                        
                        * If you cache and do truncate you just made value iteration
                        *** What we need to do is start bottom to teh top
                        Use V_k
                        
                Contributors: 
    https://github.com/josephedradan

Reference:
                    https://www.youtube.com/watch?v=4LW3H_Jinr4&list=PLsOUugYMBBJENfZ3XAToMsg44W7LeUVhF&index=9
            
            COMPSCI 188 - 2018-09-20
                Notes:
                    Policy = map of states to actions
                    Utility = sum of discounted rewards
                    Values = expected future utility from a state (max node)
                    Q-Values = expected future utility from a q-state (change node)
                    
                Rerference:
                    https://www.youtube.com/watch?v=ZToWj64rxvQ&list=PLsOUugYMBBJENfZ3XAToMsg44W7LeUVhF&index=10

        """

        """
        This function is a policy
        
        Solve for Max Q* then return it
        
        Notes:
            1. Solve for all Q*
            2. Solve max of all Q* (Solve for V*)
            3. return Max V*'s return action from v*
            
        """

        # # Unnecessary check, use it runValueIteration instead
        # if self.mdp.isTerminal(state):
        #     return None

        # Dict of all key action and value Q*
        counter_k_action_v_q_star = util.Counter()

        for action in self.mdp.getPossibleActions(state):
            # Q* State
            q_star = self.computeQValueFromValues(state, action)

            # print(f"{action:<5} q_star:", q_star)

            counter_k_action_v_q_star[action] = q_star

        # print("counter_k_action_v_q_star.argMax()", counter_k_action_v_q_star.argMax())
        # print()

        # Return V*'s action (So this function is a policy since you give this function an state and you get an action)
        return counter_k_action_v_q_star.argMax()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=1000):
        """
          Your cyclic value iteration player should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        r"""
        Question 4 (Not Required): Asynchronous Value Iteration

        Execution:
            python gridworld.py -a asynchvalue -i 1000 -ng 10
            python autograder.py -q q4

            py -3.6 gridworld.py -a asynchvalue -i 1000 -ng 10
            py -3.6 autograder.py -q q4
        

        Notes:
            The reason this class is called AsynchronousValueIterationAgent is because we will update 
            only one state in each iteration, as opposed to doing a batch-style update. Here is how 
            cyclic value iteration works. In the first iteration, only update the value of the first 
            state in the states list. In the second iteration, only update the value of the second. 
            Keep going until you have updated the value of each state once, then start back at the 
            first state for the subsequent iteration. If the state picked for updating is terminal, 
            nothing happens in that iteration. You can implement it as indexing into the states 
            variable defined in the code skeleton.

                1.  In the first iteration, only update the value of the first state in the states list
                2.  In the second iteration, only update the value of the second state in the states list
                3.  Keep going until you have updated the value of each state once, then start 
                    back at the first state for the subsequent iteration
                4.  If the state picked for updating is terminal, nothing happens in that iteration
                
        Results:
            *** PASS: test_cases\q4\1-tinygrid.test
            *** PASS: test_cases\q4\2-tinygrid-noisy.test
            *** PASS: test_cases\q4\3-bridge.test
            *** PASS: test_cases\q4\4-discountgrid.test
            
            ### Question q4: 1/1 ###
            
            
            Finished at 21:57:38
            
            Provisional grades
            ==================
            Question q4: 1/1
            ------------------
            Total: 1/1
        """

        for index_iteration in range(self.iterations):

            list_state: list = self.mdp.getStates()

            # Cycle state based on the iteration
            state = list_state[index_iteration % len(list_state)]

            if self.mdp.isTerminal(state):
                continue

            actions_possible = self.mdp.getPossibleActions(state)

            """
            It is the expected value of starting in that state and playing optimally 
            if the game is going to end in k steps
            """
            v_star = max([self.computeQValueFromValues(state, action) for action in actions_possible])

            self.values[state] = v_star


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """

    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
          Your prioritized sweeping value iteration player should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        r"""
        Question 5 (Not Required): Prioritized Sweeping Value Iteration

        Execution:
            python gridworld.py -a asynchvalue -i 1000 -ng 10
            python autograder.py -q q4

            py -3.6 gridworld.py -a asynchvalue -i 1000 -ng 10
            py -3.6 autograder.py -q q4

        Notes:
        
        Result:
            
            *** PASS: test_cases\q5\1-tinygrid.test
            *** PASS: test_cases\q5\2-tinygrid-noisy.test
            *** PASS: test_cases\q5\3-bridge.test
            *** PASS: test_cases\q5\4-discountgrid.test
            
            ### Question q5: 3/3 ###
            
            
            Finished at 21:57:15
            
            Provisional grades
            ==================
            Question q5: 3/3
            ------------------
            Total: 3/3
        """

        # print("self.values", self.values)

        """
        1. Compute predecessors of all states.

        Notes:
            When you compute predecessors of a state, make sure to store them in a set, not a list,
            to avoid duplicates.
        """
        dict_k_state_v_set_predecessor = defaultdict(set)

        """
        2. Initialize an empty priority queue.

        Notes:
            Please use util.PriorityQueue in your implementation. The update method in this class will
            likely be useful; look at its documentation.
        """
        pq = util.PriorityQueue()

        """
        3. For each non-terminal state s, do:
        (note: to make the autograder work for this question, you must iterate over states in the order returned 
        by self.mdp.getStates())
        """
        for state in self.mdp.getStates():

            # Auto skip if terminal
            if self.mdp.isTerminal(state):
                continue

            # 1a. current value of s in self.values
            state_current_value = self.values.get(state, 0)  # 0 if the value does not exist

            ##########

            """
            computeActionFromValues

            Notes:
                Custom computeActionFromValues
                Need this to have access to specific scopes
                    used for dict_k_state_v_set_predecessor[state_possible].add(state)
            """

            list_q_star = []

            for action in self.mdp.getPossibleActions(state):

                ##########
                """
                computeQValueFromValues
                """

                summation_of_expected_value = 0

                for state_possible, probability in self.mdp.getTransitionStatesAndProbs(state, action):
                    # R(s, a, s')
                    reward = self.mdp.getReward(state, action, state_possible)

                    # gamma * V*(s')
                    utility_best_times_gamma = self.discount * self.getValue(state_possible)

                    # P(s'|s,a)  # Probably of s' given s, a  # Probably is also known as the weighted sum
                    expected_value = probability * (reward + utility_best_times_gamma)

                    summation_of_expected_value += expected_value

                    #####

                    """
                    From this loop, we have the parent and so we can get the children.
                    Now we can use the dict where
                        key == state_possible   # State (not to be confused with state)
                        value == state          # Predecessor (state is the parent which is the predecessor)
                    """
                    dict_k_state_v_set_predecessor[state_possible].add(state)

                ##########

                # Q* State
                q_star = summation_of_expected_value

                list_q_star.append(q_star)

                #####

            """
            It is the expected value of starting in that state and playing optimally
            if the game is going to end in k steps

            1b. highest Q-value across all possible actions from s (this represents what the value should be)
            """

            # pprint(dict_k_state_v_set_predecessor)

            v_star_max = max(list_q_star)

            ##########

            """
            1. Find the absolute value of the difference between the current value of s in self.values and the highest
            Q-value across all possible actions from s (this represents what the value should be); call this number
            diff. Do NOT update self.values[s] in this step.
            """

            diff = abs(state_current_value - v_star_max)

            """
            2. Push s into the priority queue with priority -diff (note that this is negative). We use a negative
            because the priority queue is a min heap, but we want to prioritize updating states that have a
            higher error.
            """
            pq.push(state, -1 * diff)

        # 4. For index_iteration in (0, 1, 2, ..., self.iterations - 1), do:
        for index_iteration in range(self.iterations):

            # 1. If the priority queue is empty, then terminate.
            if pq.isEmpty():
                return

            # 2. Pop a state s off the priority queue.
            state_popped = pq.pop()

            list_actions_possible_state_popped = self.mdp.getPossibleActions(state_popped)

            # 3. Update s's value (if it is not a terminal state) in self.values.
            if not self.mdp.isTerminal(state_popped):
                v_star_max = max(
                    [self.computeQValueFromValues(state_popped,
                                                  action) for action in list_actions_possible_state_popped]
                )
                self.values[state_popped] = v_star_max

            # 4. For each predecessor p of s, do:
            for state_predecessor in dict_k_state_v_set_predecessor.get(state_popped):

                # 1a. current value of p in self.values
                state_predecessor_value = self.values.get(state_predecessor, 0)  # 0 if the value does not exist

                list_actions_possible_state_predecessor = self.mdp.getPossibleActions(state_predecessor)

                # 1b. highest Q-value across all possible actions from p
                v_star_state_predecessor = max(
                    [self.computeQValueFromValues(state_predecessor,
                                                  action) for action in list_actions_possible_state_predecessor]
                )

                """
                1. Find the absolute value of the difference between the current value of p in self.values and the
                highest Q-value across all possible actions from p (this represents what the value should be); call
                this number diff. Do NOT update self.values[p] in this step.
                """
                diff = abs(state_predecessor_value - v_star_state_predecessor)

                """
                2. If diff > theta, push p into the priority queue with priority -diff (note that this is negative),
                as long as it does not already exist in the priority queue with equal or lower priority. As before,
                we use a negative because the priority queue is a min heap, but we want to prioritize updating states
                that have a higher error.

                Notes:
                    Please use util.PriorityQueue in your implementation. The update method in this class will
                    likely be useful; look at its documentation.
                """
                if diff > self.theta:
                    pq.update(state_predecessor, -1 * diff)
