channel = 12

try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
import time

begin_time = time.time()

def myCallback(pin):
	print("event on pin " + str(pin) + " at " + str(time.time()-begin_time))

if __name__ == '__main__':
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(channel, GPIO.FALLING, callback=myCallback)
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		pass
	GPIO.remove_event_detect(channel)
	GPIO.cleanup()
