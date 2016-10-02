channel = 12

try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
import time
#import threading.Timer as Timer
#from threading import Timer

lastTime = time.time()
newEvent = False
times = list()

def decodeRC():
	global newEvent
	newEvent = False
	#print("Button has been pressed, length of list of times: " + str(len(times)))
	if len(times) < 34:
		return
	ivs = [(u-v) for u,v in zip(times[1:],times)]
	data = [int(i>0.0012) for i in ivs[1:33]]
	#print(data)
	# decode address 
	a = 0
	b = 1
	for d in data[0:8]:
		a = a + b*d
		b = 2*b
	# decode command
	c = 0
	b = 1
	for d in data[16:24]:
		c = c + b*d
		b = 2*b
	print(a,c)	
	del times[:]

def myCallback(pin):
	global newEvent
	global lastTime
	lastTime = time.time()
	times.append(time.time())
	newEvent = True

if __name__ == '__main__':
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(channel, GPIO.FALLING, callback=myCallback)
	try:
		while True:
			time.sleep(0.5)
			if newEvent and time.time() > (lastTime + 0.03): 
				decodeRC()
	except KeyboardInterrupt:
		pass
	GPIO.remove_event_detect(channel)
	GPIO.cleanup()
