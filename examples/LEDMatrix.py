"""
ATTENTION!

The Joy-Pi Advanced 2 is no longer compatible with this code for the LED 
Matrix. To ensure compatibility with the Raspberry Pi 5, the LED matrix is now 
controlled via I²C because of the RP2040 microcontroller chip. The LED matrix can 
now be controlled with the Joy-Pi Advanced via this repository 
http://github.com/joy-it/JoyPi_RGB_Matrix_RaspberryPi.
"""

# Required modules are inserted and configured
from JoyPi_Advanced_RaspberryPi import LEDMatrix
import time

# Create object matrix
matrix = LEDMatrix()

# colourWipe animation with different colors
print("colourWipe animation")
matrix.colourWipe((255, 0, 0)) # red
matrix.colourWipe((0, 255, 0)) # green
matrix.colourWipe((0, 0, 255)) # blue

# theaterChase animation with different colors
print("theaterChase animation")
matrix.theaterChase((127, 127, 127)) # white
matrix.theaterChase((127, 0, 0)) # red
matrix.theaterChase((0, 0, 127)) # blue

# rainbow animation
print("rainbow animation")
matrix.rainbow()

# set RGB matrix to yellow
matrix.RGB_on((255, 255, 0))
time.sleep(2)
# set RGB matrix to turquoise
matrix.RGB_on((0, 255, 255))
time.sleep(2)
# set RGB matrix to purple
matrix.RGB_on((255, 0, 255))
time.sleep(2)

# clean Matrix up
matrix.clean()

# Displays a heart onto the LED matrix
print("Display a heart")
heart = [1,6,8,9,10,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,50,51,52,53,59,60]
for i in heart:
    matrix.setPixel(i,(255,0,0))
matrix.show()
time.sleep(5)

# Clear matrix
print("Clear LEDs")
matrix.clean()
