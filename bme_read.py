import time
import os
import bme280
import smbus2
import pymongo

from datetime import date

port = 0
address = 0x76

bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)
LOG_PATH = "sensor/bme280/"
os.makedirs(LOG_PATH, exist_ok=True)

while (True):
    bmedata = bme280.sample(bus, address, calibration_params)
    dat = (str(int(time.time())) + ", " + str(round(bmedata.temperature, 4))+", "+str(round(bmedata.pressure, 4))+", "+str(round(bmedata.humidity, 4))+"\r\n")
    json = {"time" : str(int(time.time())), "temperature": str(round(bmedata.temperature, 4)), "hudmidity" : str(round(bmedata.humidity, 4)), "pressure" : str(round(bmedata.temperature, 4))}
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Station"]
        mycol = mydb["meteo"]
        x = mycol.insert_one(json)
    except Exception as e:
        print(e)
    # print(x)
    log_file = open(LOG_PATH+str(date.today())+".csv", "a")
    log_file.write(dat)
    log_file.close()
    time.sleep(59)
