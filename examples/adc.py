from JoyPi_Advanced_RaspberryPi import adc
import time

# initialize ADC
adc = adc()


# create a header for a table
for i in range(8):
    print("| RawVal CH", i," |    V   ",end = '')
print("|")
print('-' * 195)

try:
    while True:
        # read values from ADC in each run and print it
        for i in range(8):
            value = adc.read_value(i)
            voltage = adc.read_voltage(i, value)
            # without value the digital value will be read
            print("|    ", value,"    | ", voltage," ",end = '')
            time.sleep(0.1)
        print("|")
        # wait 2 seconds
        time.sleep (2)
except KeyboardInterrupt:
    adc.close()