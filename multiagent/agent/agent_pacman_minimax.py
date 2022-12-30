"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/29/2022

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

from multiagent.agent import AgentPacman
from multiagent.game.directions import Action
from multiagent.game.gamestate import GameState


class AgentContainer:
    __slots__ = ["index_agent", "action", "score"]

    def __init__(self, index_agent, action):
        self.index_agent = index_agent
        self.action = action
        self.score = None

    def __str__(self):
        return "({} {} {})".format(self.index_agent, self.action, self.score)


# @callgraph(use_list_index_args=[1, 3, 4], display_callable_name=False, )
def dfs_recursive_minimax_v1(game_state: GameState,
                             depth: int,
                             function_evaluation: callable,
                             index_agent: int = 0,
                             agent_container_previous: AgentContainer = None,
                             ) -> [float, AgentContainer]:
    """
    Does dfs recursive minimax

    Notes:
        Does not work because you are stacking multiple min agents on top of each other which causes min of min

        Basically, you want
            max -> min -> max -> min -> max -> etc...
            not
            max -> min -> min -> max -> min -> min

        because you will propagate multiple min values which is wrong

    IMPORTANT NOTES:
        THE ASSUMPTION MADE in "Notes" IS WRONG, LOOK AT dfs_recursive_minimax_v3 FOR CORRECT SOLUTION

        DO NOT USE THIS CODE, IT IS NOT CORRECT AND THE ASSUMPTIONS ARE WRONG

    Reference:
        Algorithms Explained – minimax and alpha-beta pruning
            Reference:
                https://www.youtube.com/watch?v=l-hh51ncgDI
    """

    # print("index_agent", index_agent, "depth", depth)

    # List of legal movements ("North")
    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # Check if game is over via pacman dead or pacman got all food and survived
    if game_state.isWin() or game_state.isLose() or depth == 0:
        score = function_evaluation(game_state)
        agent_container_previous.score = score

        # Return the score
        return score, agent_container_previous

    # If Pacman (Maximizer)
    if index_agent == 0:

        score_max: Union[float, None] = None
        agent_container_final_score_max: Union[AgentContainer, None] = None

        # _LIST_TEMP = []

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            agent_container_current = AgentContainer(index_agent, action)

            # Agent selection (Select next agent for the next call)
            index_agent_new = index_agent + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v1(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  )

            # _LIST_TEMP.append(score_calculated)

            if score_max is None or score_calculated > score_max:
                score_max = score_calculated

                """
                *** INCORRECT TO ASSIGN agent_container_current TO agent_container_final_score_max
                LOOK AT dfs_recursive_minimax_v3 FOR THE CORRECT SOLUTION
                """
                agent_container_final_score_max = agent_container_current

        # print("P Depth", depth)
        # print("P MOVE", list_str_move_legal)
        # print("P ACTION", agent_container_final_score_max.action)
        # print("P CALCULATED", _LIST_TEMP)
        # print("P Score: {} Action: {} ".format(score_max, agent_container_final_score_max.action))
        # print()
        return score_max, agent_container_final_score_max

    # If a Ghost (Minimizer)
    else:
        score_min: Union[float, None] = None
        agent_container_final_score_min: Union[AgentContainer, None] = None

        # _LIST_TEMP = []

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            agent_container_current = AgentContainer(index_agent, action)

            # Agent selection (Select next agent for the next call)
            if index_agent >= game_state.getNumAgents() - 1:
                index_agent_new = 0
                depth -= 1  # Depth is only decremented when all agents have moved

            else:
                index_agent_new = index_agent + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v1(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  )

            # _LIST_TEMP.append(score_calculated)

            if score_min is None or score_calculated < score_min:
                score_min = score_calculated
                """
                *** INCORRECT TO ASSIGN agent_container_current TO agent_container_final_score_min
                LOOK AT dfs_recursive_minimax_v3 FOR THE CORRECT SOLUTION
                """
                agent_container_final_score_min = agent_container_current  # *** WRONG TO ASSIGN agent_container_current

        # print(f"G{index_agent} Depth", depth)
        # print(f"G{index_agent} MOVE", list_str_move_legal)
        # print(f"G{index_agent} ACTION", agent_container_final_score_min.action)
        # print(f"G{index_agent} CALCULATED", _LIST_TEMP)
        # print("G{} Score: {} Action: {} ".format(index_agent, score_min, agent_container_final_score_min.action))
        # print()

        return score_min, agent_container_final_score_min


