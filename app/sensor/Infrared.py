import RPi.GPIO as GPIO
import time


def init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(11,GPIO.IN)
	pass
def run():
	while True:
		inValue = GPIO.input(11)
		if inValue == True:
			print "Someone is closing!"
		else:
			print "Noanybody!"
		time.sleep(5)
time.sleep(5)
init()
run()
GPIO.cleanup()

