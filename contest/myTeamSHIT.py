# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from game import Actions

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'GnarAgent', second = 'GnarAgent'):
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

class GnarAgent(CaptureAgent):
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
    self.opponents=self.getOpponents(gameState)
    self.team=self.getTeam(gameState)

  def chooseAction(self, gameState):
      """
        Returns an action.  You can use any method you want and search to any depth you want.
        Just remember that the mini-contest is timed, so you have to trade off speed and computation.

        Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
        just make a beeline straight towards Pacman (or away from him if they're scared!)
      """
      "*** YOUR CODE HERE ***"
      #self.depth=2
      return self.value(gameState, self.index, float("-inf"), float("inf"), 2)[1]

  def value(self, gameState, agentIndex, alpha, beta, depth):
    #terminate when it is a leaf node, i.e. when the game ends
    #if gameState.isWin() or gameState.isLose():
    #  return (self.evaluationFunction(gameState), 'stop')
    #last ghost reached, time to decrease a depth
    if agentIndex == gameState.getNumAgents():
      return self.value(gameState, 0, alpha, beta, depth - 1)
    elif agentIndex in self.opponents: #agent is a ghost
      return self.minvalue(gameState,agentIndex, alpha, beta, depth)
    elif agentIndex in self.team: #agent is pacman
      return self.maxvalue(gameState,agentIndex, alpha, beta, depth)
    else:
      print "ERROR"
      return 0

  def maxvalue(self, gameState, agentIndex, alpha, beta, depth):
    v = float("-inf")
    bestAction = 'stop'
    legalMoves = gameState.getLegalActions(agentIndex) # Collect legal moves and successor states
    for action in legalMoves:
      score = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex+1, alpha, beta, depth)
      if score[0] > v:
        v = score[0]
        bestAction = action
        if v > beta:
          return (v, bestAction)
        alpha = max(v,alpha)
    return (v, bestAction)

  def minvalue(self, gameState, agentIndex, alpha, beta, depth):
    v = float("inf")
    bestAction = 'stop'
     #terminate when agent is the final ghost at depth 0
    if not gameState.getAgentPosition(agentIndex):
      return (v, bestAction) #FUCK
    if agentIndex == (gameState.getNumAgents() - 1) and depth == 0:
      legalMoves = gameState.getLegalActions(agentIndex) # Collect legal moves and successor states
      for action in legalMoves:
        score = self.betterEvaluationFunction(gameState.generateSuccessor(agentIndex, action))
        if score[0]< v:
          bestAction = action
          v = score[0]
          if v < alpha:
            return (v, bestAction)
          beta = min(beta, v)
      return (v, bestAction)
    else: # keep on recursing
      legalMoves = gameState.getLegalActions(agentIndex) # Collect legal moves and successor states
      for action in legalMoves:
        score = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex+1, alpha, beta, depth)
        if score[0] < v:
          v = score[0]
          bestAction = action
          if v < alpha:
            return (v, bestAction)
          beta = min(beta, v)
      return (v, bestAction) 



  def betterEvaluationFunction(self, currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: This evaluation function rewards for the number of food pellets left, penalizes for the distance to the not scared ghosts to Pacman, 
      penalizes for the mazedistance to closest food, penalizes for the maximum manhattan distance to food, penalizes for the manhattan distance to the closest capsule, penalizes for the number of capsules,
      and rewards for a higher game score. It also uses a small random variation to simulate non-optimal play
    """
    "*** YOUR CODE HERE ***"
    from game import Agent

   #  newPos = currentGameState.getPacmanPosition()
   #  newFood = currentGameState.getFood()
   #  newGhostStates = currentGameState.getGhostStates()
   #  #print newGhostStates[0].configuration
   #  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
   #  capsules=currentGameState.getCapsules()
   #  numCapsules=len(capsules)

   #  #calculate the mazeDistance when the Pellet is close 
   #  if numCapsules>0:
   #    Cdist=[]
   #    for xy2 in capsules:
   #      dist = util.manhattanDistance(newPos,xy2)
   #      if dist < 3:
   #        dist = mazeDistance(newPos,xy2,currentGameState)
   #      Cdist.append(dist)
   #    CdistMin=min(Cdist)
   #  else:
   #    CdistMin=99999
   #  if CdistMin==0:
   #    CdistMin=10000

   #  ghostPositions=[newGhostStates[i].getPosition() for i in range(len(newGhostStates))]
   #  foodCount=newFood.count()
   #  GdistsFromP=[util.manhattanDistance(newPos,xy2) for xy2 in ghostPositions]

   #  #only calculates the mazeDistance of Ghosts when it is a short distance, for speed

   #  i = 0
   #  for dist in GdistsFromP:
   #    if dist < 4:
   #      GdistsFromP[i] = mazeDistance(newPos,(int(ghostPositions[i][0]), int(ghostPositions[i][1])),currentGameState)
   #    i = i + 1
   # # GdistsFromP=[mazeDistance(newPos,(int(x2), int(y2)),currentGameState) for (x2,y2) in ghostPositions]

   #  ClosestGdist=min(GdistsFromP)
   #  scaredtimeSum=sum(newScaredTimes)
   #  foodPositions=newFood.asList()
   #  FdistsFromP=[util.manhattanDistance(newPos,xy2) for xy2 in foodPositions]
   #  if not len(FdistsFromP)==0:
   #    FdistMin=closestFoodDistance(currentGameState)
   #    FdistMax=max(FdistsFromP)
   #  else:
   #    FdistMin=0
   #    FdistMax=0

   #  gameScore=currentGameState.getScore()
   #  """
   #  if gameScore>0:
   #    gameScore=currentGameState.getScore()
   #  else:
   #    gameScore=0
   #  """
   #  evalue = 0
   #  i = 0

   #  #if there are scared ghosts, then don't waste pellets
   #  if scaredtimeSum > 0:
   #    evalue+=(2000./float(foodCount+1))+(1./float((FdistMin)+1))+float(numCapsules*2000)+(10./(float(FdistMax)+1))#+(1./float((CdistMin)+1))-(float(100000)/(float(gameScore)+1))
   #    evalue+=100
   #  else:
   #    evalue-=100
   #    evalue+=(2000./float(foodCount+1))+(1./float((FdistMin)+1))-float(numCapsules*50)+(10./(float(FdistMax)+1))+(10./float((CdistMin)+1))#-(float(100000)/(float(gameScore)+1))
   #  evalue += float(gameScore)*20

   #  #use a random number generator to "simulate" non-optimal play
   #  evalue += float(random.randint(0,9))/float(10)

   #  #go through all the ghosts and see if they are scared or not
   #  while i < len(newScaredTimes):
   #    if newScaredTimes[i] == 0: #ghost in question is not scared
   #      #if GdistsFromP[i] < 3:
   #      #the ghost just respawned
   #      if newGhostStates[i].configuration == newGhostStates[i].start:
   #        evalue += 20
   #      else:
   #        evalue -= 1./float(GdistsFromP[i]+1)
   #        evalue -= 20
   #        """
   #        if scaredtimeSum > 0:
   #           if GdistsFromP[i] < 2:
   #            evalue -= 1./float(GdistsFromP[i]+1)       
   #        else:
   #          if min(GdistsFromP) == GdistsFromP[i]:
   #            evalue -= 1./float(GdistsFromP[i]+1)
   #        """
   #    else:
   #       evalue += 10./float(GdistsFromP[i]+1) #ghost in question is scared, so chase it
   #       #evalue += float(gameScore)*200
   #    i = i + 1
    return (self.getScore(currentGameState),1)
