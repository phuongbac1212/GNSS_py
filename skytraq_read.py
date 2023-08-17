import binascii
import os
import time
import serial
import serial.tools.list_ports
import requests
import math

GLOBAL_API_URL = 'https://api_db.septentrio.eu.org/skytraq_upload'


def getAlphaPort():
    for port, desc, hwid in serial.tools.list_ports.grep("VID:PID=0403:6001"):
        # print("{}: {} [{}]".format(port, desc, hwid))
        return port
    pass


def checkMsg(messages, start, stop, cs):
    if not messages:
        return None  # Return None if no messages provided
    # Calculate XOR checksum
    checksum = 0
    for i in range(start, stop + 1):
        checksum ^= messages[i]
    return checksum == cs


SERIAL_PORT = getAlphaPort()

LOG_PATH = "./"
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
    if not checkMsg(messages=msg, start=4, stop=len(msg) - 4, cs=msg[len(msg) - 3]):
        print("checksum fail")
        continue
    # append to var
    send_msg += msg.hex()

    # update time and print output
    if msg_type == 0xE5:
        ts = int.from_bytes(msg[9:13], "big") / 1000
        if int.from_bytes(msg[7:9], "big") != gps_week or (ts // 60 // 60 // 24 % 7) != gps_day:
            gps_week = int.from_bytes(msg[7:9], "big")
            gps_day = int(ts // 60 // 60 // 24 % 7)
            os.makedirs(LOG_PATH + str(gps_week), exist_ok=True)
            log_file.close()
            log_file = open(LOG_PATH + str(gps_week) + "/" + str(gps_week) + "_" + str(gps_day) + ".dat", "ab")
        # print(send_msg)
        try:
            json = {"GpsWeek": gps_week,
                    "GpsTow": ts,
                    "skytraq": send_msg}
            x = requests.post(GLOBAL_API_URL, json)
            print(x)
        except Exception as e:
            print("send" + e)
        send_msg = ''
    try:
        log_file.write(msg)
        os.fsync(log_file.fileno())
    except Exception as e:
        print(e)
    time.sleep(0.01)
