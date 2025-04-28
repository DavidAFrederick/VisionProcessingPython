
import gpiod
import time
from gpiod.line import Direction, Value
# https://libgpiod.readthedocs.io/en/latest/python_api.html


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

    if (False):
        print (dht_line.get_value(DHT_PIN))
        print (dht_line.get_value(DHT_PIN))
        print (dht_line.get_value(DHT_PIN))
        print (dht_line.get_value(DHT_PIN))
        print (dht_line.get_value(DHT_PIN))
        print (dht_line.get_value(DHT_PIN))

        for index in range(500):
            print ( int(dht_line.get_value(DHT_PIN) == Value.INACTIVE), end="" )

        print("")


    time_now = time.time()

    # Reconfigure as input
    # dht_line.release()
    # dht_line = gpiod.request_lines( CHIP,  config={DHT_PIN:  gpiod.LineSettings(direction=Direction.INPUT, bias=gpiod.line.Bias.PULL_UP)})

    while True:
        current_time = time.time()
        # if current_time - time_now > 0.0002:     # Stop waiting after 200 uSec - Original
        if current_time - time_now > 0.004:     # Stop waiting after 200 uSec
            break
        # if (bool(dht_line.get_value(DHT_PIN)) == False):     original
        if (bool(dht_line.get_value(DHT_PIN) == Value.INACTIVE)):  #  Original
        # if (bool(dht_line.get_value(DHT_PIN) == Value.ACTIVE)):  Trying inverted data
            data.append(0)
        else:
            data.append(1)
    
    start = 0
    
    print ("Len(data): ", len(data))

    for counter in range(len(data)):
        print(data[counter], end="")
    print ("")
    # input("Paused")

    # find the first  transistion from Low  to High
    for i in range(len(data)):
        if data[i] == 0 and data[i+1] == 1:
            start = i + 2
            break
    
    data = data[start:]

    print ("Len(data): ", len(data), "    Start: ", start)

    for counter in range(len(data)):
        print(data[counter], end="")
    print ("")

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
    dht_line.release()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

try:
    humidity, temperature = read_dht22_data()
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
    else:
        print("Data read error")

except RuntimeError as error:
    print(error.args[0])
except Exception as error:
    print(error.args[0])
finally:
    cleanup_GPIO()