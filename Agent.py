import Environment

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
qValues = np.full((Crawler.numberServoArmStates, numberServoHandStates, numActions), 10, dtype=np.int32)
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
        return np.argmax(q_values[int(state[0]), int(state[1])])
    else: #choose a random action
        print("Random Action")
        return np.random.randint(4)