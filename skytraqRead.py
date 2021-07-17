import binascii
import os
import struct
import time

import serial
import queue

from skytraqSend import skytraqSend

SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_RATE = 115200
gpsSerial = serial.Serial(SERIAL_PORT, SERIAL_RATE)


def ByteToHexStr(byte):
    return binascii.hexlify(byte).decode('utf-8').upper()


def checksum(bytes):
    cs = 0
    for b in bytes:
        cs ^= b
    return cs


def getSingleRtcmMsg():
    return gpsSerial.read_until(b'\r\n')


rtcmExplain = {0xE5: "Extended Raw Measurement Data v.1",
               0xE7: "",
               0xE8: "",
               0xDF: "Navigation stat",
               0xE1: "",
               226: "",
               224: " "}


def stqGetTow(bytes, type):
    if type == 0xDF:
        return struct.unpack('>d', bytes[9:17])[0]  # sai giờ


def stqGetWN(bytes, type):
    if type == 0xDF:
        return int.from_bytes(bytes[7:9], "big")


######################################################################
############# MAIN FUNCTION START FROM HERE###########################
######################################################################

queue = queue.Queue()
thread1 = skytraqSend(queue)
thread1.start()
sendMsg = ''
week = ((int(time.time()) - 315964782 - 18) // 60 // 60 // 24 // 7)
day = 8
try:
    os.mkdir("/home/fang/send/" + str(week))
except:
    print("folder exist")
log_file = open("/home/fang/send/" + str(week) + "/" + str(week) + "_" + str(day) + ".dat", "ab")

while True:
    msg = getSingleRtcmMsg()
    msgType = int.from_bytes(msg[4:5], "big")
    sendMsg += ByteToHexStr(msg)
    day_cur = stqGetTow(msg, msgType) // 60 // 60 // 24
    if day_cur != day:
        day = day_cur
        if day == 0:
            try:
                os.mkdir("/home/fang/send/" + str(week))
            except:
                print("folder exist")
        log_file = open("/home/fang/send/" + str(week) + "/" + str(week) + "_" + str(day) + ".dat", "ab")

    log_file.write(msg)
    if msgType == 0xDF:
        data2send = [sendMsg, stqGetWN(msg, msgType), stqGetTow(msg, msgType)]
        queue.put(data2send)
        sendMsg = ''
