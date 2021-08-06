import time
import Encoder
import numpy as np
from adafruit_servokit import ServoKit
from Sensor import Sensor

class Environment:
    def __init__(self, servoArmNumberOfStates, servoHandNumberOfStates, numberOfActions):
        self.numberOfActions = numberOfActions
        
        #This delay time allows the servos to set their position and the crawler to roll
        self.delayTime = 0.2
        
        #Parameters of Rotary Encoder
        self.wheel = Encoder.Encoder(17, 18)
        #Paramters of Ultrasonic Sensor
        self.sensor = Sensor()
        self.lastDistance = 0
      
        #Initialize Adafruit Servo Kit  
        kit = ServoKit(channels=16)

        #Set Parameters for ServoArm
        self.servoArm = kit.servo[0]
        self.servoArmNumberOfStates = servoArmNumberOfStates
        self.servoArmInitialAngle = 127.0
        self.servoArmCurrentAngle = self.servoArmInitialAngle
        self.servoArmMinAngle = 120.0
        self.servoArmMaxAngle = 160.0
        self.servoArmStepAngle = int((self.servoArmMaxAngle-self.servoArmMinAngle)/(self.servoArmNumberOfStates-1))
        self.servoArmInitialState=int(((self.servoArmInitialAngle-self.servoArmMinAngle)/self.servoArmStepAngle)) #This is an integer between zero and numOfStates-1 used to index the state number of servo

        #Set Parameters for ServoHand
        self.servoHand = kit.servo[15]
        self.servoHandNumberOfStates = servoHandNumberOfStates
        self.servoHandInitialAngle = 84.0
        self.servoHandCurrentAngle = self.servoHandInitialAngle
        self.servoHandMinAngle = 0.0
        self.servoHandMaxAngle = 140.0
        self.servoHandStepAngle = int((self.servoHandMaxAngle-self.servoHandMinAngle)/(self.servoHandNumberOfStates-1))
        self.servoHandInitialState=int(((self.servoHandInitialAngle-self.servoHandMinAngle)/self.servoHandStepAngle))
        
        #Define the initial state of the environment
        self.state = (self.servoArmInitialState, self.servoHandInitialState)

    #A setup method that will put the servos into their initial angle
    def setup(self):
        self.servoArm.angle = self.servoArmInitialAngle
        time.sleep(self.delayTime)
        self.servoHand.angle = self.servoHandInitialAngle
        time.sleep(self.delayTime)
        print("Setup completed")

    #This method returns the number of actions to the agent
    def getNumberOfActions(self):
        return self.numberOfActions

    #This method will physically execute the chosen action and will get the next states for Arm and Hand
    def move(self, actionIndex, lastDistance):
        servoArmCurrentState, servoHandCurrentState = self.state
        servoArmNewState = servoArmCurrentState
        servoHandNewState = servoHandCurrentState
        negativeReward = False

        #Action 0
        if actionIndex == 0 and servoArmCurrentState < (self.servoArmNumberOfStates-1):
            servoArmNewState += 1
            self.servoArmNextAngle = self.servoArmCurrentAngle + self.servoArmStepAngle
            self.servoArm.angle = self.servoArmNextAngle
            self.servoArmCurrentAngle = self.servoArmNextAngle
            print("Current Angle after action zero is " + str(self.servoArmCurrentAngle))
            time.sleep(self.delayTime)
        elif actionIndex == 0 and servoArmCurrentState >= (self.servoArmNumberOfStates-1):
            print ("Action is not allowed!!!")
            negativeReward = True

        #Action 1
        elif actionIndex == 1 and servoArmCurrentState != 0:
            servoArmNewState -= 1
            self.servoArmNextAngle = self.servoArmCurrentAngle - self.servoArmStepAngle
            self.servoArm.angle = self.servoArmNextAngle
            self.servoArmCurrentAngle = self.servoArmNextAngle
            print("Current Angle after action one is " + str(self.servoArmCurrentAngle))
            time.sleep(self.delayTime)
        elif actionIndex == 1 and servoArmCurrentState == 0:
            print ("Action is not allowed!!!")
            negativeReward = True
        
        #Action 2
        elif actionIndex == 2 and servoHandCurrentState < (self.servoHandNumberOfStates-1):
            servoHandNewState += 1
            self.servoHandNextAngle = self.servoHandCurrentAngle + self.servoHandStepAngle
            self.servoHand.angle = self.servoHandNextAngle
            self.servoHandCurrentAngle = self.servoHandNextAngle
            print("Current Angle after action two is " + str(self.servoHandCurrentAngle))
            time.sleep(self.delayTime)
        elif actionIndex == 2 and servoHandCurrentState >= (self.servoHandNumberOfStates-1):
            print ("Action is not allowed!!!")
            negativeReward = True

        #Action 3
        elif actionIndex == 3 and servoHandCurrentState != 0:
            servoHandNewState -= 1
            self.servoHandNextAngle = self.servoHandCurrentAngle - self.servoHandStepAngle
            self.servoHand.angle = self.servoHandNextAngle
            self.servoHandCurrentAngle = self.servoHandNextAngle
            print("Current Angle after action three is " + str(self.servoHandCurrentAngle))
            time.sleep(self.delayTime)
        elif actionIndex == 3 and servoHandCurrentState == 0:
            print ("Action is not allowed!!!")
            negativeReward = True

        #currentDistance = self.sensor.read()
        currentDistance = self.wheel.read()
        if negativeReward != True:
            deltaDistance = currentDistance - lastDistance
            reward = (deltaDistance*20)*(-1)
        else:
            deltaDistance = 0
            reward = deltaDistance

        lastDistance = currentDistance

        self.state = (servoArmNewState, servoHandNewState)
        return np.array(self.state), lastDistance, reward

