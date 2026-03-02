# Required modules are inserted and configured
from JoyPi_Advanced_RaspberryPi import gyroscope
import time

# create object gyroscope
gyro = gyroscope()

# Main program loop
try:
    while True:
        # print read tilt and temperature
        print("Tilt:\t", gyro.getTilt())
        print("Temperature:\t", gyro.getTemperature())
        
        # short break
        time.sleep(1)

# Clean up after program is finished
except KeyboardInterrupt:
    gyro.close()