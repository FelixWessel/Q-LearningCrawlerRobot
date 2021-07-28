from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)


class Servo:
    def __init__(self, connection, numberOfStates, initialAngle, minAngle, maxAngle):
        # hier muss noch der Anschluss aus der SuperKlasse rein
        self.numberOfStates = numberOfStates
        self.initialAngle = initialAngle
        self.currentAngle = self.initialAngle
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.stepAngle = int((self.maxAngle-self.minAngle)/(self.numberOfStates-1))
        self.initialServoState=int(((self.initialAngle-self.minAngle)/self.stepAngle)) #This is an integer between zero and numOfStates-1 used to index the state number of servo
