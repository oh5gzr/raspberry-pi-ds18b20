#Python script for reading temperature data from 1-wire sensors such as a DS18B20 and saving the output into a file.
#Temperature readings are handled in celcius, bacause anybody with any living braincells only uses the metric system of measurement.
#Tested on Raspberry Pi A+ and B+ running Raspbian Linux.
#Run as root or make nessesary chnages to user priviledges.

import os
import time


#Uncomment these if the kernel modules are not loaded by other means like /etc/modules.
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

#------------------------------------------------------------------------
#Variables
#------------------------------------------------------------------------

#This is the default path (Raspbian Linux) for 1-wire device data. Do not change unless you know what you are doing.
base_dir = '/sys/bus/w1/devices/'

#Change this value to the correct sensor directory. List your available devices by running 'ls /sys/bus/w1/devices/' on your system's console. 
device_folder = 'device id. e.g. 28-0000066f9c40'

#This sums up the complete path to said device. Do not change unless you know what you are doing.
device_file = base_dir + device_folder + '/w1_slave'

#This sets the script update interval in seconds.
delay = '30'

#Change this to the path of the output file.
output_file_path = '/path/to/output/file'

#------------------------------------------------------------------------
#The code
#------------------------------------------------------------------------

#Read raw output as separate lines. The raw data is formatted like this:
#
# 00 00 00 00 00 00 00 00 00 : crc=00 YES
# 00 00 00 00 00 00 00 00 00 t=00000
#
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#This section parses the raw data.	
def read_temp():

	#Strip the first line if it contains 'YES' in the end. Otherwise read the raw data again.
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
	
	#Find 't=' on the second line and capture the reseeding data into the variable temp_string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
		
		#Because the raw data contains the temperature value in millicelsius, we need to divide temp_string by 1000 and save it as temp_c.
        temp_c = float(temp_string) / 1000.0
        return temp_c

#This section handles writing output into a file.	 
while True:
		#Uncomment for unrounded degub output.
        #print(read_temp())
		
		#Open the output file as writable into and refer to it as 'f'
        f = open(output_file_path,'w')
		#Grab the output of read_temp and round it down into one decimal, then save it as a string variable 't'.
        t = str(round(read_temp(),1))
		
		#Write the rouded down output into the predefined output file and close the file.
        f.write( t, )
        f.close()
		
		#Wait for the time defined in the delay wariable and repeat.
        time.sleep(float(delay))
