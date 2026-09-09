from JoyPi_Advanced_RaspberryPi import servomotor
import time

# initialize servomotor
motor = servomotor()

# main program loop
try:
    while True:
        print ("Turn left ...")
        # move to the left with 2/5 speed
        motor.setDirection(90, 2)
        time.sleep(0.5)
        
        print ("Turn right ...")
        # move to the right with 2/5 speed
        motor.setDirection(-90, 2)
        time.sleep(0.5)

# Clean up after the program is finished  
except KeyboardInterrupt:
    motor.end()