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
SERIAL_RATE = 4800
sm = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)
LOG_PATH = "sensor/sm/"
os.makedirs(LOG_PATH, exist_ok=True)

while True:
    try:
        sm.write([0x03, 0x03, 0x00, 0x00, 0x00, 0x0a, 0xc4, 0x2f])
        sm_data = sm.read_until(b'\x0103')
        print(" ".join("%02x" % b for b in sm_data))
        sm_val = (sm_data[3] * 256 + sm_data[4])/10
        tp_val = (sm_data[5] * 256 + sm_data[6])/10
        ec_val = sm_data[7] * 256 + sm_data[8]
        ph_val = (sm_data[9] * 256 + sm_data[10])/10
        n_val = sm_data[11] * 256 + sm_data[12]
        p_val = sm_data[7] * 256 + sm_data[8]
        k_val = sm_data[7] * 256 + sm_data[8]
        sal_val = sm_data[7] * 256 + sm_data[8]
        tds_val = sm_data[7] * 256 + sm_data[8]
        dat = (str(int(time.time())) + ", " + str(sm_val) +
               ", " + str(tp_val) +
               ", " + str(ec_val) +
               ", " + str(ph_val) +
               ", " + str(n_val) +
               ", " + str(p_val) +
               ", " + str(k_val) +
               ", " + str(sal_val)+", " + str(tds_val) + "\r\n")
        json = {"time":str(int(time.time())),
                "sm":str(sm_val),
                "tp":str(tp_val),
                "EC":str(ec_val),
                "pH":str(ph_val),
                "N":str(n_val),
                "P":str(p_val),
                "K":str(k_val),
                "salinity":str(sal_val),
                "TDS":str(tds_val)}

        try:
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["Station"]
            mycol = mydb["sm"]
            x = mycol.insert_one(json)
        except Exception as e:
            print(e)
        print(dat)
        log_file = open(LOG_PATH + str(date.today()) + ".csv", "a")
        log_file.write(dat)
        log_file.close()
    except:
        SERIAL_PORT = getRS485Port()
        sm = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)
    time.sleep(10)