##############################################################################################################

class AgentGhostContainer:

    def __init__(self, game_state: GameState, index_agent: int, action: str,
                 game_state_previous: GameState):
        self.game_state = game_state
        self.index_agent = index_agent
        self.action = action
        self.game_state_previous = game_state_previous


def get_list_last_ghost_agent_game_state(game_state: GameState,
                                         index_agent: int,
                                         game_state_previous: GameState,
                                         list_game_state: List[float] = None
                                         ) -> List[AgentGhostContainer]:
    """
    This gets the game_state based on the last ghost before it becomes pacman's turn to move

    Notes:
        Needs the first of the ghosts -> returns list of game_state that are the last game_state
        before pacman's turn

    """
    if list_game_state is None:
        list_game_state = []

    if index_agent == 0:
        print("YOUR INPUT IS WRONG")
        return get_list_last_ghost_agent_game_state(game_state, index_agent + 1, game_state_previous)

    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # print(list_str_move_legal)

    for action in list_str_move_legal:

        game_state_new = game_state.generateSuccessor(index_agent, action)

        index_agent_new = index_agent + 1
        # print(index_agent_new)

        if index_agent >= game_state.getNumAgents() - 1:

            # print("ADD TO LIST", index_agent, action, game_state.getGhostPosition(index_agent))
            # if index_agent == 2:
            #     print(game_state.getGhostPosition(index_agent - 1))
            # print()

            agent_ghost_container = AgentGhostContainer(game_state,
                                                        index_agent,
                                                        action,
                                                        game_state_previous)

            list_game_state.append(agent_ghost_container)
        else:
            # print("RECURSIVE CALL", index_agent, action, game_state.getGhostPosition(index_agent))
            # if index_agent == 2:
            #     print(game_state.getGhostPosition(index_agent - 1))

            if game_state.isWin() or game_state.isLose():
                agent_ghost_container = AgentGhostContainer(game_state,
                                                            index_agent,
                                                            action,
                                                            game_state_previous)
                return [agent_ghost_container]

            get_list_last_ghost_agent_game_state(game_state_new,
                                                 index_agent_new,
                                                 game_state,
                                                 list_game_state)

    return list_game_state


