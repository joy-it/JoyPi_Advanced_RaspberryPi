#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  
###################################################################################
# Edited by Joy-IT
# 
###################################################################################
#  Copyright 2020  <pi@kb>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Written by BitHead (Britany Head)
#  https://forums.raspberrypi.com/viewtopic.php?t=263498
# Step 1) Enable I2C in Raspi-Config (Interfacing Options)
# Step 2) sudo apt-get install i2c-tools python3-smbus
# Step 3) plug it in (don't forget your pull-up resistors) and run this program

import smbus
import time
import threading
import numpy as np

class colour:

    def __init__(self, i2c_address = 0x10):
        """
        initialize colour sensor
        i2c_address - i2c_address of colour sensor (default 0x10)
        """
        self.address = i2c_address
        self.bus = smbus.SMBus(1)
        self.enableSensor()
    
    def write(self, cmd, val):
        """
        write value into register on the colour sensor
        cmd - register
        val - value to be written
        """
        self.bus.write_word_data(self.address, cmd, val)
    
    def read(self, cmd):
        """
        read value from register on the colour sensor
        cmd - register
        """
        return self.bus.read_word_data(self.address, cmd)
        
    def enableSensor(self):
        """
        activate Sensor
        """
        conf = self.read(0x00) & 0x00FE
        self.write(0x00, conf)
        
    def disableSensor(self):
        """
        deactivate Sensor
        """
        conf = (self.read(0x00) & 0x00FE) | 0x000
        self.write(0x00, conf)
        time.sleep(.001)
    
    def getRGBW(self):
        """
        returns colour values from colour sensor - red, green, blue, white
        """
        return self.read(0x08), self.read(0x09), int(self.read(0x0A) * 1.5), self.read(0x0B)
        
    def setIntegrationTime(self, int_time):
        """
        set integration time with variable int_time
        int_time - integration time 
            0 = 40 ms
            1 = 80 ms
            2 = 160 ms
            3 = 320 ms
            4 = 640 ms
            5 = 1280 ms
        """
        if int_time < 0 or int_time > 5:
            raise ValueError('int_time is not in range')
        conf = self.read(0x00) & 0x0003
        self.write(0x00, (conf | (int_time << 4)))
        
    def forceMode(self):
        """
        forces measurement mode - triggers to start
        """
        conf = (self.read(0x00) & 0x0072) | 0x0002
        self.write(0x00, conf)
        
    def autoMode(self):
        """
        automatic measurement mode
        """
        conf = self.read(0x00) & 0x0070
        self.write(0x00, conf)
    
    def readAll(self):
        """
        returns most recognized colour and raw values
        """
        r, g, b, w = self.getRGBW()
        raw_val = [r, g, b, w]
        dominant_col, dominant_val = "red", r
        if g > dominant_val: dominant_col, dominant_val = "green", g
        if b > dominant_val: dominant_col, dominant_val = "blue", b
        
        return dominant_col, raw_val