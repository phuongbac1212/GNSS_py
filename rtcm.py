import sys

import serial
import binascii


def getbitu(buff, pos, length):
    bits = 0
    for i in range(pos, pos + length):
        bits = (bits << 1) + ((buff[i // 8] >> (7 - i % 8)) & 1)
    return bits


def extractGPSTime(data):
    i = 24
    rtcmType = getbitu(data, i, 12)
    i += 12;
    # / *decode rtcm3 message * /
    if rtcmType == 1074 or rtcmType == 1075 or rtcmType == 1076 or rtcmType == 1077 or \
            rtcmType == 1094 or rtcmType == 1095 or rtcmType == 1096 or rtcmType or 1097 or \
            rtcmType == 1104 or rtcmType == 1105 or rtcmType == 1106 or rtcmType == 1107 or \
            rtcmType == 1114 or rtcmType == 1115 or rtcmType == 1116 or rtcmType == 1117:
        # / * GPS, GAL, SBS, QZS * /
        i += 12
        tow = getbitu(data, i, 30) * 0.001
        i += 30
        return tow

    if rtcmType == 1124 or rtcmType == 1125 or rtcmType == 1126 or rtcmType == 1127:
        # / * BDS * /
        i += 12;
        tow = getbitu(data, i, 30) * 0.001;
        i += 30;
        i += 1;
        tow += 14.0;  # / *BDT -> GPST * /
        return tow;
    return -1


def ByteToHexStr(byte):
    return binascii.hexlify(byte).decode('utf-8').upper()


def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


def getSingleRtcmMsg():
    dropMsg, rtcmFullmsg, rtcmDataFrame = [], [], []
    msgByteCount, rtcmId, rtcmLength = 0, 0, 0
    while True:
        nowByte = int(ByteToHexStr(gpsSerial.read(1)), base=16)
        if msgByteCount == 0:
            if nowByte == 211:  # 0xD3
                if len(dropMsg) != 0:
                    print("[UNKNOWN] : ", end="")
                    print(dropMsg)
                    dropMsg = []
            else:
                dropMsg.append(nowByte)
                print("---", dropMsg)
                continue
        elif msgByteCount == 1:
            rtcmLength = (nowByte & 3) << 8
        elif msgByteCount == 2:
            rtcmLength += nowByte
        elif msgByteCount <= 2 + rtcmLength:
            rtcmDataFrame.append(nowByte)
        # elif (msgByteCount > 2 + rtcmLength) and (msgByteCount <= (2 + rtcmLength) + 2):
        # 여기는 CRC 앞 두바이트
        elif msgByteCount == (2 + rtcmLength) + 3:
            rtcmFullmsg.append(nowByte)  # CRC 마지막 한바이트
            rtcmId = rtcmFullmsg[3]
            rtcmId = rtcmId << 4
            rtcmId = rtcmId | ((rtcmFullmsg[4] >> 4) or 15)
            return [rtcmFullmsg, rtcmDataFrame, rtcmId]
        msgByteCount += 1
        rtcmFullmsg.append(nowByte)


SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_RATE = 115200
gpsSerial = serial.Serial(SERIAL_PORT, SERIAL_RATE)
rtcmExplain = {1005: "Stationary RTK reference station ARP", 1074: "GPS MSM4", 1077: "GPS MSM7", 1084: "GLONASS MSM4",
               1087: "GLONASS MSM7", 1094: "Galileo MSM4", 1097: "Galileo MSM7", 1124: "BeiDou MSM4",
               1127: "BeiDou MSM7", 1230: "GLONASS code-phase biases",
               4072: "Reference station PVT (u-blox proprietary RTCM Message)"}
f = open("out.dat", "wb")
while True:
    rtcmMsg = getSingleRtcmMsg()
    rtcmex = rtcmExplain[rtcmMsg[2]] if rtcmMsg[2] in rtcmExplain else str(rtcmMsg[2])
    if rtcmMsg[2] == 1074:
        print(extractGPSTime(rtcmMsg[0]))
    #     a = int.from_bytes(rtcmMsg[0][6:10], byteorder="big", signed=False)
    #
    # else:
    #     a = 0
    # print("[RTCM] (", rtcmex, ") : ", a, "|", len(rtcmMsg[0]), "|", rtcmMsg[0])
    # f.write(bytearray(rtcmMsg[0]))
