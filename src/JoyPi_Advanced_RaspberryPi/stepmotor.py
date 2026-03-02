import math
from gpiozero import DigitalOutputDevice
import time

class stepmotor:

    def __init__(self, pin1 = 22, pin2 = 23, pin3 = 24, pin4 = 4):
        self.pin_A = DigitalOutputDevice(pin1, initial_value = False)
        self.pin_B = DigitalOutputDevice(pin2, initial_value = False)
        self.pin_C = DigitalOutputDevice(pin3, initial_value = False)
        self.pin_D = DigitalOutputDevice(pin4, initial_value = False)
        self.interval = 0.0011

    def step1(self):
        self.pin_D.on()
        time.sleep(self.interval)
        self.pin_D.off()

    def step2(self):
        self.pin_D.on()
        self.pin_C.on()
        time.sleep(self.interval)
        self.pin_D.off()
        self.pin_C.off()

    def step3(self):
        self.pin_C.on()
        time.sleep(self.interval)
        self.pin_C.off()

    def step4(self):
        self.pin_B.on()
        self.pin_C.on()
        time.sleep(self.interval)
        self.pin_B.off()
        self.pin_C.off()

    def step5(self):
        self.pin_B.on()
        time.sleep(self.interval)
        self.pin_B.off()

    def step6(self):
        self.pin_A.on()
        self.pin_B.on()
        time.sleep(self.interval)
        self.pin_A.off()
        self.pin_B.off()

    def step7(self):
        self.pin_A.on()
        time.sleep(self.interval)
        self.pin_A.off()

    def step8(self):
        self.pin_D.on()
        self.pin_A.on()
        time.sleep(self.interval)
        self.pin_D.off()
        self.pin_A.off()

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

    def turnReverse(self, count):
        for i in range(int(count)):
            self.step8()
            self.step7()
            self.step6()
            self.step5()
            self.step4()
            self.step3()
            self.step2()
            self.step1()

    def close(self):
        self.pin_A.close()
        self.pin_B.close()
        self.pin_C.close()
        self.pin_D.close()

    def turnSteps(self, steps):
        """ 
        Rotate by n steps
        """
        if steps < 0:
            self.turnReverse(abs(int(steps)))
        else:
            self.turn(int(steps))

    def turnDegrees(self, deg):
        """ 
        Rotate n degrees
        """
        if deg < 0:
            self.turnReverse(abs(round(deg*512/360,0)))
        else:
            self.turn(round(deg*512/360,0))


    def turnDistance(self, dist, rad):
        """
        Rotation by distance value
        """
        if dist < 0:
            self.turnReverse(abs(round(512*dist/(2*math.pi*rad),0)))
        else:
            self.turn(round(512*dist/(2*math.pi*rad),0))
