# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
		"""
		  Your value iteration agent should take an mdp on
		  construction, run the indicated number of iterations
		  and then act according to the resulting policy.

		  Some useful mdp methods you will use:
			  mdp.getStates()
			  mdp.getPossibleActions(state)
			  mdp.getTransitionStatesAndProbs(state, action)
			  mdp.getReward(state, action, nextState)
			  mdp.isTerminal(state)
		"""
		self.mdp = mdp
		self.discount = discount
		self.iterations = iterations
		self.values = util.Counter() # A Counter is a dict with default 0

		# Write value iteration code here
		"*** YOUR CODE HERE ***"
		for i in range(self.iterations): # Will range through all iterations to determine each Vk(s)
			counter = util.Counter()
			for state in mdp.getStates(): # Range through all possible states
				if self.mdp.isTerminal(state): # This means the state value cannot change in the specific iteration
					counter[state] = 0
				else:
					actions = self.mdp.getPossibleActions(state) # Get all possible actions available at a given state
					values = [self.computeQValueFromValues(state, action) for action in actions] # Compute the values of each action
					counter[state] = max(values) # Choose the best possible value (and therefore action) accordingly

			self.values = counter # Change the initial counter to the new one determined above
		

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
		"""
		Compute the Q-value of action in state from the
		value function stored in self.values.
		"""
		"*** YOUR CODE HERE ***"

		stateAndProbs = self.mdp.getTransitionStatesAndProbs(state, action) # Get as the function says, the state and probabilities to compute the Q-value as an array of tuples (state, probability)
		sum = 0

		for nextState, probability in stateAndProbs:
			reward = self.mdp.getReward(state, action, nextState) # Corresponds to R(s, a, s')
			sum += probability * (reward + self.discount * self.values[nextState]) # probability corresponds to the weight given by the transition function T(s, a, s')

		return sum

    def computeActionFromValues(self, state):
		"""
		The policy is the best action in the given state
		according to the values currently stored in self.values.

		You may break ties any way you see fit.  Note that if
		there are no legal actions, which is the case at the
		terminal state, you should return None.
		"""
		"*** YOUR CODE HERE ***"

		if self.mdp.isTerminal(state): # Check the simple case first of reaching the terminal state where the only action is to exit
			return None

		actions = self.mdp.getPossibleActions(state) # Get all possible actions at the given state
		bestAction = max(actions, key = lambda x: self.computeQValueFromValues(state, x)) # Computes the Q-values of each action, finds the max and returns the associated action

		return bestAction

    def getPolicy(self, state):
		return self.computeActionFromValues(state)

    def getAction(self, state):
		"Returns the policy at the state (no exploration)."
		return self.computeActionFromValues(state)

    def getQValue(self, state, action):
		return self.computeQValueFromValues(state, action)
