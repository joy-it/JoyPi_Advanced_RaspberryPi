import RPi.GPIO as GPIO
import time

class servomotor:
    
    def __init__(self, pin = 18, position = 0):
        self.pin = pin
        self.position = position
        self.start_pos = position
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
        self.motor = GPIO.PWM(self.pin, 50)
        self.motor.start(0)
        
    def setDirection(self, set_pos, speed = 5):
        """
        moves servomotor to a specified position set_pos (-100 to 100 / right to left)
        with speed (1 to 5 / slow to fast)
        """
        # defining sign function
        sign = lambda x: -1 if x < 0 else 1
        
        # catch values out of the intervall
        if set_pos < -100 : set_pos = -100
        elif set_pos > 100 : set_pos = 100
        if speed < 1 : speed = 1
        elif speed > 5 : speed = 5
        
        # turn from current position to set_pos with a certain speed      
        for turn in range(self.position, int(set_pos) + sign(set_pos), int(speed * 10 * sign(set_pos - self.position))):
            self.motor.ChangeDutyCycle(0.05 * turn + 7)
            self.position = turn
            time.sleep(0.1)

    def setHome(self):
        """
        set servo back to start position
        """
        self.setDirection(self.start_pos)
        
    def getPosition(self):
        """
        returns the position of the servomotor
        """
        return self.position
    
    def end(self):
        """
        moves servo to start position, stops PWM communication and cleans up
        """
        self.setHome()
        self.motor.stop()
        GPIO.cleanup()