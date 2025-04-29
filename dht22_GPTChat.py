import gpiod
import time
from gpiod.line import Direction, Value

# Define the GPIO chip and line
CHIP_NAME = '/dev/gpiochip0'  # Adjust based on pin used, run `gpiodetect` and `gpiodinfo` to confirm
LINE_OFFSET = 4  # BCM GPIO number; change according to your wiring

# Timing constants (us = microseconds)
MAX_WAIT_TIME = 100  # Max wait in microseconds for pin state change
DHT_PULSE_TIMEOUT = 1000  # microseconds

def wait_for_level(line, level, timeout_us):
    """Wait for pin to reach a specific level, with a timeout."""
    start = time.perf_counter()
    while (time.perf_counter() - start) * 1_000_000 < timeout_us:
        if line.get_value() == level:
            return True
    return False

def read_dht22():
    with gpiod.Chip(CHIP_NAME) as chip:
        # line = chip.get_line(LINE_OFFSET)  #####
        line = gpiod.request_lines( CHIP_NAME,  config={LINE_OFFSET: gpiod.LineSettings(direction=Direction.OUTPUT,output_value=Value.INACTIVE)})

        config = gpiod.LineRequest()
        
        # 1. Send start signal (pull low for >1ms)
        config.request_type = gpiod.LineRequest.DIRECTION_OUTPUT
        line.request(config)
        line.set_value(0)
        time.sleep(0.0012)  # 1.2 ms
        line.set_value(1)
        time.sleep(0.00002)  # 20 us
        line.release()

        # 2. Switch to input
        config.request_type = gpiod.LineRequest.DIRECTION_INPUT
        config.consumer = "dht22"
        line.request(config)

        # 3. Read response
        if not wait_for_level(line, 0, DHT_PULSE_TIMEOUT):  # Sensor pulls low
            raise RuntimeError("DHT22 not responding (initial low)")
        if not wait_for_level(line, 1, DHT_PULSE_TIMEOUT):  # Sensor pulls high
            raise RuntimeError("DHT22 not responding (initial high)")
        if not wait_for_level(line, 0, DHT_PULSE_TIMEOUT):  # Sensor starts sending data
            raise RuntimeError("DHT22 not responding (data start)")

        # 4. Read 40 bits
        data = []
        for i in range(40):
            if not wait_for_level(line, 1, DHT_PULSE_TIMEOUT):
                raise RuntimeError(f"Bit {i}: no rising edge")
            start_time = time.perf_counter()
            if not wait_for_level(line, 0, DHT_PULSE_TIMEOUT):
                raise RuntimeError(f"Bit {i}: no falling edge")
            pulse_duration = (time.perf_counter() - start_time) * 1_000_000  # us
            data.append(1 if pulse_duration > 50 else 0)

        # 5. Convert to bytes
        bits = ''.join(str(bit) for bit in data)
        bytes_ = [int(bits[i:i+8], 2) for i in range(0, 40, 8)]

        # 6. Checksum
        if sum(bytes_[:4]) & 0xFF != bytes_[4]:
            raise RuntimeError("Checksum failed")

        humidity = ((bytes_[0] << 8) + bytes_[1]) / 10.0
        temperature = ((bytes_[2] & 0x7F) << 8 | bytes_[3]) / 10.0
        if bytes_[2] & 0x80:
            temperature = -temperature

        return humidity, temperature

# Run example
try:
    hum, temp = read_dht22()
    print(f"Temperature: {temp:.1f}°C, Humidity: {hum:.1f}%")
except RuntimeError as e:
    print(f"Error: {e}")
