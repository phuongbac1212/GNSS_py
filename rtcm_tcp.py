import socket
from pyrtcm import RTCMReader
import requests
import time
class TCPConnection:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            print('Successful Connection')
        except:
            print('Connection Failed')

    def readlines(self):
        data = self.sock.recv(9999)
        return data


GLOBAL_API_URL = 'https://api_db.septentrio.eu.org/rtcm_upload'

if __name__ == '__main__' : 
    listen = TCPConnection()
    listen.connect('192.168.1.3', 4321)

    f = open("testrtcm.dat", "wb")
    while (True):
        rawMsg = listen.readlines()
        f.write(rawMsg)
        try:
            msg = RTCMReader.parse(rawMsg)
            ts = (rawMsg[6] << 24 | rawMsg[7] << 16 | rawMsg[8] << 8 | rawMsg[9]) >>2
            json = {"UTCtime": int(time.time()),
                    "GPSepoch": ts,
                    "rtcm_msg": rawMsg.hex()}
            x = requests.post(GLOBAL_API_URL, json, timeout=2)
            #print(x)
        except Exception as e:
            print(e)
        time.sleep(0.001)



