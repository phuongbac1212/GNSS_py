import time
import os
import bme280
import smbus2

from datetime import date

port = 0
address = 0x76
try:
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)
except Exception as err:
    print("ERROR")

LOG_PATH = "./sensor/bme280/"
os.makedirs(LOG_PATH, exist_ok=True)
day = date.today()
log_file = open(LOG_PATH+str(day)+".csv", "a")

while (True):
    if (day != date.today()):
        log_file.close()
        day = date.today()
        log_file = open(LOG_PATH+str(day)+".csv", "a")

    try:
        bmedata = bme280.sample(bus, address, calibration_params)
        dat = (str(int(time.time())) + ", " + str(round(bmedata.temperature, 4))+", "+str(round(bmedata.pressure, 4))+", "+str(round(bmedata.humidity, 4))+"\r\n")
        print(dat)
        log_file.write(dat+"\n")
    except Exception as err:
        print("ERROR")
        bmedata = None
    time.sleep(0.1)

