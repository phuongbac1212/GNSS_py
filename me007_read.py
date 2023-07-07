import os
import time
import serial
from datetime import date

SERIAL_PORT = "/dev/ttyS2"
SERIAL_RATE = 9600
me007 = serial.Serial(SERIAL_PORT, SERIAL_RATE)
LOG_PATH = "./sensor/me007/"

os.makedirs(LOG_PATH, exist_ok = True)

while (True):
    try:
        me007_data = me007.read_until(b'\xff')
        if len(me007_data) >= 7:
            dist = me007_data[1] << 8 | me007_data[2]
            tempr = me007_data[3] << 8 | me007_data[4]
        else:
            dist = 0
            tempr = 0
        log_file = open(LOG_PATH+str(date.today())+".csv", "a")
        dat = (str(int(time.time())) + ", " + str(dist) + ", " + str(tempr)+"\r\n")
        log_file.write(dat)
        log_file.close()
    except Exception as err:
        print("ERROR")
    time.sleep(10)

