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
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
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

"""
Un agent est en défense s'il est de son côté et en attaque s'il est du côté adverse.
Pathfinding de Marlon pour définir une politique initiale.
Ghostbusters de Lorenzo pour donner une position (x, y) "précise" des adversaires.
Maxime/Cécile définissent une politique de plus en plus compétente.
"""

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
    self.start = gameState.getAgentPosition(self.index)
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
  
  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor
    
  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights
  
  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features
  
  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class ApproxQAgent(CaptureAgent):
  """
  An agent should be able to change from offensive to 
  defensive depending on the information it has access 
  to. What will change is the algorithm used to choose
  actions; Q-learning or Alpha-Beta.
  """
  # All the following function are those used in the Project 3 Approximate Q Agent
  def __init__(self, extractor='IdentityExtractor', actionFn = None, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
    self.featExtractor = util.lookup(extractor, globals())()
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    if actionFn == None:
        actionFn = lambda state: state.getLegalActions()
    self.actionFn = actionFn
    self.episodesSoFar = 0
    self.accumTrainRewards = 0.0
    self.accumTestRewards = 0.0
    self.numTraining = int(numTraining)
    self.epsilon = float(epsilon)
    self.alpha = float(alpha)
    self.discount = float(gamma)
    self.weights = util.Counter()
    self.values = util.Counter()
    
  def final(self, state):
    deltaReward = state.getScore() - self.lastState.getScore()
    self.observeTransition(self.lastState, self.lastAction, state, deltaReward)
    self.stopEpisode()

    # Make sure we have this var
    if not 'episodeStartTime' in self.__dict__:
        self.episodeStartTime = time.time()
    if not 'lastWindowAccumRewards' in self.__dict__:
        self.lastWindowAccumRewards = 0.0
    self.lastWindowAccumRewards += state.getScore()

    NUM_EPS_UPDATE = 100
    if self.episodesSoFar % NUM_EPS_UPDATE == 0:
        print 'Reinforcement Learning Status:'
        windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
        if self.episodesSoFar <= self.numTraining:
            trainAvg = self.accumTrainRewards / float(self.episodesSoFar)
            print '\tCompleted %d out of %d training episodes' % (
                    self.episodesSoFar,self.numTraining)
            print '\tAverage Rewards over all training: %.2f' % (
                    trainAvg)
        else:
            testAvg = float(self.accumTestRewards) / (self.episodesSoFar - self.numTraining)
            print '\tCompleted %d test episodes' % (self.episodesSoFar - self.numTraining)
            print '\tAverage Rewards over testing: %.2f' % testAvg
        print '\tAverage Rewards for last %d episodes: %.2f'  % (
                NUM_EPS_UPDATE,windowAvg)
        print '\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime)
        self.lastWindowAccumRewards = 0.0
        self.episodeStartTime = time.time()

    if self.episodesSoFar == self.numTraining:
        msg = 'Training Done (turning off epsilon and alpha)'
        print '%s\n%s' % (msg,'-' * len(msg))
        
  def observationFunction(self, state):
    """
        This is where we ended up after our last action.
        The simulation should somehow ensure this is called
    """
    if not self.lastState is None:
        reward = state.getScore() - self.lastState.getScore()
        self.observeTransition(self.lastState, self.lastAction, state, reward)
    return state
  
  def getQValue(self, state, action):
    """
		  Should return Q(state,action) = w * featureVector
		  where * is the dotProduct operator
		"""
    "*** YOUR CODE HERE ***"

    return self.getWeights() * self.featExtractor.getFeatures(state, action) # Equivalent to calculating a linear formula
  
  def update(self, state, action, nextState, reward):
    """
		Should update your weights based on transition
		"""
    "*** YOUR CODE HERE ***"

    def multiplyAll(counter, multiplier): # Function to multiply all features by the corresponding (alpha * difference)
      multiplier = float(multiplier)
      for key in counter.keys():
        counter[key] *= multiplier

    difference = reward + self.discount * self.getValue(nextState) - self.getQValue(state, action) # Difference formula from Approximate Q-learning
    features = self.featExtractor.getFeatures(state, action) # Get the features of the environment
    multiplyAll(features, (self.alpha * difference))
    self.weights += features
    
  def getPolicy(self, state):
        return self.computeActionFromQValues(state)

  def getValue(self, state):
      return self.computeValueFromQValues(state)
    
  def computeValueFromQValues(self, state):
    """
    Returns max_action Q(state,action)
    where the max is over legal actions.  Note that if
    there are no legal actions, which is the case at the
    terminal state, you should return a value of 0.0.
    """
    "*** YOUR CODE HERE ***"

    legalActions = self.getLegalActions(state) # Fetch all possible actions at the given state

    if not legalActions: # No legal actions indicates we're in the terminal state
      return 0.0

    return self.getQValue(state, self.getPolicy(state)) # Gets the Q-value from the state and policy at the given state
		
  def computeActionFromQValues(self, state):
		"""
		Compute the best action to take in a state.  Note that if there
		are no legal actions, which is the case at the terminal state,
		you should return None.
		"""
		"*** YOUR CODE HERE ***"

		legalActions = self.getLegalActions(state) # Fetch all possible actions at the given state

		if not legalActions: # No legal actions indicates we're in the terminal state
			return None

		return max(legalActions, key=lambda action: self.getQValue(state, action)) # Get the maximum Q-value and return the corresponding action
  
  def getWeights(self, gameState, action):
    """
    Here is where the weights of the features are determined
    and applied to the game. These weights will change as
    the game evolves and actions are executed.
    """
    return self.weights
  
  def getFeatures(self, gameState, action): 
    """
    Here is the place where features are chose for agents.
    Approximate Q-learning has some defined features
    already and weights are adapted according to the game
    evolution.
    Alpha-Beta also has some pre-defined features and 
    weights also !!!(A vérifier)!!!
    """