# @callgraph(use_list_index_args=[1, 3, 4], display_callable_name=False, )
def dfs_recursive_minimax_v2(game_state: GameState,
                             depth: int,
                             function_evaluation: callable,
                             index_agent: int = 0,
                             agent_container_previous: AgentContainer = None,
                             game_state_previous: GameState = None,
                             ) -> [float, AgentContainer]:
    """
    This function tries to compress all ghost agents together, the problem is that not all ghosts need to move in order
    for the game to end.

    Basically, the game can end when one of the ghosts moves so compressing all ghost agent moves together passes the
    point when the game ends, so it's suboptimal to do this.

    This means that dfs_recursive_minimax_v1 is more correct than this solution.

    IMPORTANT NOTE:
        *** THIS CODE DOES NOT WORK AND THE ASSUMPTIONS ABOUT SKIPPING TO THE LAST GHOST BEFORE PACMAN'S TURN IS WRONG

    """

    # print("index_agent", index_agent)

    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # Check if game is over via pacman dead or pacman got all food and survived
    if game_state.isWin() or game_state.isLose() or depth == 0:
        score = function_evaluation(game_state)
        agent_container_previous.score = score

        # Return the score
        return score, agent_container_previous

    # If Pacman (Maximizer)
    if index_agent == 0:

        score_max: Union[float, None] = None
        agent_container_final_score_max: Union[AgentContainer, None] = None

        list_temp = []

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            agent_container_current = AgentContainer(index_agent, action)

            # Agent selection (Select next agent for the next call)
            index_agent_new = index_agent + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v2(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  game_state,
                                                                                  )

            list_temp.append(score_calculated)

            if score_max is None or score_calculated > score_max:
                score_max = score_calculated
                agent_container_final_score_max = agent_container_current

        # print("depth", depth)
        # print("PACMAN SCORES", list_temp)
        # print()
        return score_max, agent_container_final_score_max

    # If a Ghost (Minimizer)
    else:

        list_last_ghost_agent_game_state = get_list_last_ghost_agent_game_state(game_state,
                                                                                index_agent,
                                                                                game_state_previous)

        # print("list_last_ghost_agent_game_state", list_last_ghost_agent_game_state)

        score_min: Union[float, None] = None
        agent_container_final_score_min: Union[AgentContainer, None] = None

        _LIST_TEMP = []

        for last_ghost_agent_game_state in list_last_ghost_agent_game_state:

            index_agent_last = last_ghost_agent_game_state.index_agent

            action = list_last_ghost_agent_game_state

            game_state_new = last_ghost_agent_game_state.game_state

            agent_container_current = AgentContainer(index_agent_last, action)

            # Agent selection (Select next agent for the next call)
            if index_agent_last >= game_state.getNumAgents() - 1:
                index_agent_new = 0
                depth -= 1  # Depth is only decremented when all agents have moved
            else:
                index_agent_new = index_agent_last + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v2(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  game_state,
                                                                                  )

            _LIST_TEMP.append(score_calculated)

            if score_min is None or score_calculated < score_min:
                score_min = score_calculated
                agent_container_final_score_min = agent_container_current

        # THE BELOW WILL BASICALLY ADDS REPEAT CALLS WHICH IS WRONG.
        # for action in list_str_move_legal:
        #
        #     for last_ghost_agent_game_state in list_last_ghost_agent_game_state:
        #
        #         game_state_last = last_ghost_agent_game_state.game_state
        #         # print("last_ghost_agent_game_state.index_agent", last_ghost_agent_game_state.index_agent)
        #
        #         index_agent_last = last_ghost_agent_game_state.index_agent
        #         game_state_new = game_state_last.generateSuccessor(index_agent_last, action)
        #
        #         agent_container_current = AgentContainer(index_agent_last, action)
        #
        #         # Agent selection (Select next agent for the next call)
        #         if index_agent_last >= game_state.getNumAgents() - 1:
        #             index_agent_new = 0
        #             depth -= 1  # Depth is only decremented when all agents have moved
        #         else:
        #             index_agent_new = index_agent_last + 1
        #
        #         score_calculated, agent_container_returned = dfs_recursive_minimax_v2(game_state_new,
        #                                                                               depth,
        #                                                                               function_evaluation,
        #                                                                               index_agent_new,
        #                                                                               agent_container_current,
        #                                                                               game_state,
        #                                                                               )
        #
        #         _LIST_TEMP.append(score_calculated)
        #
        #         if score_min is None or score_calculated < score_min:
        #             score_min = score_calculated
        #             agent_container_final_score_min = agent_container_current

        # print("depth", depth)
        # print(_LIST_TEMP)
        # print()
        return score_min, agent_container_final_score_min


##############################################################################################################

