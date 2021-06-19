import sys

import requests
import time
import threading

class rtcmSend(threading.Thread):
  # overriding constructor
  def __init__(self, queue):
    # calling parent class constructor
    threading.Thread.__init__(self)
    self.import_url = 'http://112.137.134.7:5000/data'
    self.queue = queue

  # define your own run method
  def run(self):
    while True:
        if self.queue.qsize() >= 1:
            # print("not emplty", self.queue.qsize())
            rtcm_data = self.queue.get()
            data = {
                "data": rtcm_data[0],
                "time": rtcm_data[2],
                "GPS_Week": rtcm_data[1],
                "stationID": "pipi"
            }
            try:
                x = requests.post(self.import_url, data=data)
                print(x, "\t time=", rtcm_data[2], "\t size=", sys.getsizeof(rtcm_data[0]))
            except Exception as err:
                print(err.args)
            time.sleep(0.5)

