
import gpiod
import time
from datetime import datetime
from gpiod.line import Direction, Value
# https://libgpiod.readthedocs.io/en/latest/python_api.html


#  pip list
# Package               Version
# --------------------- ---------
# gpiod                 2.3.0     <<<  Required for Raspberry Pi 5 due to the new GPIO architecture
# numpy                 2.2.5
# opencv-contrib-python 4.11.0.86
# pip                   23.0.1
# setuptools            66.1.1
# sshkeyboard           2.3.1



# Constants
CHIP = "/dev/gpiochip0"
DHT_PIN = 4  # GPIO pin connected to DHT22 data pin
value_str = {Value.ACTIVE: "Active", Value.INACTIVE: "Inactive"}
value = Value.ACTIVE

# Initialize the GPIO chip and set a line for output 
chip = gpiod.Chip(CHIP)
dht_line = gpiod.request_lines( CHIP,  config={DHT_PIN: gpiod.LineSettings(direction=Direction.OUTPUT,output_value=value)})
dht_line.release()
time.sleep(1.0)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def read_dht22_data():

    data = []

    # Configure the DHT pin for output
    dht_line = gpiod.request_lines( CHIP,  config={DHT_PIN: gpiod.LineSettings(direction=Direction.OUTPUT,output_value=value)})

    # Pulse the DHT pin for 2 millisec
    dht_line.set_value(DHT_PIN,Value.INACTIVE)
    time.sleep(0.002)
    dht_line.set_value(DHT_PIN,Value.ACTIVE)
    dht_line.release()

    # Configure the  line for input  (Must be released from previous use)
    dht_line = gpiod.request_lines( CHIP,  config={DHT_PIN:  gpiod.LineSettings(direction=Direction.INPUT, bias=gpiod.line.Bias.PULL_UP)})

    time_now = time.time()

    # After we send the send the "start signal", sample the DHT pin as fast as you can for 4 milliseconds
    # Collect the raw data in a list.

    while True:
        current_time = time.time()
        if current_time - time_now > 0.004:     # Stop waiting after 4 milliSeconds
            break
        if (bool(dht_line.get_value(DHT_PIN) == Value.INACTIVE)):  
            data.append(0)
        else:
            data.append(1)
    
    start = 0

    # find the first  transistion from Low  to High
    for i in range(len(data)):
        if data[i] == 0 and data[i+1] == 1:
            start = i + 2
            break
    
    # Cut off unneeded initial data
    data = data[start:]

    if (False):    # Print the raw data
        print ("Len(data): ", len(data), "    Start: ", start)

        for counter in range(len(data)):
            print(data[counter], end="")
        print ("")

#
#  Example Raw data
#
# #
# Len(data):  887
# 11111100000000011111000000000001111100000000000111110000000000011111000000000001111100000000
# 00011111000000000001111100000000000111111111111111000000000001111111111111110000000000011111
# 11111111110000000000001111110000000000011111111111111110000000000001111111111111111000000000
# 00111111000000000001111111111111111100000000000111111000000000000111110000000000001111110000
# 00000001111110000000000001111100000000000011111100000000000111111000000000001111110000000000
# 00111111000000000001111111111111111000000000000111111111111111100000000000111111000000000001
# 11111000000000000111111111111111100000000000111111000000000000111111111111111100000000000111
# 11111111111111000000000001111111111111111000000000000111110000000000001111111111111111000000
# 00000111111000000000000111110000000001111111111111111000000000000111111111111111100000000000
# 11111100000000000111111111111111111111111111111111111111111

  # Now that we have a list of raw data, parse the data breaking at each transition from low(1) to high(1).
  # We are creating a list of lists
  # [ [number of ones, number of zeros, bit value], [number of ones, number of zeros, bit value], ]

  # zero the variables: number_ones, number_zeros, bit value
    number_ones = 0
    number_zeros = 0
    bit_value = None
    raw_data_list = []
    element_value = []
# loop through each value
    for index in range (len(data)-1):
        sample_value = data[index]
        next_sample_value = data[index+1]
        
        if (sample_value == 1):
            number_ones = number_ones + 1

        if (sample_value == 0):
            number_zeros = number_zeros + 1

        if (sample_value == 0) and (next_sample_value == 1):  # Detect a low to high transistion
            if (number_ones < 8):     #### <<<  This value may need to change or be a percentage !!!
                bit_value = 0         ### Need to see if processor loading changes the raw data sampling rate
            else:
                bit_value = 1
        # Create the inner list value then appended it to the outer list.
            element_value = [number_ones,number_zeros,bit_value]
            raw_data_list.append(element_value)

            #  Clear everthing and repeat
            number_ones = 0
            number_zeros = 0
            bit_value = None

    #  Convert the raw data list of lists into a new parsed list of resultant bits
    new_data = []

    number_of_rows = 0
    for index in raw_data_list:
        number_of_rows = number_of_rows + 1
        new_data.append(index[2])
    
    data = new_data

    # Troubleshooting - print the  40 bits
    if (False):
        for index in range(len(data)):
            if (data[index]==1): print ("1",end="")
            if (data[index]==0): print ("0",end="")
        print("   length:", len(data))
        print("")
    # The following code was pulled from the internet.

    humidity_bits = data[0:8]
    humidity_decimal_bits = data[8:16]
    temperature_bits = data[16:24]
    temperature_decimal_bits = data[24:32]
    checksum_bits = data[32:40]

    humidity = 0
    for bit in humidity_bits:
        humidity = (humidity << 1) | bit
    
    humidity_decimal = 0
    for bit in humidity_decimal_bits:
        humidity_decimal = (humidity_decimal << 1) | bit

    temperature = 0
    for bit in temperature_bits:
        temperature = (temperature << 1) | bit
    
    temperature_decimal = 0
    for bit in temperature_decimal_bits:
        temperature_decimal = (temperature_decimal << 1) | bit

    checksum = 0
    for bit in checksum_bits:
        checksum = (checksum << 1) | bit
    
    calculated_checksum = (humidity + humidity_decimal + temperature + temperature_decimal) & 0xFF

    if checksum == calculated_checksum:
        return humidity + humidity_decimal / 10, temperature + temperature_decimal / 10
    else:
        return None, None


##
def cleanup_GPIO():
    # dht_line.release()    ## Not working
    chip.close()
    pass

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

try:
    for counter in range (2000):
        humidity, temperature = read_dht22_data()
        temperature_fahrenheit = 9/5 * temperature + 32
        if humidity is not None and temperature is not None:
            now = datetime.now()
            print(f"Time: {now.strftime('%Y-%m-%d %H:%M:%S') } Temperature: {temperature_fahrenheit:.1f}°F, Humidity: {humidity:.1f}%")
        else:
            # print("Data read error")
            pass
        time.sleep(5)

except RuntimeError as error:
    print(error.args[0])
except Exception as error:
    print(error.args[0])
finally:
    cleanup_GPIO()