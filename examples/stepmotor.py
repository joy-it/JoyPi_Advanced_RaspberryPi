# -*- coding:utf-8 -*-
import time
from JoyPi_Advanced_RaspberryPi import stepmotor

# create object of the stepper motor 
print("movement started")
motor = stepmotor()

# move a single step with the help of the turnSteps method
print("single step")
motor.turnSteps(1)

# pause
time.sleep(0.5)

# Drive 20 steps
print("20 steps")
motor.turnSteps(20)

time.sleep(0.5)

# move a quarter turn with the help of the turnDegree method
print("quarter turn")
motor.turnDegrees(90)

time.sleep(0.5)

# Drive one full turn
print("full rotation")
motor.turnDegrees(360)

# Drive one full turn in the other direction
print("full rotation in the other direction")
motor.turnDegrees(-360)

print("Movement stopped")

# free all used pins
motor.close()