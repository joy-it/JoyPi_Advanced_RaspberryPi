# import necessary libraries
from JoyPi_Advanced_RaspberryPi import barometer
import busio
import board

# initilize barometer
i2c = busio.I2C(board.SCL, board.SDA)
baro = barometer(i2c)

# prepare table for printing values
print("| temperature |   pressure    |  altitude  |")
print(45 * "-")
# change the reference_pressure to your local pressure to calculate your altitude
print("|   ", baro.get_temperature(), "   |   ", baro.get_pressure(), "   |   ", baro.get_altitude(reference_pressure = 1013.25), "  |")