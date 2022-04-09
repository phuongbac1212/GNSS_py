import subprocess
from datetime import time

gnss_proc = subprocess.Popen(['python3', 'skytraq_read.py'], stdout=subprocess.PIPE)
bme_proc = subprocess.Popen(['python3', 'bme_read.py'], stdout=subprocess.PIPE)
me007_proc = subprocess.Popen(['python3', 'me008_read.py'], stdout=subprocess.PIPE)

while (True):
    gnss_dat = gnss_proc.stdout.readlines()
    bme_dat = bme_proc.stdout.readlines()
    me007_dat = me007_proc.stdout.readlines()

    print("gnss_dat = "+gnss_dat)
    print("bme_dat = "+bme_dat)
    print("me007_dat = "+me007_dat)
    time.sleep(0.1)
