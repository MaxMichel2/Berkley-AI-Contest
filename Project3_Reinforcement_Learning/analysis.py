# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0 # Default noise was 0.2, with noise = 0, the agent ignores the surrounding negative reward cells and aims straight for the exit
    return answerDiscount, answerNoise

def question3a(): # Prefer the close exit (+1), risking the cliff (-10)
    answerDiscount = 0.2 # The longer you stay, the less you get
    answerNoise = 0 # We want to "risk the cliff" as in walk along it
    answerLivingReward = -0.2 # Living is expensive so get out quickly
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b(): # Prefer the close exit (+1), but avoiding the cliff (-10)
    answerDiscount = 0.2 # Rewards are worth 80% less each time
    answerNoise = 0.2 # 20% chance to have a wrong move so the Agent will avoid any direction containing the cliff
    answerLivingReward = -0.2 # Costs a lot to stay in the game
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c(): # Prefer the distant exit (+10), risking the cliff (-10)
    answerDiscount = 0.9 # Rewards don't lose too much value with time so the big reward for the furthest exit becomes more appealing
    answerNoise = 0 # We want to "risk the cliff" as in walk along it
    answerLivingReward = 0 # Doesn't cost anything to stay alive
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d(): # Prefer the distant exit (+10), avoiding the cliff (-10)
    answerDiscount = 0.9 # Rewards don't lose too much value with time so the big reward for the furthest exit becomes more appealing
    answerNoise = 0.2 # 20% chance to have a wrong move so the Agent will avoid any direction containing the cliff
    answerLivingReward = 0 # Doesn't cost anything to stay alive
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e(): # Avoid both exits and the cliff (so an episode should never terminate)
    answerDiscount = 1 # No discount, rewards are always worth their initial value
    answerNoise = 0 # Go anywhere
    answerLivingReward = 0.1 # The longer you stay, the more you get
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
	answerEpsilon = None
	answerLearningRate = None
	# return answerEpsilon, answerLearningRate
	# If not possible, return 'NOT POSSIBLE'
	return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
