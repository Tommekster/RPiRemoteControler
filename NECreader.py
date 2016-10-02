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

def list2num(l):
	b = 1
	n = 0
	for i in l:
		n = n + i*b
		b = 2*b
	return n

def printResult(a,c):
	print(a,c)

def decodeRC(callback = printResult):
	global newEvent
	newEvent = False
	if len(times) < 34:
		return
	ivs = [(u-v) for u,v in zip(times[1:],times)]
	data = [int(i>0.0012) for i in ivs[1:33]]
	address = list2num(data[0:8])
	command = list2num(data[16:24])
	callback(address, command)	
	del times[:]

def myCallback(pin):
	global newEvent
	global lastTime
	lastTime = time.time()
	times.append(time.time())
	newEvent = True

def setup(pin):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(pin, GPIO.FALLING, callback=myCallback)

def cleanup(pin):
	GPIO.remove_event_detect(pin)
	GPIO.cleanup()

def poolRC(callback = printResult):
	while True:
		time.sleep(0.5)
		if newEvent and time.time() > (lastTime + 0.03): 
			decodeRC(callback)

if __name__ == '__main__':
	setup(channel)
	try:
		poolRC()
	except KeyboardInterrupt:
		pass
	cleanup(channel)
