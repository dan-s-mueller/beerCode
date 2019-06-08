import time
import datetime
import os
import glob
import logging
import RPi.GPIO as GPIO
import temperature_probe
	
def read_config_file(config_file):
	# Standard function to read in config files.
	with open(config_file,"r") as file:
		lines=file.read().splitlines()
		configs=[]
		for line in lines:
			line=line.split(",")
			line[0]=int(line[0])
			configs=configs+[line]
	return configs

# Log file information
logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)
handler=logging.FileHandler(os.getcwd()+"/"+
			datetime.datetime.now().strftime('./logs/proof_test_%H_%M_%d_%m_%Y.log'))
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# Read config file settings to establish run parameters.
logger.info("Reading config file data")
pinout_config_file="pinout.config"
pinout_data=read_config_file("./configs/"+pinout_config_file)

# Assign pinouts to relays
logger.info("Assigning pinouts to relays")
for idx,pinout in enumerate(pinout_data):
	if pinout[1]=="relay_cool":
		relay_cool=pinout[0]
	if pinout[1]=="relay_hot":
		relay_hot=pinout[0]
logger.debug("relay_cool: "+str(relay_cool))
logger.debug("relay_hot: "+str(relay_hot))

# Configure how the pins are interacted with
logger.info("Configuring how the pins are interacted with")
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setup([relay_cool,relay_hot], GPIO.OUT) # GPIO assign mode
GPIO.output([relay_cool,relay_hot], GPIO.LOW) # Initialize all pinouts to off

# Run main code to proof test system.
logger.info("Running proof test...")
time_interval=1.5		# Interval in seconds for when the system alternates
test_duration=60*60*3	# Total duration for the test in seconds
start=time.time()
counter=0
try:
	while (time.time()-start)<test_duration:
		timeNow=datetime.datetime.now()
		logger.info("Time remaining: "+str(datetime.timedelta(seconds=(test_duration-(time.time()-start)))))
		
		# Heat chamber
		GPIO.output(relay_cool, GPIO.LOW) # Turn off cooler, if on
		GPIO.output(relay_hot, GPIO.HIGH) # Turn on heater
		logger.debug("Chamber heating now.")
		time.sleep(time_interval)
		# Cool chamber
		GPIO.output(relay_cool, GPIO.HIGH) # Turn on cooler
		GPIO.output(relay_hot, GPIO.LOW) # Turn off heater, if on
		logging.debug("Chamber cooling now.")
		time.sleep(time_interval)
		counter=counter+1
finally:
	GPIO.cleanup()
	print('Proof test complete. Cycles completed: '+str(counter))
