
# Mapping correct test cases
    1 8
    9 14 (14 is extra)
    15 24


# Examples
        
    python autograder.py -q q1
    python autograder.py -q q2
    python autograder.py -t "test_cases/q10/8-pacman-game"
    python autograder.py -q q5 --no-graphics
    python autograder.py -q q5

    python autograder.py -t "test_cases/q10/1-1-minmax"

    python main.py -p AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better
    python main.py -p AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better --graphics GraphicsPacmanNull
    
    
    ??????????
    python main.py -p AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better --graphics FirstPersonGraphics
    ??????

    autograder -q q4
    autograder -t "test_cases/multiagent/q12/7-pacman-game"

    python main.py --quietTextGraphics
    python main.py -l mediumScaryMaze -p StayWestSearchAgent
    
    python main.py -l mediumScaryMaze -p AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better

    # Standard map stuff
    python main.py -l originalClassic -p AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better
    
# 
    python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic 
















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

