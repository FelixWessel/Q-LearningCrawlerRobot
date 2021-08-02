#Import Libraries
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

class Sensor:
    def __init__(self):

        #Define GPIO (Mode, Pins, Output)
        GPIO.setmode(GPIO.BCM)
        GPIO_TRIGGER = 23
        GPIO_ECHO = 24
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
 
    def read(self):
        # Set Trig High
        GPIO.output(GPIO_TRIGGER, True)
 
        # Set Trig Low (after 0.01ms)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
 
        startTime = time.time()
        endTime = time.time()
 
        # Calculate Start and End Time
        while GPIO.input(GPIO_ECHO) == 0:
            startTime = time.time()
 
        while GPIO.input(GPIO_ECHO) == 1:
            endTime = time.time()
 
        # Calculate Time Difference
        differenceTime = endTime - startTime
	
        # Speed of Sound (34300 cm/s) 
        distance = (differenceTime * 34300) / 2
 
        return distance
#  
# if __name__ == '__main__':
#     try:
#         while True:
#             distanz = entfernung()
#             print ("Distanz = %.1f cm" % distanz)
#             time.sleep(1)
#  
#         # Programm beenden
#     except KeyboardInterrupt:
#         print("Programm abgebrochen")
#         GPIO.cleanup()
