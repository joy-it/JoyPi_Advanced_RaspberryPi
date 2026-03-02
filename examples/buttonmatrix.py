# Required modules are inserted and configured
import busio
import board
import time
from JoyPi_Advanced_RaspberryPi import buttonmatrix

# create object matrix to control the button matrix
i2c = busio.I2C(board.SCL, board.SDA)
matrix = buttonmatrix(i2c)

# variable to save last printed result
last_result = ""

# main program loop
while True:
    try:
        # check button matrix and save it in result
        result = matrix.calculate()
        # print result if it is not the same as before and not empty
        if result != last_result and result != "":
            print(result)
            # save printed result as last result
            last_result = result
    
    # catch not possible calculations and print the error message
    except ValueError as e:
        print(e)