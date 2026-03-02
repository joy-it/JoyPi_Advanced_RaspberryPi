# -*- coding:utf-8 -*-
# Required modules are inserted and configured
import time
from JoyPi_Advanced_RaspberryPi import colour

# Create object sensor to control colour sensor
sensor = colour()

# set integration time
sensor.setIntegrationTime(2)
# set senor to auti�Mode
sensor.autoMode()
# initialize variable to save last printed colour
last_colour = ""

# main program loop
try:
    while True:
        # get dominant colour and raw values
        colour, raw_values = sensor.readAll()
        # check if a new colour is detected
        if last_colour != colour:
            # print colour and raw values
            print("Detected colour:", colour, "\t\t red:",raw_values[0], "\tgreen:",raw_values[1], "\tblue:",raw_values[2], "\twhite:", raw_values[3])
            # save printed colour as last printed colour
            last_colour = colour
except:
    # deactivate colour sensor
    sensor.disableSensor()