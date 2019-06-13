# myTeam.py
# ---------
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
from game import Agent
import game


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'AlphaBetaAgent', second = 'AlphaBetaAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.

    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)


class AlphaBetaAgent(CaptureAgent):
    evalFn = 'scoreEvaluationFunction'
    index = 0
    depth = 2

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)



    def evalFunctionPacman(self, currentGameState, agentIndex):

        # Useful information you can extract from a GameState (pacman.py)
        #successor= gameState.generateSuccessor(agentIndex,action)
        newPos = currentGameState.getPosition()
        newFood = currentGameState.getFood()
        newGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        """ Informations de position et d'etat en consderant les index 1,3 et 2,4 """

        #disctance aux ghosts
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


    #def evaluatFunctionPacman(self, currentGameState, action):


    def chooseAction(self, gameState):


        def scoreEvaluationFunction(currentGameState):
             return currentGameState.getScore()

        #Score maximal pour le Pacman
        def maxLevel(gameState,depth,agentIndex):

            currDepth = depth + 1
            if gameState.isOver() or currDepth==self.depth:   #Terminal Test
                return evalFunctionPacman(gameState, agentIndex)
            maxvalue = -999999
            actions = gameState.getLegalActions(0)   #liste des actions legales pour le pacman
            for action in actions:
                successor= gameState.generateSuccessor(0,action)

                """ 1er Agent de notre equipe"""
                if agentIndex==0:
                    maxvalue = max (maxvalue,minLevel(successor,currDepth,1))

                """ 2eme Agent de notre equipe"""
                if agentIndex==2:
                    maxvalue = max (maxvalue,minLevel(successor,currDepth,3))

            return maxvalue

        #Score minimal pour un ghost
        def minLevel(gameState,depth,agentIndex):

            minvalue = 999999
            if gameState.isOver():   #Terminal Test
                return evalFunctionPacman(gameState, agentIndex)
            actions = gameState.getLegalActions(agentIndex)

            for action in actions:
                successor= gameState.generateSuccessor(agentIndex,action)

                """ 1er Agent de l'equipe adverse"""
                if agentIndex==1:
                    minvalue = min (minvalue,maxLevel(successor,depth,2))

                """ 2eme Agent de l'equipe adverse"""
                if agentIndex==3:
                    minvalue = min(minvalue,minLevel(successor,depth,(agentIndex+1)%4))


            return minvalue

        actions = gameState.getLegalActions(0)
        currentScore = -999999
        returnAction = ''
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            # Next level is a min level. Hence calling min for successors of the root.
            score = minLevel(nextState,0,1)
            # Choosing the action which is Maximum of the successors.
            if score > currentScore:
                returnAction = action
                currentScore = score

        return returnAction
