import os
import time
import serial
from datetime import date

SERIAL_PORT = "/dev/ttyS2"
SERIAL_RATE = 9600
me007 = serial.Serial(SERIAL_PORT, SERIAL_RATE)
LOG_PATH = "./sensor/me007/"

day = date.today()
os.makedirs(LOG_PATH, exist_ok = True)
log_file = open(LOG_PATH+str(day)+".csv", "a")

while (True):
    if (day != date.today()):
        log_file.close()
        day = date.today()
        log_file = open(LOG_PATH+str(day)+".csv", "a")

    try:
        me007.flush()
        me007_data = me007.read_until(b'\xff')
        if len(me007_data) >= 7:
            dist = me007_data[1] << 8 | me007_data[2]
            tempr = me007_data[3] << 8 | me007_data[4]
        else:
            dist = 0
            tempr = 0

        dat = (str(int(time.time())) + ", " + str(dist) + ", " + str(tempr)+"\r\n")
        print(dat)
        log_file.write(dat)
    except Exception as err:
        print("ERROR")
    time.sleep(0.0)

