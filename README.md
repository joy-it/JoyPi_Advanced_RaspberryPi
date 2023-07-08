# JoyPi_Advanced_RaspberryPi
Library for several modules for the Raspberry Pi

## About the Joy Pi Advanced
More information coming soon

## Note
This repository was created for the use with the Joy Pi Advanced on the Raspberry Pi.

This library includes ADC, gyroscope, barometer, button matrix, colour sensor, LED matrix, servo motor and step motor which are mounted on the Joy Pi Advanced.

## Dependencies
This library has some dependencies which are used to control the modules of the Joy Pi Advanced.

[`rpi_ws281x`](https://github.com/jgarff/rpi_ws281x) - for the LED matrix
[`Adafruit CircuitPython BusDevice`](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice) - for the barometer
[`Adafruit_CircuitPython_MCP230xx`](https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx) - for the button matrix

## Installation
```
git clone https://github.com/joy-it/JoyPi_Advanced_RaspberryPi.git
cd JoyPi_Advanced_RaspberryPi
sudo python3 setup.py install
```
## Library Guide
### ADC
- `adc(bus = 0, device = 0)` - initialize ADC with default values
- `open()` - starts communication
- `read_value(channel)` - returns raw value from a selected channel
- `read_voltage(channel, value=None)` - returns measured voltage from a selected channel, raw value can also be calculated into voltage with this method
- `close()` - ends communication
### Gyroscope
- `gyroscope(bus = 0, device = 2)`- initialize gyroscope with default values
- `open()` - starts communication
- `close()` - ends communication
- `getTemperature()` - returns measured temperature
- `getTilt()` - returns the tilted direction
- `scale_Factor(scale)` - sets scale factor of the gyroscope (0, 8, 16 or 24)
### Barometer
- `barometer(i2c: busio.I2C, i2c_address = 0x77, resolution=4096)` - initialize barometer with default values
- `get_pressure()` - returns the measured pressure
- `get_temperature()`- returns the measured temperature
- `get_altitude(reference_pressure = 1013.25)` - return the calculated altitude with the measured pressure and your local pressure (`reference_pressure`)
### Button matrix
- `buttonmatrix(i2c: busio.I2C, i2c_address = 0x22)`- initialize button matrix with default values
- `getKey()` - returns the pressed button
- `clearMemory()` - clears class variable `calculated`
- `calculate()` - method to use the button matrix as a calculator
### Colour sensor
- `colour(i2c_address = 0x10)`- initialize colour sensor with default values
- `enableSensor()` - start communication
- `disableSensor()`- end communication
- `getRGBW()` - returns measured RGBW values
- `setIntegrationTime()` - set integration time (`0`-40ms, `1`-80ms, `2`-160ms, `3`-320ms, `4`-640ms or `5`-1280ms)
- `forceMode()` - forces measurement mode
- `autoMode()`- automatic measurement mode
- `readAll()` - returns RGB colours as well as raw values
### LED matrix
- `LEDMatrix( pin = 18, brightness = 100)`- initialize LED matrix with default values
- `clean()` - clears the LED matrix
- `setPixel(position, colour)` - sets specific pixel to a selected colour
- `RGB_on(colour)` - sets the complete matrix to one selected colour
- `rainbow(wait_ms=20, iterations=1)` - rainbow effect on the whole matrix with default values
- `colourWipe(colour, wait_ms=50)` - Move selected colour pixel by pixel onto the matrix with default speed
- `theaterChase( colour, wait_ms=50, iterations=10)` - chaser animation with a selected colour with deafult speed
- `show()` - displays set pixels
- `demo1()` - demo program version 1
- `demo2()` - demo program version 2 
### Servo motor
- `servomotor(pin = 18, position = 0)` - initialize servo motor with default values
- `setDirection(set_pos, speed = 5)` - moves servomotor to a selected position (`set_pos`) with default speed
- `setHome()` - sets servomotor to start position
- `getPosition()` - returns position of servo motor
- `end()` - moves servo into start position, stops communication and cleans up communication
### Step motor
- `stepmotor(pin1 = 22, pin2 = 23, pin3 = 24, pin4 = 4)`- initialize step motor with default values
- `turnSteps(steps)` - turns a selected amount of steps
- `turnDegrees(deg)` - turns a selected amount of degree
- `turnDistance(dist, rad)` - rotates by distance value
- `end()` - clears up communication
