# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    r"""
    Question 2 (1 point): Bridge Crossing Analysis

    Execution:
        python autograder.py -q q2
        py -3.6 autograder.py -q q2

    Notes:
        You literally need to guess and check

    Results:

        *** PASS: test_cases\q2\1-bridge-grid.test

        ### Question q2: 1/1 ###


        Finished at 22:02:05

        Provisional grades
        ==================
        Question q2: 1/1
        ------------------
    """
    answerDiscount = 0.9

    # How often an agent ends up in an unintended successor state when they perform an action
    answerNoise = 0  # You want 0 because rng sucks
    return answerDiscount, answerNoise


def question3a():
    """
    Question 3 (5 points): Policies
    Prefer the close exit (+1), risking the cliff (-10)

    Execution:
        python autograder.py -q q3
        py -3.6 autograder.py -q q3

    Notes:
        You literally need to guess and check

    """

    answerDiscount = 0.1
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3b():
    """
    Question 3 (5 points): Policies
    Prefer the close exit (+1), but avoiding the cliff (-10)

    Execution:
        python autograder.py -q q3
        py -3.6 autograder.py -q q3

    Notes:
        You literally need to guess and check

    """

    answerDiscount = 0.1
    answerNoise = 0.1
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3c():
    """
    Question 3 (5 points): Policies
    Prefer the distant exit (+10), risking the cliff (-10)

    Execution:
        python autograder.py -q q3
        py -3.6 autograder.py -q q3

    Notes:
        You literally need to guess and check

    """
    answerDiscount = 0.9
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3d():
    """
    Question 3 (5 points): Policies
    Prefer the distant exit (+10), avoiding the cliff (-10)

    Execution:
        python autograder.py -q q3
        py -3.6 autograder.py -q q3

    Notes:
        You literally need to guess and check

    """
    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3e():
    r"""
    Question 3 (5 points): Policies
    Avoid both exits and the cliff (so an episode should never terminate)

    Execution:
        python autograder.py -q q3
        py -3.6 autograder.py -q q3

    Notes:
        You literally need to guess and check

    Results:
        *** PASS: test_cases\q3\1-question-3.1.test
        *** PASS: test_cases\q3\2-question-3.2.test
        *** PASS: test_cases\q3\3-question-3.3.test
        *** PASS: test_cases\q3\4-question-3.4.test
        *** PASS: test_cases\q3\5-question-3.5.test

        ### Question q3: 5/5 ###


        Finished at 22:01:11

        Provisional grades
        ==================
        Question q3: 5/5
        ------------------
        Total: 5/5
    """
    answerDiscount = 0.9
    answerNoise = 0
    answerLivingReward = 1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question8():
    r"""
    Question 8 (1 point): Bridge Crossing Revisited

    Execution:
        py -3.6 gridworld.py -a q -k 50 -n 0 -g BridgeGrid -e 1
        py -3.6 gridworld.py -a q -k 50 -n 0 -g BridgeGrid -e 0

        # Meh answer, -l == learning rate, -e == epsilon
        py -3.6 gridworld.py -a q -k 50 -n 0 -g BridgeGrid -e 0.5 -l 1

        py -3.6 autograder.py -q q8

    Notes:
        Q^new(s_t, a_t) = Q^old(s_t, a_t) + alpha * TD(s_t, a_t)
        TD(s_t, a_t) = r_t + (gamma * max_a Q(s_t+1, a)) - Q(s_t, a_t)

        Q^new(s_t, a_t) =  Q^old(s_t, a_t) + alpha * (r_t + (gamma * max_a Q(s_t+1, a)) - Q(s_t, a_t))
        Q^new(s_t, a_t) =  Q^old(s_t, a_t) + alpha * (r_t + (gamma * max_a Q(s_t+1, a)) - Q^old(s_t, a_t))

        TD =        Temporal Difference

        alpha =     learning rate
                        low alpha -> TD is not as impactful to Q^new
                        high alpha -> TD is very impactful to Q^new

        epsilon =   Exploitation or Exploration (low epsilon -> Exploitation, high epsilon -> Exploration)

    Reference:
        Exploration vs. Exploitation - Learning the Optimal Reinforcement Learning Policy

            Notes:
                If epsilon low then you will most likely do Exploitation
                If epsilon high then you will most likely do Exploration

            Reference:
                https://youtu.be/mo96Nqlo1L8?list=PLZbbT5o_s2xoWNVdDudn51XM8lOuZ_Njv&t=32

    Results:
        ### Question q8: 1/1 ###


        Finished at 23:30:10

        Provisional grades
        ==================
        Question q8: 1/1
        ------------------
        Total: 1/1

    """
    answerEpsilon = 0.8
    answerLearningRate = 0.9

    # return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'
    return 'NOT POSSIBLE'


if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis

    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
