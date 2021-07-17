import os

cur_wn = 2162
day = 6

os.system("7z a -o{/home/fang/send/"+str(cur_wn)+"/} -t7z " + str(day) + ".dat -m9=LZMA2 -aoa")
os.system("rm /home/fang/send/"+str(cur_wn)+"/" + str(day)+".dat")
