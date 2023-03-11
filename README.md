
# Remake of UC Berkeley Pacman Assignment

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


# Guaranteed to work

    main -ap AgentGoWest
    main -gs "AgentGhostRandom AgentGhostRandom AgentGhostRandom"
    main -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic 
    main -ap PacmanQAgent -x 2000 -n 2010 -l smallGrid 
    main -l mediumScaryMaze -p StayWestSearchAgent
    main --quietTextGraphics
    main -p AgentPacmanMinimaxAlphaBeta -a evaluation_function=evaluation_function_better
    autograder -q q4
    autograder -q q2
    autograder -q q5
    autograder -q q12
    autograder -q q23
    autograder -q q24
    
    autograder -t "test_cases/q11/2-1a-vary-depth"
    autograder -q q9 --no-graphics
    autograder -t "test_cases/multiagent/q4/7-pacman-game"
    autograder -t "test_cases/q10/1-1-minmax"
    gridworld.py -g MazeGrid
    gridworld.py -a q -K 5 -m ???????????????
    
    # QUESTIONABLE, NEED TO CHANGE THE RULES FOR GHOSTS SO THEY MOVE IF MAKING AN ILLEGAL MOVE
    main -ap AgentPacmanExpectimax -ags "[AgentPacmanGhostRandom(), AgentGoWest(), AgentPacmanGhostDirectional()]"  
    
    # FINE
    main -ap AgentPacmanExpectimax -ags "[AgentPacmanGhostRandom(), AgentPacmanGhostDirectional(), AgentPacmanGhostDirectional()]"
#####################################################################

# JOSEPH FIX THIS BELOW

CHECK .test FILES FOR THE BELOW JOSEPH

class: "EvalAgentTest"  # Q23 IS UNIQUE

OR

ghosts: 

OR

pacmanParams:

###

SearchProblem USE self.set_graphics and self.graphics WHICH CAME FROM 
AN Agent get_graphics set_graphics

getGhostStates -> get_list_container_state_ghost for StatePacman

PacmanGameTreeTest and GraphGameTreeTest SHARE AN AGENT MAKE A CLASS FOR THEIR SHARED AGENT
THE PROBLEMS ARE WITH q10

#####

.initialize(lay, 0) Look for this and replace it

######

### Question q9: 2/4 ### Pacman EvalAgentTest   # FIXED
### Question q10: 0/5 ### Pacman PacmanGameTreeTest
### Question q11: 0/5 ### Pacman PacmanGameTreeTest
### Question q12: 0/5 ### Pacman PacmanGameTreeTest
### Question q14: 0/0 ###  # NEED BETTER ALGO


###########################################################################

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
      
   
      virtualenv .venv -p python3.11
   
   3. Activate virtual environment (Unix)

      
      source .venv/bin/activate

   3. Activate virtual environment (Windows)
   
      
      .venv/Scripts/activate

   4. Install Requirements
   
      
      pip install requirements.txt