# @callgraph(use_list_index_args=[1, 3, 4], display_callable_name=False, )
def dfs_recursive_minimax_v3(game_state: GameState,
                             depth: int,
                             function_evaluation: callable,
                             index_agent: int = 0,
                             agent_container_previous: AgentContainer = None,
                             ) -> [float, AgentContainer]:
    """
    DFS Recursive Minimax algorithm almost correctly implemented

    *** THIS CODE IS STILL WRONG, IT ASSUMES THAT THE FIRST CHILDREN OF THE ROOT ARE MINIMIZERS.
        THE CORRECT IMPLEMENTATION IS dfs_recursive_minimax_v4

    IMPORTANT NOTES:
        THE ONLY DIFFERENCE BETWEEN dfs_recursive_minimax_v3 and dfs_recursive_minimax_v1 IS THAT
        THE CORRECT AgentContainer agent_container_returned IS RETURNED FOR
        agent_container_final_score_min
        AND
        agent_container_final_score_max

        *** THE REASON WHY YOU NEED TO RETURN agent_container_returned INSTEAD IS BECAUSE
        YOU HAVE TO REMEMBER THAT YOU ARE SELECTING THE AgentContainer FROM THE FOLLOWING CALL. SO
        agent_container_current IS NOT CORRECT BECAUSE THE FOLLOWING RECURSIVE CALL MAY HAVE FOUND THAT
        agent_container_current MAY NOT BE THE
        agent_container_final_score_min or agent_container_final_score_max

        BECAUSE OF MINOR CODE CHANGE, dfs_recursive_minimax_v3 MUST EXIST SO THAT FUTURE ME WILL NOTICE MY MISTAKE
        AND WILL NOT HAVE TO REPEAT THIS DEBUGGING PROCESS.

    Reference:
        Algorithms Explained – minimax and alpha-beta pruning
            Reference:
                https://www.youtube.com/watch?v=l-hh51ncgDI
    """

    # List of legal movements ("North")
    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # Check if game is over via pacman dead or pacman got all food and survived
    if game_state.isWin() or game_state.isLose() or depth == 0:
        score = function_evaluation(game_state)
        agent_container_previous.score = score
        # Return the score
        return score, agent_container_previous

    # If Pacman (Maximizer)
    if index_agent == 0:

        score_max: Union[float, None] = None
        agent_container_final_score_max: Union[AgentContainer, None] = None

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            agent_container_current = AgentContainer(index_agent, action)

            # Agent selection (Select next agent for the next call)
            index_agent_new = index_agent + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v3(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  )

            if score_max is None or score_calculated > score_max:
                score_max = score_calculated

                """
                *** ASSIGN agent_container_returned TO 
                agent_container_final_score_max
                INSTEAD OF 
                agent_container_current
                BECAUSE THE FOLLOWING CALL MUST SELECT THE AgentContainer
                """
                agent_container_final_score_max = agent_container_returned

        return score_max, agent_container_final_score_max

    # If a Ghost (Minimizer)
    else:
        score_min: Union[float, None] = None
        agent_container_final_score_min: Union[AgentContainer, None] = None

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            agent_container_current = AgentContainer(index_agent, action)

            # Agent selection (Select next agent for the next call)
            if index_agent >= game_state.getNumAgents() - 1:
                index_agent_new = 0
                depth -= 1  # Depth is only decremented when all agents have moved

            else:
                index_agent_new = index_agent + 1

            score_calculated, agent_container_returned = dfs_recursive_minimax_v3(game_state_new,
                                                                                  depth,
                                                                                  function_evaluation,
                                                                                  index_agent_new,
                                                                                  agent_container_current,
                                                                                  )

            if score_min is None or score_calculated < score_min:
                score_min = score_calculated

                """
                *** ASSIGN agent_container_returned TO 
                agent_container_final_score_min 
                INSTEAD OF 
                agent_container_current
                BECAUSE THE FOLLOWING CALL MUST SELECT THE AgentContainer
                """
                agent_container_final_score_min = agent_container_returned

        return score_min, agent_container_final_score_min


##############################################################################################################

