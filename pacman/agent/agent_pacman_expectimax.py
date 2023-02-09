"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/30/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import List
from typing import Tuple
from typing import Union

from common.action import Action
from pacman.agent import AgentPacman
from common.state import State


def _dfs_recursive_expectimax_v1_handler(state: State,
                                         depth: int,
                                         function_evaluation: callable,
                                         index_agent: int = 0,
                                         ) -> float:
    """
    This is the actual DFS Recursive Expectimax algorithm's main body.

    Notes:
        This does not have probably for the summation part of the algorithm

    Reference:
        Lecture 7: Expectimax
            Notes:
                How to do it
            Reference:
                https://youtu.be/jaFRyzp7yWw?t=707
    """

    # Check if game is over via pacman dead or pacman got all food and survived
    if state.isWin() or state.isLose() or depth <= 0:
        score = function_evaluation(state, None)

        # Return the score
        return score

    # List of legal movements ("North")
    list_str_move_legal: List[str] = state.getLegalActions(agentIndex=index_agent)

    # If Pacman (Maximizer)
    if index_agent == 0:

        score_max: Union[float, None] = None

        for action in list_str_move_legal:
            state_new = state.generateSuccessor(index_agent, action)

            # Agent selection (Select next player for the next call)
            index_agent_new = index_agent + 1

            score_calculated = _dfs_recursive_expectimax_v1_handler(state_new,
                                                                    depth,
                                                                    function_evaluation,
                                                                    index_agent_new,
                                                                    )

            if score_max is None or score_calculated > score_max:
                score_max = score_calculated

        return score_max

    else:
        """
        If a Ghost (Avg of Summation or Avg of Summation of Expected values)
        Notes:
            In this example, there is no probability so no expected values
        """

        score_sum: Union[float, None] = 0

        for action in list_str_move_legal:

            state_new = state.generateSuccessor(index_agent, action)

            # Agent selection (Select next player for the next call)
            if index_agent >= state.getNumAgents() - 1:
                index_agent_new = 0
                depth_new = depth - 1  # *** DEPTH IS ONLY CHANGED WHEN ALL AGENTS HAVE MOVED
            else:
                index_agent_new = index_agent + 1
                depth_new = depth

            score_calculated = _dfs_recursive_expectimax_v1_handler(state_new,
                                                                    depth_new,
                                                                    function_evaluation,
                                                                    index_agent_new,
                                                                    )

            score_sum += score_calculated

        score_avg = score_sum / len(list_str_move_legal)
        return score_avg


def dfs_recursive_expectimax_v1(state: State,
                                depth: int,
                                function_evaluation: callable,
                                index_agent: int = 0,
                                ) -> Union[str, None]:
    """
    DFS Recursive Expectimax algorithm algorithm's header

    Notes:
        The header is needed to make selection of the action easier

    Reference:
        Lecture 7: Expectimax
            Notes:
                How to do it
            Reference:
                https://youtu.be/jaFRyzp7yWw?t=707

    """
    # List of legal movements ("North")
    list_str_move_legal: List[str] = state.getLegalActions(agentIndex=index_agent)

    # List that contains tuples where each tuple has (score, action) as its elements
    list_pair: List[Tuple[float, str]] = []

    for action in list_str_move_legal:
        state_new = state.generateSuccessor(index_agent, action)

        # Agent selection (Select next player for the next call)
        index_agent_new = index_agent + 1

        score_calculated = _dfs_recursive_expectimax_v1_handler(state_new,
                                                                depth,
                                                                function_evaluation,
                                                                index_agent_new,
                                                                )

        list_pair.append((score_calculated, action))

    # If there are pairs, select the action with the max cost and return the action.
    if list_pair:
        result = max(list_pair, key=lambda item: item[0])

        # print(list_pair)
        score_max = result[0]
        action_score_max = result[1]

        return action_score_max

    return None


class AgentPacmanExpectimax(AgentPacman):
    """
      Your expectimax player (str_question 4)
    """

    def getAction(self, state: State) -> Action:
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        """
        Notes:
            Just take dfs_recursive_minimax_v4 and modify it by changing the the Minimizer to an
            Avg of the Summation of expected values

        Run:
            Testing:
                python autograder.py -q q4
                python autograder.py -q q4 --no-graphics  

                py -3.6 autograder.py -q q4
                py -3.6 autograder.py -q q4 --no-graphics  # Use this one

            Actual:
                python autograder.py -q q4
                python autograder.py -q q4 --no-graphics  

                py -3.6 autograder.py -q q4
                py -3.6 autograder.py -q q4 --no-graphics  # Use this one
        """

        ####################

        r"""
        V1
            The correct expectimax algorithm based on the body of dfs_recursive_minimax_v4

        Notes:
            It's just a modified dfs_recursive_minimax_v4 to use only a Maximizer and a Avg of Summation Expected
            values

        Result:
            py -3.6 autograder.py -q q4 --no-graphics
                Question q4
                ===========

                *** PASS: test_cases\q4\0-eval-function-lose-states-1.test
                *** PASS: test_cases\q4\0-eval-function-lose-states-2.test
                *** PASS: test_cases\q4\0-eval-function-win-states-1.test
                *** PASS: test_cases\q4\0-eval-function-win-states-2.test
                *** PASS: test_cases\q4\0-expectimax1.test
                *** PASS: test_cases\q4\1-expectimax2.test
                *** PASS: test_cases\q4\2-one-ghost-3level.test
                *** PASS: test_cases\q4\3-one-ghost-4level.test
                *** PASS: test_cases\q4\4-twoghosts-3level.test
                *** PASS: test_cases\q4\5-twoghosts-4level.test
                *** PASS: test_cases\q4\6-1a-check-depth-one-ghost.test
                *** PASS: test_cases\q4\6-1b-check-depth-one-ghost.test
                *** PASS: test_cases\q4\6-1c-check-depth-one-ghost.test
                *** PASS: test_cases\q4\6-2a-check-depth-two-ghosts.test
                *** PASS: test_cases\q4\6-2b-check-depth-two-ghosts.test
                *** PASS: test_cases\q4\6-2c-check-depth-two-ghosts.test
                *** Running AgentPacmanExpectimax on smallClassic 1 time(s).
                Pacman died! Score: 84
                Average Score: 84.0
                Scores:        84.0
                Win Rate:      0/1 (0.00)
                Record:        Loss
                *** Finished running AgentPacmanExpectimax on smallClassic after 0 seconds.
                *** Won 0 out of 1 games. Average score: 84.000000 ***
                *** PASS: test_cases\q4\7-pacman-game.test

                ### Question q4: 5/5 ###


                Finished at 12:53:27

                Provisional grader
                ==================
                Question q4: 5/5
                ------------------
                Total: 5/5

                Your grader are NOT yet registered.  To register your grader, make sure
                to follow your instructor's guidelines to receive credit on your name_project.
        """
        result = dfs_recursive_expectimax_v1(
            state,
            self.depth,
            self.evaluation_function
        )

        return result
