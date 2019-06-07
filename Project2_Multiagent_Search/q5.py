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




#autre methode qui ne marche pas
newPos = currentGameState.getPacmanPosition()
newFood = currentGameState.getFood()
newGhostStates = currentGameState.getGhostStates()
newCapsules = currentGameState.getCapsules()
newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

closestGhost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
if newCapsules:
    closestCapsule = min([manhattanDistance(newPos, caps) for caps in newCapsules])
else:
    closestCapsule = 0

if closestCapsule:
    closest_capsule = -3 / closestCapsule
else:
    closest_capsule = 100

if closestGhost:
    ghost_distance = -2 / closestGhost
else:
    ghost_distance = -500

foodList = newFood.asList()
if foodList:
    closestFood = min([manhattanDistance(newPos, food) for food in foodList])
else:
    closestFood = 0

return -2 * closestFood + ghost_distance - 10 * len(foodList) + closest_capsule