# @callgraph(use_list_index_args=[1, 5, 7], display_callable_name=False, )
def _dfs_recursive_minimax_v4_handler(game_state: GameState,
                                      depth: int,
                                      alpha: Union[None, float],
                                      beta: Union[None, float],
                                      function_evaluation: callable,
                                      index_agent: int = 0,
                                      alpha_beta_pruning: bool = False,
                                      # _callgraph_special: Any = None
                                      ) -> float:
    """
    This is the actual DFS Recursive Minimax algorithm's main body.

    Notes:
        This is the correct implementation of the algorithm needed to get all the points for autograder.py's
        Q2 and Q3

    Reference:
        Algorithms Explained – minimax and alpha-beta pruning
            Reference:
                https://www.youtube.com/watch?v=l-hh51ncgDI
    """

    # Check if game is over via pacman dead or pacman got all food and survived
    if game_state.isWin() or game_state.isLose() or depth <= 0:
        score = function_evaluation(game_state)

        # Return the score
        return score

    # List of legal movements ("North")
    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # If Pacman (Maximizer)
    if index_agent == 0:

        score_max: Union[float, None] = None

        # _LIST_SCORE_DEBUG = []

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            # Agent selection (Select next agent for the next call)
            index_agent_new = index_agent + 1

            score_calculated = _dfs_recursive_minimax_v4_handler(game_state_new,
                                                                 depth,
                                                                 alpha,
                                                                 beta,
                                                                 function_evaluation,
                                                                 index_agent_new,
                                                                 alpha_beta_pruning,
                                                                 # str((depth, index_agent, action))
                                                                 )

            # _LIST_SCORE_DEBUG.append(score_calculated)

            if score_max is None or score_calculated > score_max:
                score_max = score_calculated

            if alpha_beta_pruning:

                if alpha is None or score_calculated > alpha:
                    alpha = score_calculated

                r"""
                Notes:
                    Do not use <= on the minimizer, use < because <= will break test_cases\q3\6-tied-root.test 
                    because it will cut off a branch that may have a low score. Because the code
                    for the minimizer is the same for the maximizer, then the maximizer should have the same
                    logic as the minimizer.

                IMPORTANT NOTES:
                    YOU MUST USE
                        if beta is not None and alpha is not None and beta < alpha
                    AND NOT
                        if beta and alpha and beta < alpha
                    BECAUSE beta AND alpha MIGHT BE 0.0 WHICH WOULD RESULT IN False
                """
                if beta is not None and alpha is not None and beta < alpha:
                    # Cut off branch
                    break

        # print("P Depth", depth)
        # print("P MOVE", list_str_move_legal)
        # print("P CALCULATED", _LIST_SCORE_DEBUG)
        # print("P Score: {} ".format(score_max))
        # print()

        return score_max

    # If a Ghost (Minimizer)
    else:
        score_min: Union[float, None] = None

        # _LIST_SCORE_DEBUG = []

        for action in list_str_move_legal:

            game_state_new = game_state.generateSuccessor(index_agent, action)

            # Agent selection (Select next agent for the next call)
            if index_agent >= game_state.getNumAgents() - 1:
                index_agent_new = 0
                depth_new = depth - 1  # *** DEPTH IS ONLY CHANGED WHEN ALL AGENTS HAVE MOVED
            else:
                index_agent_new = index_agent + 1
                depth_new = depth

            score_calculated = _dfs_recursive_minimax_v4_handler(game_state_new,
                                                                 depth_new,
                                                                 alpha,
                                                                 beta,
                                                                 function_evaluation,
                                                                 index_agent_new,
                                                                 alpha_beta_pruning,
                                                                 # str((depth, index_agent, action))
                                                                 )

            # _LIST_SCORE_DEBUG.append(score_calculated)

            if score_min is None or score_calculated < score_min:
                score_min = score_calculated

            if alpha_beta_pruning:

                if beta is None or score_calculated < beta:
                    beta = score_calculated

                r"""
                Notes:
                    Do not use <= on the minimizer, use < because <= will break test_cases\q3\6-tied-root.test 
                    because it will cut off a branch that may have a low score. Because the code
                    for the minimizer is the same for the maximizer, then the maximizer should have the same
                    logic as the minimizer.

                IMPORTANT NOTES:
                    YOU MUST USE
                        if beta is not None and alpha is not None and beta < alpha
                    AND NOT
                        if beta and alpha and beta < alpha
                    BECAUSE beta AND alpha MIGHT BE 0.0 WHICH WOULD RESULT IN False
                """
                if beta is not None and alpha is not None and beta < alpha:
                    # Cut off branch
                    break

        # print(f"G{index_agent} Depth", depth)
        # print(f"G{index_agent} MOVE", list_str_move_legal)
        # print(f"G{index_agent} CALCULATED", _LIST_SCORE_DEBUG)
        # print("G{} Score: {}".format(index_agent, score_min))
        # print()

        return score_min


# @callgraph(use_list_index_args=[1, 3], display_callable_name=False,)
def dfs_recursive_minimax_v4(game_state: GameState,
                             depth: int,
                             function_evaluation: callable,
                             index_agent: int = 0,
                             alpha_beta_pruning: bool = False,
                             ) -> Union[str, None]:
    """
    DFS Recursive Minimax algorithm correctly implemented (With alpha beta pruning support)

    Notes:
        This is the header for DFS Recursive Minimax algorithm, the reason why it's the header is because
        the root is pacman and its children should be its actions and you want to select the action based on the
        score. If this header was not hear like with the previous versions of this code, then you would need to
        look at children of the root again to know which move was associated with the score returned to the root.

        Basically, the code would look uglier if you didn't have this header.

    Reference:
        Algorithms Explained – minimax and alpha-beta pruning
            Reference:
                https://www.youtube.com/watch?v=l-hh51ncgDI
    """
    # List of legal movements ("North")
    list_str_move_legal: List[str] = game_state.getLegalActions(agentIndex=index_agent)

    # List that contains tuples where each tuple has (score, action) as its elements
    list_pair: List[Tuple[float, str]] = []

    # alpha and beta for alpha beta pruning
    alpha: Union[None, float] = None
    beta: Union[None, float] = None

    for action in list_str_move_legal:

        game_state_new = game_state.generateSuccessor(index_agent, action)

        # Agent selection (Select next agent for the next call)
        index_agent_new = index_agent + 1

        score_calculated = _dfs_recursive_minimax_v4_handler(game_state_new,
                                                             depth,
                                                             alpha,
                                                             beta,
                                                             function_evaluation,
                                                             index_agent_new,
                                                             alpha_beta_pruning,
                                                             # str((depth, index_agent, action))
                                                             )

        if alpha_beta_pruning:

            if alpha is None or score_calculated > alpha:
                alpha = score_calculated

            r"""
            Notes:
                Do not use <= on the minimizer, use < because <= will break test_cases\q3\6-tied-root.test 
                because it will cut off a branch that may have a low score. Because the code
                for the minimizer is the same for the maximizer, then the maximizer should have the same
                logic as the minimizer.

            IMPORTANT NOTES:
                YOU MUST USE
                    if beta is not None and alpha is not None and beta < alpha
                AND NOT
                    if beta and alpha and beta < alpha
                BECAUSE beta AND alpha MIGHT BE 0.0 WHICH WOULD RESULT IN False
            """
            if beta is not None and alpha is not None and beta < alpha:
                # Cut off branch
                break

        list_pair.append((score_calculated, action))

        # print("-" * 50)

    # If there are pairs, select the action with the max cost and return the action.
    if list_pair:
        result = max(list_pair, key=lambda item: item[0])

        score_max = result[0]
        action_score_max = result[1]

        # print(list_pair)
        # print(action_score_max)
        # print("#" * 100)

        # create_callgraph(type_output="png")

        return action_score_max

    return None


