channel = 12 # board 18

try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
import time

def myCallback(pin):
	print("event on pin " + str(pin) + " at " + str(time.time) + " " + GPIO.input(pin))

def print_value(pin):
	print str(GPIO.input(pin)),

if __name__ == '__main__':
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(channel, GPIO.FALLING, callback=print_value)
	try:
		while True:
			time.sleep(0.0001)
	except KeyboardInterrupt:
		pass
	GPIO.remove_event_detect(channel)
	GPIO.cleanup()
