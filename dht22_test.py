#  pip install Adafruit_DHT


import Adafruit_DHT
import time

DHT_PIN = 4  # GPIO pin connected to the DHT22 data pin
DHT_TYPE = Adafruit_DHT.DHT22

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.1f}C")
        print(f"Humidity: {humidity:.1f}%")
    else:
        print("Failed to retrieve data from DHT22 sensor")
    time.sleep(2)