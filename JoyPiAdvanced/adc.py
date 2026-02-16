from spidev import SpiDev
import RPi.GPIO as GPIO
    
class adc:
    SYSTEM_STATUS = 0x00
    READ_CMD = 0x10
    WRITE_CMD = 0x08
    CHANNEL_SEL = 0x11
    PIN_CFG = 0x05
    SEQUENCE_CFG = 0x10
    
    def __init__(self, bus = 0, device = 0, cs = 8):
        """
        initialize ADC
        bus - select bus
        device - select device
        """
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz
        self.spi.mode = 0
        self.cs = cs
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.cs, GPIO.OUT, initial=GPIO.HIGH)
 
    def open(self):
        """
        start SPI communication
        """
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz
    
    def read_value(self, channel):      
        """
        returns raw value from a specific channel
        channel - which channel should be read from
        """ 
        data = self.read_register(self.SEQUENCE_CFG)
        self.write_register(self.SEQUENCE_CFG, data[0] & 0xFC)
        self.write_register(self.PIN_CFG, 0x00)
        self.write_register(self.SEQUENCE_CFG, 0x00)
        self.write_register(self.CHANNEL_SEL, channel)
        GPIO.output(self.cs, GPIO.LOW)
        self.spi.readbytes(2)
        GPIO.output(self.cs, GPIO.HIGH)
        GPIO.output(self.cs, GPIO.LOW)
        data = self.spi.readbytes(2)
        GPIO.output(self.cs, GPIO.HIGH)
        return ((data[0]<<8) | data[1]) >>4
 
    def read_voltage(self, channel, value = None): 
        """
        returns measured voltage from a specific channel
        channel - which should be read from
        value - if channel is already read, raw value can be then used to calculate voltage
        """
        if value is None:  
            return round((self.read_value(channel) / 4096) * 5.0, 2)
        return round((value / 4096) * 5.0, 2)

    def close(self):
        """
        end SPI communication
        """
        self.spi.close()
        GPIO.cleanup()
        
    def read_register(self, reg):
        """
        returns value from a specific register
        reg - register which should be read from
        """
        GPIO.output(self.cs, GPIO.LOW)
        self.spi.writebytes([self.READ_CMD, reg, 0x00])
        GPIO.output(self.cs, GPIO.HIGH)
        return self.spi.readbytes(1)
        
    def write_register(self, reg, data):
        """
        write value into a specific register
        reg - register in which should be written
        data - value which should be written into the register
        """
        GPIO.output(self.cs, GPIO.LOW)
        self.spi.writebytes([self.WRITE_CMD, reg, data])
        GPIO.output(self.cs, GPIO.HIGH)
        
    def read_status(self):
        """
        return status of the ADC
        """
        return self.read_register(self.SYSTEM_STATUS)
        
    
        
                 
                                                                                                                              