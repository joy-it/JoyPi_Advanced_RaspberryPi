import board
import busio
import digitalio
import time
from adafruit_mcp230xx.mcp23008 import MCP23008

class buttonmatrix:

    # values shown on the button matrix
    dictionary = {(0, 0) : "7",
                  (0, 1) : "4",
                  (0, 2) : "1",
                  (0, 3) : "0",
                  (1, 0) : "8",
                  (1, 1) : "5",
                  (1, 2) : "2",
                  (1, 3) : "#",
                  (2, 0) : "9",
                  (2, 1) : "6",
                  (2, 2) : "3",
                  (2, 3) : "=",
                  (3, 0) : "*",
                  (3, 1) : "/",
                  (3, 2) : "+",
                  (3, 3) : "-"}
    
    def __init__(self, i2c: busio.I2C, i2c_address = 0x22):
        """
        i2c - i2c port
        i2c_address - address of the barometer
        """
        self.i2c_address = i2c_address
        mcp = MCP23008(i2c, address = self.i2c_address)
        self.rows = [mcp.get_pin(4), mcp.get_pin(5), mcp.get_pin(6), mcp.get_pin(7)]
        self.columns = [mcp.get_pin(0), mcp.get_pin(1), mcp.get_pin(2), mcp.get_pin(3)]
        self.calculated = ""
        
        for i in range(len(self.rows)):
            self.rows[i].direction = digitalio.Direction.INPUT
            self.rows[i].pull = digitalio.Pull.UP
            
            self.columns[i].direction = digitalio.Direction.OUTPUT
            self.columns[i].value = False

    
    def _checkMatrix(self):
        """
        returns the column and row which was pressed
        """
        column_value, row_value = None, None
        for i in range(len(self.rows)):
            if self.rows[i].value == False :
                row_value = i

        # flip columns and rows to get the column
        for i in range(len(self.columns)):
            self.columns[i].direction = digitalio.Direction.INPUT
            self.columns[i].pull = digitalio.Pull.UP
            self.rows[i].direction = digitalio.Direction.OUTPUT
            self.rows[i].value = False
                
        for i in range(len(self.columns)):
            if self.columns[i].value == False :
                column_value = i
        
        # set columns and rows back
        for i in range(len(self.rows)):
            self.rows[i].direction = digitalio.Direction.INPUT
            self.rows[i].pull = digitalio.Pull.UP
            self.columns[i].direction = digitalio.Direction.OUTPUT
            self.columns[i].value = False

        time.sleep(.1)
        return column_value, row_value
            

    def getKey(self):
        """
        returns the name of the button which was pressed
        """
        try:
            return self.dictionary[self._checkMatrix()]
        except KeyError:
            return None

    def clearMemory(self):
        """
        clears class variable calculated
        """
        self.calculated = ""
        

    def calculate(self):
        """
        method to use button matrix as calculator
        """
        value = self.getKey()
        if value is None:
            return self.calculated
        if value == "=":
            try:
                self.calculated = str(eval(self.calculated))
                return self.calculated
            # catch if number should be divided by zero
            except ZeroDivisionError :
                self.clearMemory()
                raise ValueError("You can not divide by zero!")
            # catch if string is not convertable to a number
            except SyntaxError:
                self.clearMemory()
                raise ValueError("Term can not be calculated!")
        elif value == "#":
            self.clearMemory()
        else:
            self.calculated += value
            return self.calculated
