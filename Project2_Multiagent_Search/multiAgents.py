# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #distance aux ghosts
        #manhattanDistance distance de bloc a bloc
        closestghost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])

        if closestghost:
            ghost_dist = -10/closestghost
        else:
            ghost_dist = -1000   #s'il n'y a aucun ghost

        #distance a la nourriture
        foodList = newFood.asList()
        if foodList:
            closestfood = min([manhattanDistance(newPos, food) for food in foodList])
        else:
            closestfood = 0

        #calcule un score
        return (-2 * closestfood) + ghost_dist - (100*len(foodList))
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        numberOfGhosts = gameState.getNumAgents() - 1

        #Score maximal pour le Pacman
        def maxLevel(gameState,depth):
            currDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currDepth==self.depth:   #Terminal test
                return self.evaluationFunction(gameState)
            maxvalue = -999999
            actionList = gameState.getLegalActions(0)   #liste des actions legales pour le pacman
            for action in actionList:
                successor= gameState.generateSuccessor(0,action)    #les coups laissés au choix du fantome
                maxvalue = max (maxvalue,minLevel(successor,currDepth,1))   #fonction reccursive minimax

            return maxvalue


        #Score minimal pour un ghost
        def minLevel(gameState,depth, agentIndex):
            minvalue = 999999
            if gameState.isWin() or gameState.isLose():   #Terminal test
                return self.evaluationFunction(gameState)
            actionList = gameState.getLegalActions(agentIndex)

            for action in actionList:
                successor= gameState.generateSuccessor(agentIndex,action)
                if agentIndex == (gameState.getNumAgents() - 1):
                    minvalue = min (minvalue,maxLevel(successor,depth))
                else:
                    minvalue = min(minvalue,minLevel(successor,depth,agentIndex+1))

            return minvalue


        #Root level action.  = determine l'action suivante
        actions = gameState.getLegalActions(0)      #liste des actions du pacman
        currentScore = -999999
        returnAction = ''

        #trouve l'action du pacman qui generera le score le moins faible possible
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)

            # Next level is a min level. Hence calling min for successors of the root.
            score = minLevel(nextState,0,1)

            # Choosing the action which is Maximum of the successors.
            if score > currentScore:   #a l'avantage du Pacman
                returnAction = action
                currentScore = score

        return returnAction
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):


    def getAction(self, gameState):

        #Score maximal pour le Pacman
        def maxLevel(gameState,depth,alpha, beta):
            currDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currDepth==self.depth:   #Terminal Test
                return self.evaluationFunction(gameState)
            maxvalue = -999999
            actions = gameState.getLegalActions(0)   #liste des actions legales pour le pacman
            alpha1 = alpha
            for action in actions:
                successor= gameState.generateSuccessor(0,action)    #les coups laissés au choix du fantome
                maxvalue = max (maxvalue,minLevel(successor,currDepth,1,alpha1,beta))   #fonction reccursive minimax
                if maxvalue > beta:
                    return maxvalue
                alpha1 = max(alpha1,maxvalue)

            return maxvalue



        #Score minimal pour un ghost
        def minLevel(gameState,depth,agentIndex,alpha,beta):
            minvalue = 999999
            if gameState.isWin() or gameState.isLose():   #Terminal Test
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex)
            beta1 = beta
            for action in actions:
                successor= gameState.generateSuccessor(agentIndex,action)
                if agentIndex == (gameState.getNumAgents()-1):
                    minvalue = min (minvalue,maxLevel(successor,depth,alpha,beta1))
                    if minvalue < alpha:
                        return minvalue
                    beta1 = min(beta1,minvalue)
                else:
                    minvalue = min(minvalue,minLevel(successor,depth,agentIndex+1,alpha,beta1))
                    if minvalue < alpha:
                        return minvalue
                    beta1 = min(beta1,minvalue)

            return minvalue



        # Alpha-Beta Pruning
        actions = gameState.getLegalActions(0)
        currentScore = -999999
        returnAction = ''
        alpha = -999999
        beta = 999999
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            # Next level is a min level. Hence calling min for successors of the root.
            score = minLevel(nextState,0,1,alpha,beta)
            # Choosing the action which is Maximum of the successors.
            if score > currentScore:
                returnAction = action
                currentScore = score
            # Updating alpha value at root.
            if score > beta:
                return returnAction
            alpha = max(alpha,score)  #calcul du meilleur coup pour Pacman

        return returnAction
        #util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        #methode classique recherche valeur max pour le pacman
        def maxLevel(gameState,depth):
            currDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currDepth==self.depth:   #Terminal Test
                return self.evaluationFunction(gameState)

            maxvalue = -999999
            actions = gameState.getLegalActions(0)
            totalmaxvalue = 0
            numberofactions = len(actions)

            for action in actions:
                successor= gameState.generateSuccessor(0,action)
                maxvalue = max (maxvalue,expectLevel(successor,currDepth,1))
            return maxvalue


        #Estimation du la valeur min des ghosts
        def expectLevel(gameState,depth, agentIndex):
            if gameState.isWin() or gameState.isLose():   #Terminal Test
                return self.evaluationFunction(gameState)

            actions = gameState.getLegalActions(agentIndex)
            totalexpectedvalue = 0
            numberofactions = len(actions)

            for action in actions:
                successor= gameState.generateSuccessor(agentIndex,action)
                if agentIndex == (gameState.getNumAgents() - 1):
                    expectedvalue = maxLevel(successor,depth)
                else:
                    expectedvalue = expectLevel(successor,depth,agentIndex+1)

                totalexpectedvalue = totalexpectedvalue + expectedvalue

            if numberofactions == 0:
                return  0
            return float(totalexpectedvalue)/float(numberofactions)


        #Root level action.   (le meme que dans minimax)
        actions = gameState.getLegalActions(0)
        currentScore = -999999
        returnAction = ''
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)

            # Next level is a expect level. Hence calling expectLevel for successors of the root.
            score = expectLevel(nextState,0,1)

            # Choosing the action which is Maximum of the successors.
            if score > currentScore:
                returnAction = action
                currentScore = score
        return returnAction

        #util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    """ Manhattan distance to the foods from the current state """
    foodList = newFood.asList()
    from util import manhattanDistance
    foodDistance = [0]
    for pos in foodList:
        foodDistance.append(manhattanDistance(newPos,pos))

    """ Manhattan distance to each ghost from the current state"""
    ghostPos = []
    for ghost in newGhostStates:
        ghostPos.append(ghost.getPosition())
    ghostDistance = [0]
    for pos in ghostPos:
        ghostDistance.append(manhattanDistance(newPos,pos))

    numberofPowerPellets = len(currentGameState.getCapsules())

    score = 0
    numberOfNoFoods = len(newFood.asList(False))
    sumScaredTimes = sum(newScaredTimes)
    sumGhostDistance = sum (ghostDistance)
    reciprocalfoodDistance = 0
    if sum(foodDistance) > 0:
        reciprocalfoodDistance = 1.0 / sum(foodDistance)

    score += currentGameState.getScore()  + reciprocalfoodDistance + numberOfNoFoods

    if sumScaredTimes > 0:
        score +=   sumScaredTimes + (-1 * numberofPowerPellets) + (-1 * sumGhostDistance)
    else :
        score +=  sumGhostDistance + numberofPowerPellets

    return score


# Abbreviation
better = betterEvaluationFunction
