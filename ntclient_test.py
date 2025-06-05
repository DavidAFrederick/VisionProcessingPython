import time
from networktables import NetworkTables
import logging  # To see messages from networktables, you must setup logging
# 

#==(Initialize NetworkTables )========================
NetworkTables.initialize("192.168.1.223")
sd = NetworkTables.getTable("SmartDashboard")
# results = sd.putString ("rpi_zero_w_1_temperature", "3.14159")
# results = sd.putString ("rpi_zero_w_1_humidity", "3.14159")

logging.basicConfig(level=logging.DEBUG)# 

rpi_zero_w_1_temperature = "222.22"
rpi_zero_w_1_humidity = "3.33"
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Read the remote sensor
def  read_remote_sensors():
    sd.putString ("rpi_zero_w_1_temperature", "345")
    sd.putString ("rpi_zero_w_1_humidity", "123" ) 
    time.sleep(3)

    # print (f"rpi_zero_w_1_temperature {rpi_zero_w_1_temperature}    rpi_zero_w_1_humidity {rpi_zero_w_1_humidity}" )

    rpi_zero_w_1_temperature = float ( sd.getString ("rpi_zero_w_1_temperature", "88"))
    rpi_zero_w_1_humidity =    float ( sd.getString ("rpi_zero_w_1_humidity", "99" ) )
    print (f"rpi_zero_w_1_temperature {rpi_zero_w_1_temperature}    rpi_zero_w_1_humidity {rpi_zero_w_1_humidity}" )



for index in range(1000):
    read_remote_sensors()
    time.sleep(2)



