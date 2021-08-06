from Environment import Environment
import numpy as np
import time
import math

Crawler = Environment(4, 4, 4)

Crawler.setup()

#Setting the parameters for Q-Learning
discountFactor = 0.9 #discount factor for future rewards
learningRate = 0.9 #the rate at which the AI agent should learn
EPISODES = 500
totalReward = 0

#Initializing the Q table with all ones
#There are four columns for the four actions
#And there are 36 rows for 6x6 states (each of the two arms can have 6 states)
#numStates = numTheta1States*numTheta2States
numActions = Crawler.getNumberOfActions()
qValues = np.full((Crawler.servoArmNumberOfStates, Crawler.servoHandNumberOfStates, numActions), 1, dtype=np.int32)
print("Q-Table at starting point")
print(qValues)

def getEpsilon(time, EPISODES):
    A=0.5
    B=0.1
    C=0.1
    standardizedTime=(time-A*EPISODES)/(B*EPISODES)
    cosh=np.cosh(math.exp(-standardizedTime))
    epsilon=1.1-(1/cosh+(time*C/EPISODES))
    return epsilon

#define an epsilon algorithm that will choose which action to take next (i.e., where to move next)
def getNextAction(state, epsilon):
    #if a randomly chosen value between 0 and 1 is less than epsilon, 
    #then choose the most promising value from the Q-table for this state.
    if np.random.random() > epsilon:
        print("Action from Q-table")
        return np.argmax(qValues[int(state[0]), int(state[1])])
    else: #choose a random action
        print("Random Action")
        return np.random.randint(4)

Observations = 21
listOfObservations = np.zeros((EPISODES, Observations))

for t in range (0, EPISODES):
    print ("Loop No. " + str(t))
    epsilon = getEpsilon(t, EPISODES)
    print ("Epsilon " + str(epsilon))
    actionIndex = getNextAction(Crawler.state, epsilon)
    print ("The next action is action No. " + str(actionIndex))

    servoArmOldState, servoHandOldState = Crawler.state #store the old row and column indexes

    Crawler.state, Crawler.lastDistance, reward = Crawler.move(actionIndex, Crawler.lastDistance)
    print ("The current reward is "+str((reward)))
    servoArmNewState, servoHandNewState = Crawler.state
    time.sleep(0.2)

    #Receive the reward for moving to the new state, and calculate the temporal difference
    oldQValue = qValues[servoArmOldState, servoHandOldState, actionIndex]
    temporalDifference = reward + (discountFactor * np.max(qValues[int(Crawler.state[0]), int(Crawler.state[1])])) - oldQValue 

    #Update the Q-value for the previous state and action pair
    newQValue = oldQValue + (learningRate * temporalDifference)
    qValues[servoArmOldState, servoHandOldState, actionIndex] = newQValue

    totalReward = totalReward + reward 

    deltaDistance = reward / 20
    
    listOfObservations[t,:] = [
        t, 
        actionIndex, 
        reward, 
        totalReward,
        epsilon, 
        Crawler.lastDistance,
        deltaDistance,
        oldQValue,
        temporalDifference,
        newQValue,
        servoArmOldState,
        Crawler.servoArmCurrentAngle,
        servoArmNewState,
        servoHandOldState,
        Crawler.servoHandCurrentAngle,
        servoHandNewState,
        Crawler.servoArmNumberOfStates,
        Crawler.servoHandNumberOfStates,
        numActions,
        discountFactor,
        learningRate,
        ]

    t = t+1

    if t==EPISODES:
        training = False
        print("Training completed")
        print(qValues)
        print(totalReward)
        np.save(f"observations/observations.npy", listOfObservations)  