import serial
import requests
import time

# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = '/dev/ttyUSB0'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 115200
# f = open("/home/orangepi/log.txt", "ab");
import_url = 'http://112.137.134.7:5000/data'
def main():
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
    while True:
        reading = ser.readline()
        data = {
            "data": reading.hex(),
            "time": int(time.time()),
            "stationID": "?"
        }
        try :
            print(reading.hex())
        except Exception as e:
            print(".")
        # f.write(reading)
        try :
            x = requests.post(import_url, data=data)
        except Exception as err:
            print(err)

if __name__ == "__main__":
    main()
