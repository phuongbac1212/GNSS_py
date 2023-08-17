import os
import time
from datetime import date
import serial.tools.list_ports
import requests

GLOBAL_API_URL = 'https://swagger.septentrio.eu.org/upload_aux'

def getRS485Port():
    return "/dev/ttyAMA2"
    # for port, desc, hwid in serial.tools.list_ports.grep("VID:PID=10C4:EA60"):
    #     # print("{}: {} [{}]".format(port, desc, hwid))
    #     return port
    # pass

SERIAL_PORT = getRS485Port()
SERIAL_RATE = 9600
sm = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)
LOG_PATH = "aux/"
os.makedirs(LOG_PATH, exist_ok=True)

while True:
    try:
        # read the atmospheric data
        try:
            sm.write([0x04, 0x03, 0x00, 0x00, 0x00, 0x04, 0x44, 0x5c])
            at_data = sm.read_until(b'\x0403')
            #print("0x04 |" + " ".join("%02x" % b for b in at_data))
            ap_val = at_data[0] * 256 + at_data[1]
            tp_val = at_data[4] * 256 + at_data[5]
            hm_val = at_data[6] * 256 + at_data[7]
        except Exception as e:
            print(e)
            ap_val = -1
            tp_val = -1
            hm_val = -1

        # read the soil moisture at address 0x03
        try:
            sm.write([0x03, 0x03, 0x00, 0x00, 0x00, 0x0a, 0xc4, 0x2f])
            sm_data = sm.read_until(b'\x0303')
            #print("0x03 |" + " ".join("%02x" % b for b in sm_data))
            sm_val = (sm_data[3] * 256 + sm_data[4])/10
            tp_val = (sm_data[5] * 256 + sm_data[6])/10
            ec_val = sm_data[7] * 256 + sm_data[8]
            ph_val = (sm_data[9] * 256 + sm_data[10])/10
            n_val = sm_data[11] * 256 + sm_data[12]
            p_val = sm_data[7] * 256 + sm_data[8]
            k_val = sm_data[7] * 256 + sm_data[8]
            sal_val = sm_data[7] * 256 + sm_data[8]
            tds_val = sm_data[7] * 256 + sm_data[8]
        except Exception as e:
            print(e)
            sm_val = -1
            tp_val = -1
            ec_val = -1
            ph_val = -1
            n_val = -1
            p_val = -1
            k_val = -1
            sal_val = -1
            tds_val = -1

        #read the wind direction at address 0x02
        try:
            sm.write([0x02, 0x03, 0x00, 0x00, 0x00, 0x02, 0xc4, 0x38])
            wd_data = sm.read_until(b'\x0203')
            #print("0x02 |"+" ".join("%02x" % b for b in wd_data))
            wd_val = wd_data[3] * 256 + wd_data[4]
        except Exception as e:
            print(e)
            wd_val = -1

        #read the wind speed at address 0x01
        try:
            sm.write([0x01, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x0a])
            ws_data = sm.read_until(b'\x0103')
            #print("0x01 |"+" ".join("%02x" % b for b in ws_data))
            ws_val = ws_data[3] * 256 + ws_data[4]
        except Exception as e:
            print(e)
            ws_val = -1

        dat = (str(int(time.time())) + ", " + str(sm_val) +
               ", " + str(tp_val) +
               ", " + str(ec_val) +
               ", " + str(ph_val) +
               ", " + str(n_val) +
               ", " + str(p_val) +
               ", " + str(k_val) +
               ", " + str(sal_val) +
               ", " + str(tds_val) +
               ", " + str(ws_val) +
               ", " + str(wd_val) +
               ", " + str(ap_val) +
               ", " + str(hm_val) +
               "\r\n")
        json = {"time":int(time.time()),
                "soil_moisture":sm_val,
                "temperature":tp_val,
                "EC":ec_val,
                "pH":ph_val,
                "N":n_val,
                "P":p_val,
                "K":k_val,
                "salinity":sal_val,
                "TDS":tds_val,
                "wind_speed" : ws_val,
                "wind_direction" : wd_val,
                "atmos_pressure" : ap_val,
                "humid" : hm_val}
        try:
            x = requests.post(GLOBAL_API_URL, json = json)
            print(x)
        except Exception as e:
            print(e)
        #print(dat)
        log_file = open(LOG_PATH + str(date.today()) + ".csv", "a")
        log_file.write(dat)
        log_file.close()
    except:
        SERIAL_PORT = getRS485Port()
        sm = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)
    time.sleep(60)

