"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/23/2022

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""

class GameState:


    def getLegalActions(self, agentIndex=0):
        """
        Returns the legal actions for the agent specified.
        """
        #        GameState.explored.add(self)
        if self.isWin() or self.isLose():
            return []

        if agentIndex == 0:  # Pacman is moving
            return PacmanRules.getLegalActions(self)
        else:
            return GhostRules.getLegalActions(self, agentIndex)

    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor state after the specified agent takes the action.
        """
        # Check that successors exist
        if self.isWin() or self.isLose():
            raise Exception('Can\'t generate a successor of a terminal state.')

        # Copy current state
        state = GameState(self)

        # Let agent's logic deal with its action's effects on the board
        if agentIndex == 0:  # Pacman is moving
            state.data._eaten = [False for i in range(state.getNumAgents())]
            PacmanRules.applyAction(state, action)
        else:  # A ghost is moving
            GhostRules.applyAction(state, action, agentIndex)

        # Time passes
        if agentIndex == 0:
            state.data.scoreChange += -TIME_PENALTY  # Penalty for waiting around
        else:
            GhostRules.decrementTimer(state.data.agentStates[agentIndex])

        # Resolve multi-agent effects
        GhostRules.checkDeath(state, agentIndex)

        # Book keeping
        state.data._agentMoved = agentIndex
        state.data.score += state.data.scoreChange
        GameState.explored.add(self)
        GameState.explored.add(state)
        return state

    def getLegalPacmanActions(self):
        return self.getLegalActions(0)

    def generatePacmanSuccessor(self, action):
        """
        Generates the successor state after the specified pacman move
        """
        return self.generateSuccessor(0, action)

    def getPacmanState(self):
        """
        Returns an AgentState object for pacman (in game.py)

        state.pos gives the current position
        state.direction gives the travel vector
        """
        return self.data.agentStates[0].copy()

    def getPacmanPosition(self):
        return self.data.agentStates[0].getPosition()

    def getGhostStates(self):
        return self.data.agentStates[1:]

    def getGhostState(self, agentIndex):
        if agentIndex == 0 or agentIndex >= self.getNumAgents():
            raise Exception("Invalid index passed to getGhostState")
        return self.data.agentStates[agentIndex]

    def getGhostPosition(self, agentIndex):
        if agentIndex == 0:
            raise Exception("Pacman's index passed to getGhostPosition")
        return self.data.agentStates[agentIndex].getPosition()

    def getGhostPositions(self):
        return [s.getPosition() for s in self.getGhostStates()]

    def getNumAgents(self):
        return len(self.data.agentStates)

    def getScore(self):
        return float(self.data.score)

    def getCapsules(self):
        """
        Returns a list of positions (x,y) of the remaining capsules.
        """
        return self.data.capsules

    def getNumFood(self):
        return self.data.food.count()

    def getFood(self):
        """
        Returns a Grid of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = state.getFood()
        if currentFood[x][y] == True: ...
        """
        return self.data.food

    def getWalls(self):
        """
        Returns a Grid of boolean wall indicator variables.

        Grids can be accessed via list notation, so to check
        if there is a wall at (x,y), just call

        walls = state.getWalls()
        if walls[x][y] == True: ...
        """
        return self.data.layout.walls

    def hasFood(self, x, y):
        return self.data.food[x][y]

    def hasWall(self, x, y):
        return self.data.layout.walls[x][y]

    def isLose(self):
        return self.data._lose

    def isWin(self):
        return self.data._win