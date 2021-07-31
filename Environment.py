import time
import Encoder
import numpy as np
import Servo

class Environment:
    def __init__(self, numberServoArmStates, numberServoHandStates, numberOfActions):
        self.numberServoArmStates = numberServoArmStates
        self.numberServoHandStates = numberServoHandStates
        self.numberOfActions = numberOfActions
        
        #This delay time allows the servos to set their position and the crawler to roll
        self.delayTime = 0.2
        
        #Parameters of Rotary Encoder
        self.wheel = Encoder.Encoder(17, 18)
        self.lastDistance = 0

        #Define the initial state of the environment
        self.state = (self.ServoArm.initialServoState, self.ServoHand.initialServoState)
        
        #Setup of Servo Arm
        self.servoArm = Servo(0, self.numberServoArmStates, 127.0, 120.0, 160.0)

        #Setup of Servo Hand
        self.servoHand = Servo(15, self.numberServoHandStates, 84.0, 0.0, 140.0)

    #A setup method that will put the servos into their initial angle
    def setup(self):
        self.servoArm.angle = self.servoArm.initialAngle
        time.sleep(self.delayTime)
        self.servoHand.angle = self.servoHand.initialAngle
        time.sleep(self.delayTime)
        print("Setup completed")

    #This method returns the number of actions to the agent
    def getNumberOfActions(self):
        return self.numberOfActions

    #This method will physically execute the chosen action and will get the next states for Arm and Hand
    def move(self, actionIndex, lastDistance):
        currentServoArmState, currentServoHandState = self.state
        newServoArmState = currentServoArmState
        newServoHandState = currentServoHandState
        negativereward = False

        #Action 0
        if actionIndex == 0 and currentServoArmState < (self.numberServoArmStates-1):
            newServoArmState += 1
            self.ServoArmNextAngle = self.ServoArm.currentAngle + self.ServoArm.stepAngle
            self.ServoArm.angle = self.ServoArmNextAngle
            self.servoArm.currentAngle = self.self.ServoArmNextAngle
            print("Current Angle after action zero is " + str(self.ServoArm.currentAngle))
            time.sleep(self.delayTime)
        elif actionIndex == 0 and currentServoArmState >= (self.numberServoArmStates-1):
            print ("Action is not allowed!!!")
            negativereward = True

        #Action 1
        elif actionIndex == 1 and currentServoArmState != 0:
            newServoArmState -= 1
            self.ServoArmNextAngle = self.ServoArm.currentAngle - self.ServoArm.stepAngle
            self.ServoArm.angle = self.ServoArmNextAngle
            self.servoArm.currentAngle = self.self.ServoArmNextAngle
            print("Current Angle after action one is " + str(self.ServoArm.currentAngle))
            time.sleep(self.delayTime)
        elif actionIndex == 1 and currentServoArmState == 0:
            print ("Action is not allowed!!!")
            negativereward = True
        
        #Action 2
        elif actionIndex == 2 and currentServoHandState < (self.numberServoHandStates-1):
            newServoHandState += 1
            self.ServoHandNextAngle = self.ServoHand.currentAngle + self.ServoHand.stepAngle
            self.ServoHand.angle = self.ServoHandNextAngle
            self.servoHand.currentAngle = self.self.ServoHandNextAngle
            print("Current Angle after action zero is " + str(self.ServoHand.currentAngle))
            time.sleep(self.delayTime)
        elif actionIndex == 2 and currentServoHandState >= (self.numberServoHandStates-1):
            print ("Action is not allowed!!!")
            negativereward = True

        #Action 3
        elif actionIndex == 3 and currentServoHandState != 0:
            newServoHandState -= 1
            self.ServoHandNextAngle = self.ServoHand.currentAngle - self.ServoHand.stepAngle
            self.ServoHand.angle = self.ServoHandNextAngle
            self.servoHand.currentAngle = self.self.ServoHandNextAngle
            print("Current Angle after action one is " + str(self.ServoHand.currentAngle))
            time.sleep(self.delayTime)
        elif actionIndex == 3 and currentServoHandState == 0:
            print ("Action is not allowed!!!")
            negativereward = True

        currentDistance = self.wheel.read()
        if negativereward != True:
            deltaDistance = currentDistance - lastDistance
            reward = deltaDistance*20
        else:
            deltaDistance = 0
            reward = deltaDistance

        lastDistance = currentDistance

        self.state = (newServoArmState, newServoHandState)
        return np.array(self.state), lastDistance, reward

