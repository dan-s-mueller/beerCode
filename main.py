import time
import datetime
import os
import glob
import logging
import RPi.GPIO as GPIO
import temperature_probe
import mysql.connector
import record_SQL_data
	
def read_config_file(config_file):
	# Standard function to read in config files.
	with open(config_file,"r") as file:
		lines=file.read().splitlines()
		configs=[]
		for line in lines:
			line=line.split(",")
			line[0]=float(line[0])
			configs=configs+[line]
	return configs

def initialize(file_name,time_inc,brew_id,database_flag,sql_user,sql_password):
	# Log file information
	logging.basicConfig(level=logging.DEBUG)
	logger=logging.getLogger(__name__)
	handler=logging.FileHandler(os.getcwd()+"/"+
				datetime.datetime.now().strftime("./logs/"+file_name+"_%H_%M_%d_%m_%Y.log"))
	handler.setLevel(logging.INFO)
	logger.addHandler(handler)
	print "Logger started: "+"./logs/"+file_name+"_%H_%M_%d_%m_%Y.log"

	# Mysql startup info
	if database_flag:
		mydb=mysql.connector.connect(
		  host="localhost",
		  user=sql_user,
		  passwd=sql_password,
		  database="beerCode"
		)
		mycursor=mydb.cursor()
		print "Intialized sql database"

	# Assign pinouts to relays
	logger.info("Reading config file data")
	pinout_config_file="pinout.config"
	pinout_data=read_config_file("./configs/"+pinout_config_file)	
	logger.info("Assigning pinouts to relays")
	for idx,pinout in enumerate(pinout_data):
		if pinout[1]=="relay_cool":
			relay_cool=int(pinout[0])
		if pinout[1]=="relay_hot":
			relay_hot=int(pinout[0])
	logger.debug("relay_cool: "+str(relay_cool))
	logger.debug("relay_hot: "+str(relay_hot))

	# Configure how the pins are interacted with
	logger.info("Configuring how the pins are interacted with")
	GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
	GPIO.setup([relay_cool,relay_hot], GPIO.OUT) # GPIO assign mode
	GPIO.output([relay_cool,relay_hot], GPIO.LOW) # Initialize all pinouts to off
	print "Configured pins for I/O"
	
	# Create csv file if it doesn't exist
	logger.info("Creating csv file if it doesn't exist")
	try:
		if os.path.getsize("./logs/"+file_name+".csv") > 0:
			# Non empty file exists
			# Read lines, then delete the last one in case it's a weirdo
			fout=open("./logs/"+file_name+".csv","r+")
			lines=fout.readlines()
			lines=lines[:-1]
			fout.close()
			
			# Rewrite the file without the last line
			fout=open("./logs/"+file_name+".csv",'w')
			fout.writelines([item for item in lines[:-1]])
			#fout.close()
			#fout=open("./logs/"+file_name+".csv","a")
			#fout.write('time,temperature_air,temperature_liquid,op_hot,op_cold')
			fout.write('\n')
		else:
			# File exists but is empty
			fout=open("./logs/"+file_name+".csv","w")
			fout.write('time,temperature_air,temperature_liquid,op_hot,op_cold')
			fout.write('\n')
	except:
		# File doesn't exist
		fout=open("./logs/"+file_name+".csv","w")
		fout.write('time,temperature_air,temperature_liquid,op_hot,op_cold')
		fout.write('\n')
	
	if database_flag:
		return fout,logger,mydb,mycursor
	else:
		return fout,logger

def run_system(fout,logger,file_name,temp_min,temp_min_tol,temp_max,temp_max_tol,write_to_database,mydb,mycursor):
	#try:
		#while True:
	# Run the main loop of the program
	logger.debug("setpoint_low: "+str(temp_min))
	logger.debug("setpoint_high: "+str(temp_max))
	logger.debug("trigger_cool: "+str(temp_min_tol))
	logger.debug("trigger_hot: "+str(temp_max_tol))
	
	timeNow=datetime.datetime.now()
	temperature_air=temperature_probe.read_temp(0)
	temperature_liquid=temperature_probe.read_temp(1)
	logger.info("Current time: "+str(timeNow))
	logger.info("Current liquid temperature: "+str(temperature_liquid))
	logger.info("Current outside temperature: "+str(temperature_air))
	logger.info("Tempearture between setpoints: "+
					str(temperature_liquid>temp_min and temperature_liquid<=temp_max))
	
	if temperature_liquid<=(temp_min+temp_min_tol):
		# Need to heat chamber
		GPIO.output(relay_cool, GPIO.LOW) # Turn off cooler, if on
		GPIO.output(relay_hot, GPIO.HIGH) # Turn on heater
		
		logger.debug("Chamber heating now. Resolving difference of "+
			str(temp_min+temp_min_tol-temperature_liquid)+" deg F")
		if write_to_database:
			record_SQL_data.add_to_temp_log(mydb,mycursor,brewID,timeNow,temperature_air,temperature_liquid,1,0)
		fout.write(str(timeNow)+','+str(temperature_air)+','+str(temperature_liquid)+',1,0')
		fout.write('\n')
		
		time.sleep(time_interval)
	elif temperature_liquid>=(temp_max+temp_max_tol):
		# Need to cool chamber
		GPIO.output(relay_cool, GPIO.HIGH) # Turn on cooler
		GPIO.output(relay_hot, GPIO.LOW) # Turn off heater, if on
		
		logging.debug("Chamber cooling now. Resolving difference of "+
			str(temp_max+temp_max_tol-temperature_liquid)+" deg F")
		if write_to_database:
			record_SQL_data.add_to_temp_log(mydb,mycursor,brewID,timeNow,temperature_air,temperature_liquid,0,1)
		fout.write(str(timeNow)+','+str(temperature_air)+','+str(temperature_liquid)+',0,1')
		fout.write('\n')
		
		time.sleep(time_interval)
	else:
		# Chamber within operational limits, do nothing
		GPIO.output(relay_cool, GPIO.LOW) # Turn off cooler, if on
		GPIO.output(relay_hot, GPIO.LOW) # Turn off heater, if on
		
		logging.debug("Fermenter is in the happy zone, everything's off.")
		if write_to_database:
			record_SQL_data.add_to_temp_log(mydb,mycursor,brewID,timeNow,temperature_air,temperature_liquid,0,0)
		fout.write(str(timeNow)+','+str(temperature_air)+','+str(temperature_liquid)+',0,0')
		fout.write('\n')
		
		time.sleep(time_interval)
	return fout,temperature_air,temperature_liquid
	#finally:
		#fout.close()
		#mydb.close()
		#GPIO.cleanup()
		#print('Program ended, files closed.')
