# import numpy
import RPi.GPIO as GPIO
import time


        # Define the GPIO pin number in BCM terms
        # This is physical Pin 7 on the left side just above the ground
MAGNETIC_SENSOR_PIN = 4
HEADING_MOTOR_PIN = 2

class SecurityCamera():

    def __init__(self) -> None:

        self.initialize_pwm_motor()
        self.initialize_heading_motor_sensor()

    def initialize_pwm_motor(self) -> None:
        print ("Initializing pwm_motor - ", end=" ")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(HEADING_MOTOR_PIN, GPIO.OUT)
        pwm_motor = GPIO.PWM(HEADING_MOTOR_PIN, 50)  # channel=2 frequency=50Hz
        pwm_motor.start(6.6)
        max_speed = 84/10
        min_speed = 56/10
        pwm_motor.ChangeDutyCycle(6.6)   # Set motor to stopped
        print ("Done")
        # return pwm_motor
        
    def initialize_heading_motor_sensor(self) -> None:        
        print ("Initializing Heading sensor - ", end=" ")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MAGNETIC_SENSOR_PIN, GPIO.IN, GPIO.PUD_UP)
        print ("Done")

    def monitor_magnetic_limit_switch(self)  -> bool:
        mag_switch = GPIO.input(MAGNETIC_SENSOR_PIN)
        return mag_switch
    
    def turn_heading_motor_until_limit(self, direction : str):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(HEADING_MOTOR_PIN, GPIO.OUT)
        pwm_motor = GPIO.PWM(HEADING_MOTOR_PIN, 50)  # channel=2 frequency=50Hz

        if (direction == "CW"):
            pwm_motor.start(8.4) # CW from top   
            print ("CW")
        if (direction == "CCW"):
            pwm_motor.start(5.6)    # CCV from top
            print ("CCW")

        start_time = time.time()
        allowed_duration = 1.0
        run_time = 0
        time.sleep(0.4)

        while (self.monitor_magnetic_limit_switch()) and (run_time < allowed_duration):
            run_time = time.time() - start_time
            print(f"Duration: {run_time:.2f}  Limit_switch: {self.monitor_magnetic_limit_switch()}  dir: {direction} " )

            if (direction == "CW"):
                pwm_motor.start(8.4) # CW from top   
            if (direction == "CCW"):
                pwm_motor.start(5.6)    # CCV from top
            time.sleep(0.1)


        pwm_motor.ChangeDutyCycle(6.6)   
        pwm_motor.stop()
        #  dc = 5.6 = counter clockwise
        


        pwm_motor.ChangeDutyCycle(6.6)   
        pwm_motor.stop()
        #  dc = 5.6 = counter clockwise
        



    def cleanup_GPIO(self):
        # led.cleanup()
        GPIO.cleanup()


# main.py
def main():
    print("This is the main function.")
    security_camera = SecurityCamera()
    print("Monitor: ", security_camera.monitor_magnetic_limit_switch())
    security_camera.turn_heading_motor_until_limit("CCW")
    security_camera.cleanup_GPIO()



if __name__ == "__main__":
    main()


