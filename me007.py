import os
import time
import serial
from datetime import date

SERIAL_PORT = "/dev/ttyUSB0"
SERIAL_RATE = 9600
me007 = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)
LOG_PATH = "/home/GNSS_py/sensor/me007/"

day = date.today()
os.makedirs(LOG_PATH, exist_ok = True)
log_file = open(LOG_PATH+str(day)+".csv", "a")

while (True):
    if (day != date.today()):
        log_file.close()
        day = date.today()
        log_file = open(LOG_PATH+str(day)+".csv", "a")

    try:
        #me007.flush()
        me007_data = me007.read_until(b'\xff')
        print(me007_data)
        dist = me007_data[0] * 256 + me007_data[1]

        dat = (str(int(time.time())) + ", " + str(dist) + "\r\n")
        print(dat)
        log_file.write(dat)
    except Exception as err:
        print("ERROR")
    time.sleep(0.1)

