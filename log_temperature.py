import time
import datetime
import os
import glob
import logging
import RPi.GPIO as GPIO
import temperature_probe
import mysql.connector
import record_SQL_data

# Configs
time_interval=5*60
brewID=1

# Log file information
logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)
handler=logging.FileHandler(os.getcwd()+"/"+
			datetime.datetime.now().strftime('temp_log_debug_%H_%M_%d_%m_%Y.log'))
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# Mysql startup info
mydb=mysql.connector.connect(
  host="localhost",
  user="dmueller",
  passwd="Spartan1",
  database="beerCode"
)
mycursor=mydb.cursor()

# Run main code to check temperature and operate heating/cooling
logger.info("Running main code...")
fout=open(datetime.datetime.now().strftime('temp_log_%H_%M_%d_%m_%Y.csv'),'w')
fout.write('time,temperature_air,temperature_liquid')
fout.write('\n')
try:
	while True:
		timeNow=datetime.datetime.now()
		temperature_air=temperature_probe.read_temp(0)
		temperature_liquid=temperature_probe.read_temp(1)
		logger.info("Current time: "+str(timeNow))
		logger.info("Current temperature, air: "+str(temperature_air))
		logger.info("Current temperature, liquid: "+str(temperature_liquid))
		fout.write(str(datetime.datetime.now())+','+str(temperature_air)+','+str(temperature_liquid))
		fout.write('\n')
		
		record_SQL_data.add_to_temp_log(mydb,mycursor,brewID,timeNow,temperature_air,temperature_liquid)
		
		time.sleep(time_interval)
finally:
	fout.close()
	mydb.close()
	print('Program ended, files closed.')
