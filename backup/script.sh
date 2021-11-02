sudo dd if=/dev/sdc status=progress| gzip -9 > ARMBIAN-GNSS-Proj-30-10.img.gz
sudo dd if=/dev/sdc of=ARMBIAN-GNSS-Proj-30-10.img.gz count=5306367 status=progress

sudo zcat ARMBIAN-GNSS-Proj-30-10.img.gz | dd of=/dev/sdc status=progress
