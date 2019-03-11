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
			datetime.datetime.now().strftime('main_%H_%M_%d_%m_%Y.log'))
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# Assign constants that shouldn't be changed often.
time_interval=2

# Read config file settings to establish run parameters.
logger.info("Reading config file data")
pinout_config_file="pinout.config"
temperature_config_file="temperature_settings.config"
pinout_data=read_config_file(pinout_config_file)
temperature_settings=read_config_file(temperature_config_file)

# Assign pinouts to relays
logger.info("Assigning pinouts to relays")
for idx,pinout in enumerate(pinout_data):
	if pinout[1]=="relay_cool":
		relay_cool=pinout[0]
	if pinout[1]=="relay_hot":
		relay_hot=pinout[0]
logger.debug("relay_cool: "+str(relay_cool))
logger.debug("relay_hot: "+str(relay_hot))

# Assign temperature run parameters
logger.info("Assigning temperature to run parameters")
for idx,temperature_config in enumerate(temperature_settings):
	if temperature_config[1]=="setpoint_low":
		setpoint_low=temperature_config[0]
	if temperature_config[1]=="setpoint_high":
		setpoint_high=temperature_config[0]
	if temperature_config[1]=="trigger_cool":
		trigger_cool=temperature_config[0]
	if temperature_config[1]=="trigger_hot":
		trigger_hot=temperature_config[0]
logger.debug("setpoint_low: "+str(setpoint_low))
logger.debug("setpoint_high: "+str(setpoint_high))
logger.debug("trigger_cool: "+str(trigger_cool))
logger.debug("trigger_hot: "+str(trigger_hot))

# Configure how the pins are interacted with
logger.info("Configuring how the pins are interacted with")
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setup([relay_cool,relay_hot], GPIO.OUT) # GPIO assign mode
GPIO.output([relay_cool,relay_hot], GPIO.LOW) # Initialize all pinouts to off

# Run main code to check temperature and operate heating/cooling
logger.info("Running main code...")
while True:
	temperature_chamber=temperature_probe.read_temp()
	logger.info("Current time: "+str(datetime.datetime.now()))
	logger.info("Current temperature: "+str(temperature_chamber))
	logger.info("Tempearture between setpoints: "+
					str(temperature_chamber>setpoint_low and temperature_chamber<=setpoint_high))
	if temperature_chamber<=(setpoint_low+trigger_cool):
			GPIO.output(relay_cool, GPIO.LOW) # Turn off cooler, if on
			GPIO.output(relay_hot, GPIO.HIGH) # Turn on heater
			logger.debug("Chamber heating now. Resolving difference of "+
				str(setpoint_low+trigger_cool-temperature_chamber)+" deg F")
			time.sleep(time_interval)
	elif temperature_chamber>=(setpoint_high+trigger_hot):
		GPIO.output(relay_cool, GPIO.HIGH) # Turn on cooler
		GPIO.output(relay_hot, GPIO.LOW) # Turn off heater, if on
		logging.debug("Chamber cooling now. Resolving difference of "+
			str(setpoint_high+trigger_hot-temperature_chamber)+" deg F")
		time.sleep(time_interval)
	else:
		GPIO.output(relay_cool, GPIO.LOW) # Turn off cooler, if on
		GPIO.output(relay_hot, GPIO.LOW) # Turn off heater, if on
		logging.debug("Fermenter is in the happy zone, everything's off.")
		time.sleep(time_interval)
