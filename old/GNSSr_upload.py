import subprocess
import time
import os
import tempfile
bme_fifo = tempfile.mktemp()
me007_fifo = tempfile.mktemp()
os.mkfifo(bme_fifo)
os.mkfifo(me007_fifo)

bme_file = open(bme_fifo)
me007_file = open(me007_fifo)
gnss_proc = subprocess.Popen(['python3', 'skytraq_read.py'], stdout=bme_file)
#bme_proc = subprocess.Popen(['python3', 'bme_read.py'], stdout=bme_file)
#me007_proc = subprocess.Popen(['python3', 'me007_read.py'], stdout=subprocess.PIPE)

while (True):

    #gnss_dat = gnss_proc.stdout.readline()
    bme_dat = bme_file.read()
    #me007_dat = me007_proc.stdout.readline()

    print("gnss_dat = [")
    #print(gnss_dat)
    print("]")
    print(bme_dat)
    #print(me007_dat)
    #time.sleep(0.1)
