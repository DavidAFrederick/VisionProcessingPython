import gpiod
import time
from gpiod.line import Direction, Value


# Define the GPIO line used for communication
DHT22_GPIO_PIN = 4 
CHIP = "/dev/gpiochip0"


# Function to read data from DHT22 sensor
def read_dht22_data(chip, line):
    print ("1")
    # Send start signal
    line.release()
    line = gpiod.request_lines( CHIP,  config={DHT22_GPIO_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)})
    print ("2")
    # line.set_value(0)
    line.set_value(DHT22_GPIO_PIN,Value.INACTIVE)  # May not be needed
    time.sleep(0.01)
    print ("3")
    
    # line.set_value(1)
    line.set_value(DHT22_GPIO_PIN,Value.ACTIVE)

    time.sleep(0.00003)
    print ("4")


    line.release()
    line = gpiod.request_lines( CHIP,  config={DHT22_GPIO_PIN:  gpiod.LineSettings(direction=Direction.INPUT)})
    print ("5")

    # Read data bits
    data = []
    for _ in range(40):
        # while line.get_value() == 1:
        while (bool(line.get_value(DHT22_GPIO_PIN)) == True):
            print (" input:1 ",bool(line.get_value(DHT22_GPIO_PIN)))
            pass
        # while line.get_value() == 0:
        while (bool(line.get_value(DHT22_GPIO_PIN)) == False):
            print (" input:0 ",bool(line.get_value(DHT22_GPIO_PIN)))
            pass
        time.sleep(0.00003)
        # if line.get_value() == 1:
        if (bool(line.get_value(DHT22_GPIO_PIN)) == True):
            data.append(1)
        else:
            data.append(0)
        # if line.get_value() == 1:
        if (bool(line.get_value(DHT22_GPIO_PIN)) == True):
            pass

    # Convert data to bytes
    humidity_byte = bytes(data[0:8])
    humidity_decimal_byte = bytes(data[8:16])
    temperature_byte = bytes(data[16:24])
    temperature_decimal_byte = bytes(data[24:32])
    checksum_byte = bytes(data[32:40])

    # Convert bytes to integers
    humidity = int("".join(str(x) for x in humidity_byte), 2)
    temperature = int("".join(str(x) for x in temperature_byte), 2)
    checksum = int("".join(str(x) for x in checksum_byte), 2)

    # Verify checksum
    calculated_checksum = (humidity + temperature) & 0xFF
    if checksum != calculated_checksum:
        raise Exception("Checksum error")
    
    return humidity, temperature

# Main program
if __name__ == "__main__":
    # Get GPIO chip and line
    # chip = gpiod.Chip('gpiochip0')
    value_str = {Value.ACTIVE: "Active", Value.INACTIVE: "Inactive"}
    value = Value.ACTIVE

    chip = gpiod.Chip('/dev/gpiochip0')

    # line = chip.get_line(DHT22_GPIO_PIN)    
    # Configure GPIO line as output initially
    # line.request(consumer="dht22_reader", type=gpiod.LINE_REQ_DIR_OUT, default_val=1)

    line = gpiod.request_lines( CHIP,  config={DHT22_GPIO_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=value)})
    print ("Initial setup")
    try:
        while True:
            print ("Within loop")

            # Reconfigure GPIO line as input to receive data
            line.release()
            # line.request(consumer="dht22_reader", type=gpiod.LINE_REQ_DIR_IN)
            line = gpiod.request_lines( CHIP,  config={DHT22_GPIO_PIN:  gpiod.LineSettings(direction=Direction.INPUT)})
            print ("Changed Direction")
            
            # Read data and print
            humidity, temperature = read_dht22_data(chip, line)
            print(f"Humidity: {humidity}%, Temperature: {temperature}°C")
            
             # Reconfigure GPIO line as output after data is read
            line.release()
            # line.request(consumer="dht22_reader", type=gpiod.LINE_REQ_DIR_OUT, default_val=1)
            line = gpiod.request_lines( CHIP,  config={DHT22_GPIO_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.ACTIVE)})
            
            time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        line.release()
        chip.close()