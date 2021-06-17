import serial
import pyrebase
import time

# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = '/dev/ttyUSB0'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 115200

config = {
    "apiKey": "AIzaSyDBPqc_0dqLiCc6WonS6RV2ysI3ZR0BzRE",
    "authDomain": "radiant-striker-309317.firebaseapp.com",
    "databaseURL": "https://radiant-striker-309317-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "radiant-striker-309317",
    "storageBucket": "radiant-striker-309317.appspot.com",
    "messagingSenderId": "513180512814",
    "appId": "1:513180512814:web:73effc0509461669d7a5bf",
    "measurementId": "G-8VKD8RTR98"

}


def main():
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
    #
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    start_time = time.time()
    while True:

        reading = ser.readline()
        data = {
            "data": reading.hex(),
            "time": int(time.time())
        }
        result = db.push(data)
        print(reading.hex())
    # f.close()


if __name__ == "__main__":
    main()
