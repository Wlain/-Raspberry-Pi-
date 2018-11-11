import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)

while True:
	value = GPIO.input(21)
	if value == 0:
		print('right')
	else:
		print('not right')
	time.sleep(1)

