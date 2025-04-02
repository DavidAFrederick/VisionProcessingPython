import RPi.GPIO as GPIO
import time
# import keyboard
from sshkeyboard import listen_keyboard, stop_listening
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
p = GPIO.PWM(2, 50)
p.start(6.6)

p.stop()
GPIO.cleanup()