class AgentPacmanMinimax(AgentPacman):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState) -> Action:
        """
        Returns the minimax action from the current game_state using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        game_state.generateSuccessor(agentIndex, action):
        Returns the successor game game_state after an agent takes an action

        game_state.getNumAgents():
        Returns the total number of agents in the game

        game_state.isWin():
        Returns whether or not the game game_state is a winning game_state

        game_state.isLose():
        Returns whether or not the game game_state is a losing game_state
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        """

        Notes:
            In this function, we need to select a direction of movement that is the best to make.
            Basically, do a DFS Minimax, write that here pls.

            Recall that evaluationFunction does the score stuff related to direction and food

            self.evaluationFunction(game_state) returns a score (float)

            Use getAction From PacmanReflex as a reference too
        Run:
            Testing:
                python pacman.py -f -p AgentPacmanMinimax -l trappedClassic -a depth=3
                py -3.6 pacman.py -f -p AgentPacmanMinimax -l trappedClassic -a depth=3
                py -3.6 pacman.py -f -p AgentPacmanMinimax -l trappedClassic -a depth=3  # Use this one

            Actual:
                python autograder.py -q q2
                python autograder.py -q q2 --no-graphics  

                py -3.6 autograder.py -q q2
                py -3.6 autograder.py -q q2 --no-graphics  # Use this one

        """

        ####################

        # print('game_state.getLegalActions(0)',
        #       type(game_state.getLegalActions(0)),
        #       game_state.getLegalActions(0))
        # print('game_state.generateSuccessor(0, "North")',
        #       type(game_state.generateSuccessor(0, "North")),
        #       game_state.generateSuccessor(0, "North"))
        # print('game_state.getNumAgents()',
        #       type(game_state.getNumAgents()),
        #       game_state.getNumAgents())
        # print('game_state.isWin()', type(game_state.isWin()), game_state.isWin())
        # print('game_state.isLose()', type(game_state.isLose()), game_state.isLose())
        #
        # print("#" * 100)

        ####################
        # """
        # V1
        #     Standard minimax that should technically work for 1 vs 1 (Wrong assumption, Read "IMPORTANT NOTES")
        #
        # Notes:
        #     This algorithm stacks multiple min calls on top of each other which causes a small value to always
        #     propagate back.
        #
        # IMPORTANT NOTES:
        #     BOTH "Notes" and the description for V1 are WRONG. The actual reason for why this code is wrong,
        #     is because of a mistake I made in the code. Look at V3 for the actual answer.
        #
        # Result:
        #     py -3.6 pacman.py -f -p AgentPacmanMinimax -l trappedClassic -a depth=3
        #         Result:
        #             Pacman died! Score: -501
        #             Average Score: -501.0
        #             Scores:        -501.0
        #             Win Rate:      0/1 (0.00)
        #             Record:        Loss
        # """
        # result = dfs_recursive_minimax_v1(game_state, self.depth, self.evaluationFunction)
        #
        # score_final: float = result[0]
        #
        # agent_container_final: AgentContainer = result[1]
        #
        # # print("SCORE: {} PLAYER INDEX: {} PLAYER ACTION: {}".format(score_final,
        # #                                                             agent_container_final.index_agent,
        # #                                                             agent_container_final.action))
        # # create_callgraph(type_output="png")
        #
        # return agent_container_final.action

        ##########
        # """
        # V2
        #     Like v1 (standard minimax algorithm) but tries to compress all ghost agent actions together
        #     based on the assumption that all ghost actions must be made before a win or loss game game_state is reached.
        #
        # Notes:
        #     I generated the call graph and my assumption is wrong. The game can end even when not all ghost actions
        #     have been processed. This means you need to constantly check game_state if the game is a win or a loss.
        #
        # Results:
        #     Crashes because dfs_recursive_minimax_v2 runs all ghost agent actions and during that process the game
        #     may have ended via pacman win or loss (most likely loss because only ghosts move at this time).
        #     So any further game_state past the winning/losing game_state DOES NOT RETURN A SCORE which is needed
        #     to determine the action for pacman.
        #
        #     Basically, it crashes because None is returned when selecting the score and a score needs to be a number
        #
        # """
        #
        # result = dfs_recursive_minimax_v2(game_state, self.depth, self.evaluationFunction)
        #
        # score_final: float = result[0]
        #
        # agent_container_final: AgentContainer = result[1]
        #
        # # print("SCORE: {} PLAYER INDEX: {} PLAYER ACTION: {}".format(score_final,
        # #                                                             agent_container_final.index_agent,
        # #                                                             agent_container_final.action))
        # # create_callgraph(type_output="png")
        #
        # return agent_container_final.action

        ##########
        # r"""
        # V3
        #     DFS Recursive Minimax algorithm almost correctly implemented
        #
        # Notes:
        #     This is just V1 with a minor code fix that gets the correct answer
        #
        # Result:
        #     py -3.6 pacman.py -f -p AgentPacmanMinimax -l trappedClassic -a depth=3
        #         Result:
        #             Pacman emerges victorious! Score: 532
        #             Average Score: 532.0
        #             Scores:        532.0
        #             Win Rate:      1/1 (1.00)
        #             Record:        Win
        #      py -3.6 autograder.py -q q2
        #         Result:
        #             *** PASS: test_cases\q2\0-eval-function-lose-states-1.test
        #             *** PASS: test_cases\q2\0-eval-function-lose-states-2.test
        #             *** PASS: test_cases\q2\0-eval-function-win-states-1.test
        #             *** PASS: test_cases\q2\0-eval-function-win-states-2.test
        #             *** PASS: test_cases\q2\0-lecture-6-tree.test
        #             *** FAIL: test_cases\q2\0-small-tree.test
        #             *** PASS: test_cases\q2\1-1-minmax.test
        #             *** FAIL: test_cases\q2\1-2-minmax.test
        #             *** FAIL: test_cases\q2\1-3-minmax.test
        #             *** FAIL: test_cases\q2\1-4-minmax.test
        #             *** FAIL: test_cases\q2\1-5-minmax.test
        #             *** FAIL: test_cases\q2\1-6-minmax.test
        #             *** FAIL: test_cases\q2\1-7-minmax.test
        #             *** FAIL: test_cases\q2\1-7-minmax.test
        #             *** PASS: test_cases\q2\1-8-minmax.test
        #             *** FAIL: test_cases\q2\2-1a-vary-depth.test
        #             *** FAIL: test_cases\q2\2-1b-vary-depth.test
        #             *** FAIL: test_cases\q2\2-2a-vary-depth.test
        #             *** FAIL: test_cases\q2\2-2b-vary-depth.test
        #             *** FAIL: test_cases\q2\2-3a-vary-depth.test
        #             *** FAIL: test_cases\q2\2-3b-vary-depth.test
        #             *** FAIL: test_cases\q2\2-4a-vary-depth.test
        #             *** FAIL: test_cases\q2\2-4b-vary-depth.test
        #             *** FAIL: test_cases\q2\2-one-ghost-3level.test
        #             *** PASS: test_cases\q2\3-one-ghost-4level.test
        #             *** PASS: test_cases\q2\4-two-ghosts-3level.test
        #             *** FAIL: test_cases\q2\5-two-ghosts-4level.test
        #             *** FAIL: test_cases\q2\6-tied-root.test
        #             *** FAIL: test_cases\q2\7-1a-check-depth-one-ghost.test
        #             *** PASS: test_cases\q2\7-1b-check-depth-one-ghost.test
        #             *** FAIL: test_cases\q2\7-1c-check-depth-one-ghost.test
        #             *** FAIL: test_cases\q2\7-2a-check-depth-two-ghosts.test
        #             *** PASS: test_cases\q2\7-2b-check-depth-two-ghosts.test
        #             *** FAIL: test_cases\q2\7-2c-check-depth-two-ghosts.test
        #             ...
        #             RecursionError: maximum recursion depth exceeded in comparison
        # """
        #
        # result = dfs_recursive_minimax_v3(game_state, self.depth, self.evaluationFunction)
        #
        # score_final: float = result[0]
        #
        # agent_container_final: AgentContainer = result[1]
        #
        # # print("SCORE: {} PLAYER INDEX: {} PLAYER ACTION: {}".format(score_final,
        # #                                                             agent_container_final.index_agent,
        # #                                                             agent_container_final.action))
        # # create_callgraph(type_output="png")
        #
        # return agent_container_final.action

        ##########
        r"""
        V4
            DFS Recursive Minimax algorithm correctly implemented (With alpha beta pruning support)

        Notes:
            This is the only version that I have that works correctly

        Result:
            py -3.6 autograder.py -q q2 --no-graphics
                Question q2
                ===========

                *** PASS: test_cases\q2\0-eval-function-lose-states-1.test
                *** PASS: test_cases\q2\0-eval-function-lose-states-2.test
                *** PASS: test_cases\q2\0-eval-function-win-states-1.test
                *** PASS: test_cases\q2\0-eval-function-win-states-2.test
                *** PASS: test_cases\q2\0-lecture-6-tree.test
                *** PASS: test_cases\q2\0-small-tree.test
                *** PASS: test_cases\q2\1-1-minmax.test
                *** PASS: test_cases\q2\1-2-minmax.test
                *** PASS: test_cases\q2\1-3-minmax.test
                *** PASS: test_cases\q2\1-4-minmax.test
                *** PASS: test_cases\q2\1-5-minmax.test
                *** PASS: test_cases\q2\1-6-minmax.test
                *** PASS: test_cases\q2\1-7-minmax.test
                *** PASS: test_cases\q2\1-8-minmax.test
                *** PASS: test_cases\q2\2-1a-vary-depth.test
                *** PASS: test_cases\q2\2-1b-vary-depth.test
                *** PASS: test_cases\q2\2-2a-vary-depth.test
                *** PASS: test_cases\q2\2-2b-vary-depth.test
                *** PASS: test_cases\q2\2-3a-vary-depth.test
                *** PASS: test_cases\q2\2-3b-vary-depth.test
                *** PASS: test_cases\q2\2-4a-vary-depth.test
                *** PASS: test_cases\q2\2-4b-vary-depth.test
                *** PASS: test_cases\q2\2-one-ghost-3level.test
                *** PASS: test_cases\q2\3-one-ghost-4level.test
                *** PASS: test_cases\q2\4-two-ghosts-3level.test
                *** PASS: test_cases\q2\5-two-ghosts-4level.test
                *** PASS: test_cases\q2\6-tied-root.test
                *** PASS: test_cases\q2\7-1a-check-depth-one-ghost.test
                *** PASS: test_cases\q2\7-1b-check-depth-one-ghost.test
                *** PASS: test_cases\q2\7-1c-check-depth-one-ghost.test
                *** PASS: test_cases\q2\7-2a-check-depth-two-ghosts.test
                *** PASS: test_cases\q2\7-2b-check-depth-two-ghosts.test
                *** PASS: test_cases\q2\7-2c-check-depth-two-ghosts.test
                *** Running AgentPacmanMinimax on smallClassic 1 time(s).
                Pacman died! Score: 84
                Average Score: 84.0
                Scores:        84.0
                Win Rate:      0/1 (0.00)
                Record:        Loss
                *** Finished running AgentPacmanMinimax on smallClassic after 0 seconds.
                *** Won 0 out of 1 games. Average score: 84.000000 ***
                *** PASS: test_cases\q2\8-pacman-game.test

                ### Question q2: 5/5 ###


                Finished at 12:56:39

                Provisional grades
                ==================
                Question q2: 5/5
                ------------------
                Total: 5/5

                Your grades are NOT yet registered.  To register your grades, make sure
                to follow your instructor's guidelines to receive credit on your project.
        """
        action = dfs_recursive_minimax_v4(gameState, self.depth, self.evaluation_function)

        # create_callgraph(type_output="png")

        return action
