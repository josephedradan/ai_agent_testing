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
from pacman.agent import AgentPacman
from pacman.agent.agent_pacman_minimax import dfs_recursive_minimax_v4
from pacman.game.game_state import GameState


class AgentPacmanMinimaxAlphaBeta(AgentPacman):
    """
    Your minimax agent with alpha-beta pruning (str_question 3)
    """

    def getAction(self, game_state: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        """

        Run:
            Testing:
                python agent_pacman_.py -p AgentPacmanMinimaxAlphaBeta -a depth=3 -l smallClassic
                py -3.6 agent_pacman_.py -p AgentPacmanMinimaxAlphaBeta -a depth=3 -l smallClassic  # Use this one

                py -3.6 autograder.py -q q3 --no-graphics  # Use this one


            Actual:
                python autograder.py -q q3
                python autograder.py -q q3 --no-graphics  

                py -3.6 autograder.py -q q3
                py -3.6 autograder.py -q q3 --no-graphics  # Use this one
        """

        ####################

        r"""
        V1
            DFS Recursive Minimax algorithm correctly implemented (With alpha beta pruning support)

        Notes:
            It's just dfs_recursive_minimax_v4 with the kwarg alpha_beta_pruning=True

        Result:
            py -3.6 autograder.py -q q3 --no-graphics 
                Question q3
                ===========

                *** PASS: test_cases\q3\0-eval-function-lose-states-1.test
                *** PASS: test_cases\q3\0-eval-function-lose-states-2.test
                *** PASS: test_cases\q3\0-eval-function-win-states-1.test
                *** PASS: test_cases\q3\0-eval-function-win-states-2.test
                *** PASS: test_cases\q3\0-lecture-6-tree.test
                *** PASS: test_cases\q3\0-small-tree.test
                *** PASS: test_cases\q3\1-1-minmax.test
                *** PASS: test_cases\q3\1-2-minmax.test
                *** PASS: test_cases\q3\1-3-minmax.test
                *** PASS: test_cases\q3\1-4-minmax.test
                *** PASS: test_cases\q3\1-5-minmax.test
                *** PASS: test_cases\q3\1-6-minmax.test
                *** PASS: test_cases\q3\1-7-minmax.test
                *** PASS: test_cases\q3\1-8-minmax.test
                *** PASS: test_cases\q3\2-1a-vary-depth.test
                *** PASS: test_cases\q3\2-1b-vary-depth.test
                *** PASS: test_cases\q3\2-2a-vary-depth.test
                *** PASS: test_cases\q3\2-2b-vary-depth.test
                *** PASS: test_cases\q3\2-3a-vary-depth.test
                *** PASS: test_cases\q3\2-3b-vary-depth.test
                *** PASS: test_cases\q3\2-4a-vary-depth.test
                *** PASS: test_cases\q3\2-4b-vary-depth.test
                *** PASS: test_cases\q3\2-one-ghost-3level.test
                *** PASS: test_cases\q3\3-one-ghost-4level.test
                *** PASS: test_cases\q3\4-two-list_agent_ghost-3level.test
                *** PASS: test_cases\q3\5-two-list_agent_ghost-4level.test
                *** PASS: test_cases\q3\6-tied-root.test
                *** PASS: test_cases\q3\7-1a-check-depth-one-ghost.test
                *** PASS: test_cases\q3\7-1b-check-depth-one-ghost.test
                *** PASS: test_cases\q3\7-1c-check-depth-one-ghost.test
                *** PASS: test_cases\q3\7-2a-check-depth-two-list_agent_ghost.test
                *** PASS: test_cases\q3\7-2b-check-depth-two-list_agent_ghost.test
                *** PASS: test_cases\q3\7-2c-check-depth-two-list_agent_ghost.test
                *** Running AgentPacmanMinimaxAlphaBeta on smallClassic 1 time(s).
                Pacman died! Score: 84
                Average Score: 84.0
                Scores:        84.0
                Win Rate:      0/1 (0.00)
                Record:        Loss
                *** Finished running AgentPacmanMinimaxAlphaBeta on smallClassic after 0 seconds.
                *** Won 0 out of 1 games. Average score: 84.000000 ***
                *** PASS: test_cases\q3\8-agent_pacman_-game.test

                ### Question q3: 5/5 ###


                Finished at 12:54:45

                Provisional grader
                ==================
                Question q3: 5/5
                ------------------
                Total: 5/5

                Your grader are NOT yet registered.  To register your grader, make sure
                to follow your instructor's guidelines to receive credit on your name_project.
        """
        action = dfs_recursive_minimax_v4(
            game_state,
            self.depth,
            self.evaluation_function,
            alpha_beta_pruning=True
        )

        return action
