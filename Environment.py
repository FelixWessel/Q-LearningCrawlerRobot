class Environment:
    def __init__(self, numberServoArmStates, numberServoHandStates, numberOfActions):
        self.numberServoArmStates = numberServoArmStates
        self.numberServoHandStates = numberServoHandStates
        self.numberOfActions = numberOfActions
        
        self.delayTime = 0.2
        
        #Parameters of Rotary Encoder
        self.wheel = Encoder.Encoder(17, 18)
        self.lastDistance = 0

        #Setup of Servo Arm
        self.servoArm = Servo(0, self.numberServoArmStates, 127.0, 120.0, 160.0)

        #Setup of Servo Hand
        self.servoHand = Servo(15, self.numberServoHandStates, 84.0, 0.0, 140.0)
