import time
from rpi_ws281x import PixelStrip, Color

class LEDMatrix:

    def __init__(self, pin = 18, brightness = 100):
        # LED strip configuration
        self.LED_COUNT = 64              # Number of pixels
        self.LED_PIN = pin               # GPIO pin to which the module is connected
        self.LED_FREQ_HZ = 800000        # LED signal frequency
        self.LED_DMA = 10                # DMA channel used to generate the signal
        self.LED_BRIGHTNESS = brightness # Brightness setting
        self.LED_INVERT = False          # Signal inversion
        self.LED_CHANNEL = 0             # Set to 1 if GPIOs 13, 19, 41, 45 or 53 are used

        self.RIGHT_BORDER = [7,15,23,31,39,47,55,63]
        self.LEFT_BORDER = [0,8,16,24,32,40,48,56]
        
        # Create NeoPixel object
        self.strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        
        # Initialize library
        self.strip.begin()


    def clean(self):
        """ 
        Switch off all LEDs
        """
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()


    def setPixel(self, position, colour):
        """
        set Pixel on position to given colour
        """
        try:
            r, g, b = colour
        except ValueError:
            print("Colour is not a tuple!")
            
        self.strip.setPixelColor(position, Color(r, g, b))


    def RGB_on(self,colour):
        """
        set all pixels to given colour
        """
        try:
            r, g, b = colour
        except ValueError:
            print("Colour is not a tuple!")
        
        for i in range(64):
            self.strip.setPixelColor(i,Color(r, g, b))
        self.strip.show()


    def wheel(self,pos):
        """
        generate rainbow colours over positions 0-255
        """
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)


    def rainbow(self, wait_ms=20, iterations=1):
        """
        Rainbow effect on all LEDs
        """
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
        self.clean()


    def colourWipe(self, colour, wait_ms=50):
        """
        Move colours pixel by pixel over the LEDs with a given colour
        """
        try:
            r, g, b = colour
        except ValueError:
            print("Colour is not a tuple!")
        
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(r, g, b))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)


    def theaterChase(self, colour, wait_ms=50, iterations=10):
        """
        Chaser animation with a given colour
        """
        try:
            r, g, b = colour
        except ValueError:
            print("Colour is not a tuple!")
        
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, Color(r, g, b))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)


    def demo1(self):
        """
        Simple demo programm
        """
        self.theaterChase((127, 127, 127))  # White chaser
        self.theaterChase((127, 0, 0))  # Red chaser
        self.theaterChase((0, 0, 127))  # Blue chaser

        self.rainbow()

        self.clean()


    def show(self):
        """
        displays set pixels
        """
        self.strip.show()


    def demo2(self):
        """
        More complex demo programm in a continuous loop
        """
        heart = [1,6,8,9,10,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,50,51,52,53,59,60]
        try:
            for i in range(3):
                self.demo1()
            while True:
                for j in range(256):
                    for i in heart:
                        self.strip.setPixelColor(i,Color(j,0,0))
                    self.strip.show()
                for j in range(256, 0, -1):
                    for i in heart:
                        self.strip.setPixelColor(i,Color(j,0,0))
                    self.strip.show()
        except KeyboardInterrupt:
             self.clean()