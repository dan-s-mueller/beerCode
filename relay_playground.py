import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
relayControl_GPIO = [14,15]
delayTime=0.5
loops=10

try:
	GPIO.setup(relayControl_GPIO, GPIO.OUT) # GPIO assign mode
	for loop in range(loops):
		print str(loop)
		GPIO.output(relayControl_GPIO, GPIO.LOW) # out
		GPIO.output(relayControl_GPIO, GPIO.HIGH) # on
		time.sleep(delayTime)
		GPIO.output(relayControl_GPIO, GPIO.LOW) # out
		time.sleep(delayTime)
except:
	print '\nExited on loop '+str(loop)
finally:
	GPIO.cleanup()
