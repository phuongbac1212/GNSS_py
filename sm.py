import os
import time
from datetime import date
import pymongo
import serial.tools.list_ports


def getRS485Port():
    for port, desc, hwid in serial.tools.list_ports.grep("VID:PID=10C4:EA60"):
        # print("{}: {} [{}]".format(port, desc, hwid))
        return port
    pass


SERIAL_PORT = getRS485Port()
SERIAL_RATE = 9600
sm = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)
LOG_PATH = "sensor/sm/"
day = date.today()
os.makedirs(LOG_PATH, exist_ok=True)
log_file = open(LOG_PATH + str(day) + ".csv", "a")

while True:
    try:
        sm.write([0x01, 0x03, 0x00, 0x12, 0x00, 0x01, 0x24, 0x0f])
        sm_data = sm.read_until(b'\x0103')
        #print(" ".join("%02x" % b for b in sm_data))
        sm_val = sm_data[3] * 256 + sm_data[4]
        dat = (str(int(time.time())) + ", " + str(sm_val) + "\r\n")
        json = {"time" : str(int(time.time())), "sm" : str(sm_val)}
        try:
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["Station"]
            mycol = mydb["sm"]
            x = mycol.insert_one(json)
        except Exception as e:
            print(e)
        #print(dat)
        log_file = open(LOG_PATH + str(date.today()) + ".csv", "a")
        log_file.write(dat)
        log_file.close()
    except:
        SERIAL_PORT = getRS485Port()
        sm = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)
        log_file.write("not found")
    time.sleep(59)
