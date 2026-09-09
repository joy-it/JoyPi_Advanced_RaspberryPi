# -*- coding:utf-8 -*-
# Required modules are inserted and configured
import time
from JoyPi_Advanced_RaspberryPi import colour
import busio
import board

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
# Create object sensor to control colour sensor
colour_sensor = colour(i2c, colour.INTEGRATION_TIME_160MS)

# set integration time
colour_sensor.setIntegrationTime(colour.INTEGRATION_TIME_160MS)
# set senor to auti�Mode
colour_sensor.autoMode()
# initialize variable to save last printed colour
last_colour = ""

# main program loop
try:
    while True:
        # get dominant colour and raw values
        colour, raw_values = colour_sensor.readAll()
        # check if a new colour is detected
        if last_colour != colour:
            # print colour and raw values
            print("Detected colour:", colour, "\t\t red:",raw_values[0], "\tgreen:",raw_values[1], "\tblue:",raw_values[2], "\twhite:", raw_values[3])
            # save printed colour as last printed colour
            last_colour = colour
except:
    # deactivate colour sensor
    colour_sensor.disableSensor()