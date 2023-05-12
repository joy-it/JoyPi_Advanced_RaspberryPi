import busio
from adafruit_bus_device import i2c_device
import time

class barometer:
    
    RESET = 0x1E
    READ = 0x00
    CONV = 0x40
    D1 = 0x00
    D2 = 0x10
    PROM_RD = 0xA0
    ADC_RESOLUTION = {256: 0x00,
                      512: 0x02,
                      1024: 0x04,
                      2048: 0x06,
                      4096: 0x08}
    ADC_DELAY = {0x00: 0.001,
                  0x02: 0.003,
                  0x04: 0.004,
                  0x06: 0.006,
                  0x08: 0.01}
   
    def __init__(self, i2c: busio.I2C, i2c_address = 0x77, resolution=4096):
        """
        i2c - i2c port
        i2c_address - address of the barometer
        resolution - resolution of the ADC, possible values: 256, 512, 1024, 2048, 4096
        """
        self.i2c_address = i2c_address
        self.device = i2c_device.I2CDevice(i2c, self.i2c_address)
        self.resolution = self.ADC_RESOLUTION[resolution]
        self.reset()
        self._coefficients = self.read_coefficients()
    

    def reset(self):
        """
        resets barometer
        """
        with self.device as bus_device:
            bus_device.write(bytes([self.RESET]))
        
    def read_coefficient(self, index):
        """
        read value for a specific coefficient
        """
        with self.device as bus_device:
            time.sleep(0.01)
            bus_device.write(bytes([self.PROM_RD + index * 2]))
            result = bytearray(2)
            bus_device.readinto(result)
        result1, result2 = result[0], result[1]
        return (256 * result1) + result2

    def read_coefficients(self):
        """
        set values too all coefficients
        """
        coef = [0] * 6
        for i in range(6):
            coef[i] = self.read_coefficient(i+1)
            if coef[i] == 0 : coef[i] = self.read_coefficient(i+1)
        return coef

    def conversion(self, data):
        """
        read digital data
        """
        with self.device as bus_device:
            time.sleep(0.01)
            bus_device.write(bytes([0x40 | data | self.resolution]))
            time.sleep(self.ADC_DELAY[self.resolution])
            bus_device.write(bytes([self.READ]))
            result = bytearray(3)
            bus_device.readinto(result)
        return 65536 * result[0] + 256 * result[1] + result [2]
        
    def get_pressure(self):
        """
        calculates the measured pressure
        """
        d1 = self.conversion(self.D1)
        d2 = self.conversion(self.D2)
        dT = d2 - self._coefficients[4] * 256
        off = self._coefficients[1] * 131072 + (self._coefficients[3] * dT)/ 64
        sens = self._coefficients[0] * 65536 + (self._coefficients[2] * dT) / 128
        return round(((d1 * sens / 2097152 - off) / 32768) / 100, 2)

    def get_temperature(self):
        """
        calculates the measured temperature
        """
        d2 = self.conversion(self.D2)
        dT = d2 - self._coefficients[4] * 256
        return round((2000 + dT * self._coefficients[5] / 8388608) / 100, 2)

    def get_altitude(self, reference_pressure = 1013.25):
        """
        calculates altitude from the measured pressure
        reference_pressure - mean sea level pressure,  should be adjusted to local QNH
        """
        pressure = self.get_pressure()
        return round(44330 * (1 - (pressure / reference_pressure) ** (1/5.255)), 2)