#! /usr/bin/env python
import NECreader
from omxplayerDBUSsend import omxplayer_dBus

# Chart: generic IR remote control from china
# It sends address 0 and (command)
#
# /-------------------------\
# | CH-(69) CH (70) CH+(71) |
# | |<<(68) >>|(64) >||(67) |
# |  - (07)  + (21) EQ (09) |
# |                         |
# |  0 (22) +1c(25) +2c(13) |
# |  1 (12)  2 (24)  3 (94) |
# |  4 (08)  5 (28)  6 (90) |
# |  7 (66)  8 (82)  9 (74) |
# \-------------------------/

class remoteControl:
	def __init__(s):
		s.bus = omxplayer_dBus()
		s.address = 0
		s.actions = [s.actPass for i in range(0,255)]
		s.actions[67] = s.actPlayPause
		s.actions[7] = s.actVolumeDown
		s.actions[21] = s.actVolumeUp
		s.actions[25] = s.actSeekBwd
		s.actions[13] = s.actSeekFwd
		s.actions[70] = s.actStop
		NECreader.setup(NECreader.channel)
		
	def actPass(s):
		pass
		
	def actPlayPause(s):
		s.bus.pause()

	def actVolumeUp(s):
		s.bus.volumeUp()

	def actVolumeDown(s):
		s.bus.volumeDown()

	def actSeekBwd(s):
		s.bus.seekStep(forward=False)

	def actSeekFwd(s):
		s.bus.seekStep()

	def actStop(s):
		s.bus.stop()
		
	def action(s,address,command):
		if address == s.address:
			s.actions[command]()
	
	def listen(s):
		NECreader.poolRC(s.action)
		
	def cleanup(s):
		NECreader.cleanup(NECreader.channel)
		
if __name__ == '__main__':
	rc = remoteControl()
	try:
		rc.listen()
	except KeyboardInterrupt:
		pass
	rc.cleanup()
