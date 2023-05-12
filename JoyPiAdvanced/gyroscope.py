from spidev import SpiDev
import time
    
class gyroscope:

    scaleFactor = 0
    scale_gyroscope = 700
    scale_range = 46.5
    offset = 0
    
    def __init__(self, bus = 0, device = 2):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz
        tmp = self.read_register(27) & 0x26
        self.write_register(27, 0x18 | tmp)
 
 
    def open(self):
        """
        Opens up SPI communication
        """
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz


    def close(self):
        """
        Closes SPI communication
        """
        self.spi.close()

        
    def read_register(self, reg):
        """
        read value from register
        """
        tmp = self.spi.xfer3([(reg | 0x80), 0])
        return tmp[1]

        
    def write_register(self, reg, data):
        """
        write value to register
        """
        self.spi.writebytes([ (reg & 0x7F), data])
       
        
    def getTemperature(self):
        """
        returns read temnperature
        """
        temp = (self.read_register(0x41) << 8) + self.read_register(0x42)
        return (temp / 100)

    
    def getXValue(self):
        """
        returns x value
        """
        x = (self.read_register(0x43) << 8) + self.read_register(0x44)
        if (x / self.scale_gyroscope > self.scale_range):
            return x / self.scale_gyroscope - (2 * self.scale_range)
        else:
            return x / self.scale_gyroscope

    
    def getYValue(self):
        """
        returns y value
        """
        y = (self.read_register(0x45) << 8) + self.read_register(0x46)
        if (y / self.scale_gyroscope > self.scale_range):
            return y / self.scale_gyroscope - (2 * self.scale_range)
        else:
            return y / self.scale_gyroscope

    
    def getTilt(self):
        """
        returns tilt directions
        """
        y = self.getYValue()
        x = self.getXValue()
        if (y > 5):
            return 'right'
        elif (y < -5):
            return 'left'
        elif (x > 3):
            return 'forward'
        elif (x < -3):
            return 'backward'
        else:
            return 'No movement'

        
    def who_am_i(self):
        """
        returns device ID
        """
        return (self.read_register(0x75))
                
                
    def scale_Factor(self, scale):
        """
        set scale factor of gyroscope
        """
        self.scaleFactor = scale
        self.write_register(0x19, 0)
        self.write_register(0x1B, scale +1)
        if (scale == 0):
            self.scale_gyroscope = 700
            self.scale_range = 46.5
        
        elif (scale == 8): 
            self.scale_gyroscope = 350
            self.scale_range = 93
        
        elif (scale == 16): 
            self.scale_gyroscope = 175
            self.scale_range = 187
        
        elif (scale == 24): 
            self.scale_gyroscope = 87.5
            self.scale_range = 374        