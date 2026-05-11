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

import busio
from adafruit_bus_device import i2c_device
import time
import threading
import numpy as np

class colour:

    REG_CONF = 0x00
    REG_RED = 0x08
    REG_GREEN = 0x09
    REG_BLUE = 0x0A
    REG_WHITE = 0x0B

    INTEGRATION_TIME_40MS = 0
    INTEGRATION_TIME_80MS = 1
    INTEGRATION_TIME_160MS = 2
    INTEGRATION_TIME_320MS = 3
    INTEGRATION_TIME_640MS = 4
    INTEGRATION_TIME_1280MS = 5

    _INTEGRATION_TIME_VALUES = {
        INTEGRATION_TIME_40MS: 0x00,
        INTEGRATION_TIME_80MS: 0x10,
        INTEGRATION_TIME_160MS: 0x20,
        INTEGRATION_TIME_320MS: 0x30,
        INTEGRATION_TIME_640MS: 0x40,
        INTEGRATION_TIME_1280MS: 0x50,
    }

    _INTEGRATION_TIME_DELAY = {
        INTEGRATION_TIME_40MS: 0.05,
        INTEGRATION_TIME_80MS: 0.09,
        INTEGRATION_TIME_160MS: 0.17,
        INTEGRATION_TIME_320MS: 0.33,
        INTEGRATION_TIME_640MS: 0.65,
        INTEGRATION_TIME_1280MS: 1.29,
    }

    BIT_SD = 0x01
    BIT_AF = 0x02
    BIT_TRIG = 0x04
    MASK_INTEGRATION_TIME = 0x70

    def __init__(self,  i2c: busio.I2C, integration_time=INTEGRATION_TIME_160MS, i2c_address = 0x10):
        """
        initialize colour sensor
        i2c_address - i2c_address of colour sensor (default 0x10)
        """
        self.address = i2c_address
        if integration_time not in self._INTEGRATION_TIME_VALUES:
            raise ValueError("integration_time is not in range")
        self.integration_time = integration_time
        self.device = i2c_device.I2CDevice(i2c, self.address)
        self.enableSensor()
    
    def write(self, cmd, val):
        """
        write value into register on the colour sensor
        cmd - register
        val - value to be written
        """
        data = bytes([
            cmd & 0xFF,
            val & 0xFF,
            (val >> 8) & 0xFF,
        ])
        with self.device as bus_device:
            bus_device.write(data)
    
    def read(self, cmd):
        """
        read value from register on the colour sensor
        cmd - register
        """
        register = bytes([cmd & 0xFF])
        data = bytearray(2)
        last_error = None
        for _ in range(3):
            try:
                with self.device as bus_device:
                    bus_device.write_then_readinto(register, data)
                return data[0] | (data[1] << 8)
            except OSError as error:
                last_error = error
                time.sleep(0.02)
        raise last_error

    def enableSensor(self):
        """
        activate Sensor
        """
        config = self._INTEGRATION_TIME_VALUES[self.integration_time]
        config &= ~self.BIT_SD
        config &= ~self.BIT_AF
        config &= ~self.BIT_TRIG
        self.write(self.REG_CONF, config)
        time.sleep(self._INTEGRATION_TIME_DELAY[self.integration_time])
        
    def disableSensor(self):
        """
        deactivate Sensor
        """
        config = self.read(self.REG_CONF)
        config |= self.BIT_SD
        self.write(self.REG_CONF, config)
        
    def setIntegrationTime(self, integration_time):
        """
        set integration time with variable integration_time
        integration_time - _INTEGRATION_TIME_VALUES 
            INTEGRATION_TIME_40MS = 40 ms
            INTEGRATION_TIME_80MS = 80 ms
            INTEGRATION_TIME_160MS = 160 ms
            INTEGRATION_TIME_320MS = 320 ms
            INTEGRATION_TIME_640MS = 640 ms
            INTEGRATION_TIME_1280MS = 1280 ms
        """
        if integration_time not in self._INTEGRATION_TIME_VALUES:
            raise ValueError("integration_time is not in range")
        config = self.read(self.REG_CONF)
        config &= ~self.MASK_INTEGRATION_TIME
        config |= self._INTEGRATION_TIME_VALUES[integration_time]
        config &= ~self.BIT_SD
        self.integration_time = integration_time
        self.write(self.REG_CONF, config)
        time.sleep(self._INTEGRATION_TIME_DELAY[self.integration_time])
        
    def getRed(self):
        """
        returns measured value for colour red
        """
        return self.read(self.REG_RED)

    def getBlue(self):
        """
        returns measured value for colour blue
        """
        return self.read(self.REG_BLUE)

    def getGreen(self):
        """
        returns measured value for colour green
        """
        return self.read(self.REG_GREEN)
    
    def getWhite(self):
        """
        returns measured value for colour white
        """
        return self.read(self.REG_WHITE)
    
    def getRGBW(self):
        """
        returns colour values from colour sensor - red, green, blue, white
        """
        red = self.getRed()
        time.sleep(0.005)
        green = self.getGreen()
        time.sleep(0.005)
        blue = self.getBlue()
        time.sleep(0.005)
        white = self.getWhite()
        return red, green, blue, white

    def forceMode(self):
        """
        forces measurement mode - triggers to start
        """
        config = self.read(self.REG_CONF)
        config &= self.MASK_INTEGRATION_TIME
        config |= self.BIT_AF
        config |= self.BIT_TRIG
        config &= ~self.BIT_SD
        self.write(self.REG_CONF, config)
        time.sleep(self._INTEGRATION_TIME_DELAY[self.integration_time])
        
    def autoMode(self):
        """
        automatic measurement mode
        """
        config = self.read(self.REG_CONF)
        config &= self.MASK_INTEGRATION_TIME
        config &= ~self.BIT_AF
        config &= ~self.BIT_TRIG
        config &= ~self.BIT_SD
        self.write(self.REG_CONF, config)
        time.sleep(self._INTEGRATION_TIME_DELAY[self.integration_time])
    
    def readAll(self):
        """
        returns most recognized colour and raw values
        """
        red, green, blue, white = self.getRGBW()
        values = {
            "red": red,
            "green": green,
            "blue": blue,
        }

        dominant_color = max(values, key=values.get)
        return dominant_color, [red, green, blue, white]