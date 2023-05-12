import math
import RPi.GPIO as GPIO
import time

class stepmotor:

    def __init__(self, pin1 = 22, pin2 = 23, pin3 = 24, pin4 = 4):
        self.pin_A = pin1
        self.pin_B = pin2
        self.pin_C = pin3
        self.pin_D = pin4
        self.interval = 0.0011

        GPIO.setmode(GPIO.BCM)
        
        # Configure pins as output
        GPIO.setup(self.pin_A,GPIO.OUT)
        GPIO.setup(self.pin_B,GPIO.OUT)
        GPIO.setup(self.pin_C,GPIO.OUT)
        GPIO.setup(self.pin_D,GPIO.OUT)
        
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)
        GPIO.output(self.pin_D, False)

    def step1(self):
        GPIO.output(self.pin_D, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)

    def step2(self):
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_C, False)

    def step3(self):
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_C, False)

    def step4(self):
        GPIO.output(self.pin_B, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)

    def step5(self):
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)

    def step6(self):
        GPIO.output(self.pin_A, True)
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)

    def step7(self):
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)

    def step8(self):
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_A, False)

    def turn(self,count):
        for i in range (int(count)):
            self.step1()
            self.step2()
            self.step3()
            self.step4()
            self.step5()
            self.step6()
            self.step7()
            self.step8()

    def end(self):
        GPIO.cleanup()
        
        
    def turnSteps(self, steps):
        """ 
        Rotate by n steps
        """
        self.turn(int(steps))

    def turnDegrees(self, deg):
        """ 
        Rotate n degrees
        """
        self.turn(round(deg*512/360,0))

    def turnDistance(self, dist, rad):
        """
        Rotation by distance value
        """
        self.turn(round(512*dist/(2*math.pi*rad),0))