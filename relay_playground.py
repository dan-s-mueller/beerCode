import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
# relayControl_GPIO = [14,15]
relayControl_GPIO = 14
timeOn=2
timeOff=2
loops=10

try:
	GPIO.setup(relayControl_GPIO, GPIO.OUT) # GPIO assign mode
	for loop in range(loops):
		print str(loop)
		GPIO.output(relayControl_GPIO, GPIO.HIGH) # out
		GPIO.output(relayControl_GPIO, GPIO.HIGH) # on
		time.sleep(timeOn)
		GPIO.output(relayControl_GPIO, GPIO.HIGH) # out
		time.sleep(timeOff)
except:
	print '\nExited on loop '+str(loop)
finally:
	GPIO.cleanup()
