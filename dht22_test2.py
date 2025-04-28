# import RPi.GPIO as GPIO
# import time

import gpiod
import time
from gpiod.line import Direction, Value
# https://libgpiod.readthedocs.io/en/latest/python_api.html


# DHT_PIN = 4  # GPIO pin connected to DHT22 data pin
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(DHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Constants
CHIP = "/dev/gpiochip0"
SW_LINE_OFFSET = 27
LED_LINE_OFFSET = 14
DHT_PIN = 4  # GPIO pin connected to DHT22 data pin

# Initialize the GPIO chip and set a line for output 
chip = gpiod.Chip(CHIP)
value_str = {Value.ACTIVE: "Active", Value.INACTIVE: "Inactive"}
value = Value.ACTIVE
dht_line = gpiod.request_lines( CHIP,  config={DHT_PIN:  gpiod.LineSettings(direction=Direction.INPUT, bias=gpiod.line.Bias.PULL_UP)})

##
def initialize_chip() -> None:
    chip = gpiod.Chip(CHIP)
    value_str = {Value.ACTIVE: "Active", Value.INACTIVE: "Inactive"}
    value = Value.ACTIVE
##
def initialize_input_pin() -> None:        
    print ("Initializing inputs - ", end=" ")
    dht_line = gpiod.request_lines( CHIP,  config={DHT_PIN:  gpiod.LineSettings(direction=Direction.INPUT, bias=gpiod.line.Bias.PULL_UP)})
    print ("Done")

def initialize_output_pin() -> None:        
    print ("Initializing outputs - ", end=" ")
    dht_line = gpiod.request_lines( CHIP,  config={DHT_PIN:  gpiod.LineSettings(direction=Direction.INPUT, bias=gpiod.line.Bias.PULL_UP)})
    print ("Done")

##
def cleanup_GPIO():
    dht_line.release()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def read_dht22_data():
    # data = []
    # time.sleep(1)
    # GPIO.setup(DHT_PIN, GPIO.OUT)
    # GPIO.output(DHT_PIN, GPIO.LOW)
    # time.sleep(0.018)
    # GPIO.output(DHT_PIN, GPIO.HIGH)
    # GPIO.setup(DHT_PIN, GPIO.IN)

    # pulse the DHT22 pin  go low then high
    print("1a")
    data = []
    print ("1b")
    # dht_line = gpiod.request_lines( CHIP,  config={DHT_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.ACTIVE)})
    dht_line = gpiod.request_lines( CHIP,  config={DHT_PIN: gpiod.LineSettings(direction=Direction.OUTPUT)})
    print("1c")
 
    time.sleep(1)
    dht_line.set_value(DHT_PIN,Value.INACTIVE)
    time.sleep(0.018)
    dht_line.set_value(DHT_PIN,Value.ACTIVE)

    print ("2")
    time_now = time.time()

    print ("3")
    # Reconfigure as input
    dht_line.release()
    print ("3a")
    dht_line = gpiod.request_lines( CHIP,  config={DHT_PIN:  gpiod.LineSettings(direction=Direction.INPUT, bias=gpiod.line.Bias.PULL_UP)})
    print ("4")

    line_status =  bool(dht_line.get_value(DHT_PIN)) 
    print ("line_status: ", line_status)

    while True:
        print ("5")
        current_time = time.time()
        if current_time - time_now > 0.0002:
            break
        print ("6")
        # if GPIO.input(DHT_PIN) == 0:
        if (bool(dht_line.get_value(DHT_PIN)) == False):
            data.append(0)
        else:
            data.append(1)
        print ("7")
    
    start = 0
    
    for i in range(len(data)):
        if data[i] == 0 and data[i+1] == 1:
            start = i + 2
            break
    
    data = data[start:]

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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

try:
    print ("1")
    humidity, temperature = read_dht22_data()
    print ("100")
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