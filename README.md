
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

    python main.py -ap AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better
    python main.py -ap AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better --graphics GraphicsPacmanNull
    
    
    ??????????
    python main.py -ap AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better --graphics FirstPersonGraphicsPacman
    ??????

    autograder -q q4
    autograder -t "test_cases/multiagent/q12/7-pacman-game"

    python main.py --quietTextGraphics
    python main.py -l mediumScaryMaze -ap StayWestSearchAgent
    
    python main.py -l mediumScaryMaze -ap AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better

    # Standard map stuff
    python main.py -l originalClassic -ap AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better
    
    # TESTS (DON'T ADD .test)

    autograder -t "test_cases/q11/2-1a-vary-depth"
    
# Q LEARNING PACMAN
    
    # 
    python main.py -ap PacmanQAgent -x 2000 -n 2010 -l smallGrid 

    # 
    python main.py -ap ApproximateQAgent -x 2000 -n 2010 -l smallGrid 

    # ApproximateQAgent
    python main.py -ap ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic 


# ON THE SUBJECT OF GRIDWORLD (CD TO gridworld directory)

    python main.py -a value -i 100 -g BridgeGrid --discount 0.9 --noise 0.2

    python main.py -a q -ng 5 -m
    




CHECK .test FILES FOR THE BELOW JOSEPH

class: "EvalAgentTest"  # Q23 IS UNIQUE

OR

ghosts: 

OR

pacmanParams:

###

SearchProblem USE self.set_graphics and self.graphics WHICH CAME FROM 
AN Agent get_graphics set_graphics


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


# Installing virtual environment (For local installation):
   
   1. Install virtualenv
   
      
      pip install virtualenv

   2. Make virtual environment for python 3.11 (pip install virtualenv)
      
   
      virtualenv .venv -ap python3.11
   
   3. Activate virtual environment (Unix)

      
      source .venv/bin/activate

   3. Activate virtual environment (Windows)
   
      
      .venv/Scripts/activate

   4. Install Requirements
   
      
      pip install requirements.txt
