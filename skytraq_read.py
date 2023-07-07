import binascii
import os
import subprocess
import time

import serial
import serial.tools.list_ports

import math
def getAlphaPort():
    for port, desc, hwid in serial.tools.list_ports.grep("VID:PID=10c4:ea60"):
        # print("{}: {} [{}]".format(port, desc, hwid))
        return port
    pass


SERIAL_PORT = getAlphaPort()

LOG_PATH = "/home/fang/Working/GNSS_py/"
SERIAL_RATE = 115200

os.makedirs(LOG_PATH, exist_ok=True)

gpsSerial = serial.Serial(SERIAL_PORT, SERIAL_RATE)
gps_week = math.floor((time.time() - 315964800) / 60 / 60 / 24 / 7)
gps_day = 8

os.makedirs(LOG_PATH + str(gps_week), exist_ok=True)
log_file = open(LOG_PATH + str(gps_week) + "/" + str(gps_week) + "_" + str(gps_day) + ".dat", "ab")

gpsSerial.flush()  # clean before reading...
send_msg = ''
while True:
    # reading data
    msg = gpsSerial.read_until(b'\x0d\x0a')
    if msg[0:2] != b'\xa0\xa1':
        send_msg = ''
        continue
    msg_len = int.from_bytes(msg[2:4], "big")
    while msg_len > len(msg) - 7:
        msg += gpsSerial.read_until(b'\x0d\x0a')

    msg_type = int.from_bytes(msg[4:5], "big")

    # append to var
    send_msg += binascii.hexlify(msg).decode('utf-8').lower()

    # update time and print output
    if msg_type == 0xE5:
        ts = int.from_bytes(msg[9:13], "big") / 1000
        if int.from_bytes(msg[7:9], "big") != gps_week or (ts // 60 // 60 // 24 % 7) != gps_day:
            gps_week = int.from_bytes(msg[7:9], "big")
            gps_day = int(ts // 60 // 60 // 24 % 7)
            os.makedirs(LOG_PATH + str(gps_week), exist_ok=True)
            log_file.close()
            try:
                subprocess.Popen(["gzip", "-f", log_file.name])
            except Exception as e:
                print(e)
            log_file = open(LOG_PATH + str(gps_week) + "/" + str(gps_week) + "_" + str(gps_day) + ".dat", "ab")

        #print(send_msg)
        send_msg =''

    log_file.write(msg)
    os.fsync(log_file.fileno())
    time.sleep(0.01)
