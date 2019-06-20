import os
import glob
import time
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
 
def read_temp_raw(probeID):
    # [0] is air temp
    # [1] is liquid temp
    device_folder = glob.glob(base_dir + '28*')[probeID]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp(probeID):
    # [0] is air temp
    # [1] is liquid temp
    lines = read_temp_raw(probeID)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(probeID)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0	# convert from deg c to deg f
        return temp_f
