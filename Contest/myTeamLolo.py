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


#Agents can only observe an opponent's configuration (position and direction) if they or their teammate is within 5 squares (Manhattan distance)
#getAgentDistances :  list of noisy distance observations. noise is chosen uniformly at random from the range [-6, 6] is chosen with probability 1/13)
#getDistanceProb : get the likelihood of a noisy reading "Returns the probability of a noisy distance given the true distance"
# distanceCalculator.py to supply shortest path maze distances

#https://github.com/junkumar/pactureflag/blob/master/teams/PactureFlag/baselineAgents.py
#https://github.com/mrin17/PacmanCTF/blob/master/Code/myTeam.py

#on CaptureAgent.py
#getPreviousObservation(self):Returns the GameState object corresponding to the last state this agent saw (the observed state of the game last time this agent moved - this may not include all of your opponent's agent locations exactly).
#getCurrentObservation(self):Returns the GameState object corresponding this agent's current observation (the observed state of the game - this may not include all of your opponent's agent locations exactly).

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

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
    observedState = self.getCurrentObservation()
    self.elapseTime(observedState)
    self.observeState(observedState)
    

    return random.choice(actions)



  def setValidPositions(self, gameState):
    self.validPositions = []
    walls = gameState.getWalls()
    for x in range(walls.width):
      for y in range(walls.height):
        if not walls[x][y]:
          self.validPositions.append((x,y))


#-----------------------------------BELIEF------------------------------
  #numParticles
  def Initializes(self,gameState):
    self.numGhosts = len( self.getOpponents(gameState)) 
    self.distancer = Distancer(gameState.data.layout)

  def setNumParticles(self, numParticles):
    self.numParticles = numParticles

  def initializeParticles(self):
    possiblePos= list(itertools.product(self.validPositions, repeat = self.numGhosts)) #liste de produit cardinal de toutes les combianisons possible de fantomes
    random.shuffle(possiblePos) #on melange pour uniformiser la liste

    self.particles = [] #create particles as a List
    for count in range(self.numParticles): #tant que nous n'avons pas parcourue toute les particules
      for p in possiblePos: #pour chaque combinaison de posistion possible des fantomes
        if count < self.numParticles: 
          self.particles.append(p) #on rajoute la position dans la particule

  def observeState(self, gameState):
    #la position du pacman
    pacmanPosition = gameState.getAgentPosition(self.index) 
    
    #donne la liste des vrais distances entre Pacman et toute position valide
    trueDistances = []
    for p in self.validPositions:
      #trueDistances.append(util.manhattanDistance(p, pacmanPosition))
      trueDistances.append(distancer.getDistance( (p, pacmanPosition ) ) )

    #liste les observztions sur chaque agent ennemi
    noisyDistances = []
    for agent in self.getOpponents(observedState):
      noisyDistances.append(gameState.getAgentDistances()[agent])

    #si probleme
    if len(noisyDistances) < self.numGhosts:
      return
    
    #Emission Model pour chaque agent ennemi et position valide
    #emissionModels = [gameState.getDistanceProb(trueDistance, noisyDistance) for trueDistance in trueDistances, for noisyDistance in noisyDistances]

    allPossible = util.Counter() #where to store beliefs

    oldBelief = self.getBeliefDistribution() #old beliefs distribution

    for particle in self.particles:#for each tuple particle
      partial = 1.0
      for i in range(self.numGhosts): #for each ghost
        trueDistance = distancer.getDistance( (particle[i], pacmanPosition ) ) #calculate distance between pacman and the ghost i in poistion of the particle
        partial = partial * gameState.getDistanceProb(trueDistance, noisyDistances[i]) #for each ghost, we change the particles "partial" emiision model (probability of the noisy distance) given the ghost and the true distance
      allPossible[particle] = allPossible[particle] + partial #the value of the probability of this particle is the old value + noisyProbability (ca a change car beliefs est par rapport a particule maintenant)

    if not any(allPossible.values()): #si ils sont tous a 0
      self.initializeParticles() #on re-crer a partir d'ancienne distribution
    else:#cas normal
      allPossible.normalize() #normilise to add up to one
      temp = [] #temporary particle list
      for _ in range(0, self.numParticles): #pour chaque particule
        temp.append(util.sample(allPossible)) # generate a sample from a belief distribution
      self.particles = temp #enregistre pour de bon


  def elapseTime(self, gameState):
    newParticles = []
    for oldParticle in self.particles:
      newParticle = list(oldParticle) # A list of ghost positions

      # now loop through and update each entry in newParticle...
      for i in range(self.numGhosts): #for each ghost
        newPosDist = self.getBeliefDistribution()#getPositionDistributionForGhost(setGhostPositions(gameState, newParticle), i, self.ghostAgents[i]) 
        # distributions over new positions for that single ghost, given the list of previous positions of ALL of the ghosts
        newParticle[i] = util.sample(newPosDist) #generate a sample from a belief distribution
      
      newParticles.append(tuple(newParticle)) #add this to the particles
    self.particles = newParticles

  def getBeliefDistribution(self):
      #converti la list de particule en objet counter pour la distribution de probabilite
      distribution = util.Counter()#creer le Counter
      for element in self.particles: #pour chaque particule
          distribution[element] = distribution[element] + 1 #mettre dans le dictionaire, et le poid dans le dictionaire de +1
      distribution.normalize()
      return distribution

  def getMostLikelyPosition(self, agent):
    return self.getBeliefDistribution[agent].argMax()











#Transition model----------------INCOMPLET-------------------------------
def getPositionDistributionForGhost(gameState, ghostIndex, agent):
  """
  Returns the distribution over positions for a ghost, using the supplied
  gameState.
  """
  # index 0 is pacman
  ghostPosition = gameState.getGhostPosition(ghostIndex+1)
  actionDist = agent.getDistribution(gameState)
  dist = util.Counter()
  for action, prob in actionDist.items():
      successorPosition = game.Actions.getSuccessor(ghostPosition, action)
      dist[successorPosition] = prob
  return dist

def setGhostPositions(gameState, ghostPositions):
  "Sets the position of all ghosts to the values in ghostPositionTuple."
  for index, pos in enumerate(ghostPositions):
      conf = game.Configuration(pos, game.Directions.STOP)
      gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
  return gameState
