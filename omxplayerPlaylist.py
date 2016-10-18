#! /usr/bin/env python
#from omxplayerDBUSsend import omxplayer_dBus
from subprocess import PIPE,Popen

# omxplayer and dbus-send must be executed by the same user
# Thus I want to make omxplayer's playlist runs omxplayer as a subprocess.
# Usind stdin/stdout I probably don't need dBus anymore.
#
# http://stackoverflow.com/questions/16768290/understanding-popen-communicate
# https://github.com/brainfoolong/omxwebgui

class omxplayerSubprocess:
	left = "\x1b\x5b\x44"
	right = "\x1b\x5b\x43"
	down = "\x1b\x5b\x42"
	up = "\1b\x5b\x41"
	def __init__(s):
		s.p = Popen(["echo","ahoj"],stdin=PIPE,stdout=PIPE)
		
	def isOpen(s):
		v = s.p.poll()
		return not type(v)==int

	def _send_(s,cmd):
		if s.isOpen():
			s.p.stdin.write(cmd)
	
	def close(s):
		s._send_("q")
		
	def open(s,filename):
		if s.isOpen():
			s.close()
		s.p = Popen(["omxplayer","-o","both",str(filename)],stdin=PIPE,stdout=PIPE)

	def pause(s):
		s._send_("p")
		
	def volumeUp(s)
		s._send_("+")
		
	def volumeDown(s)
		s._send_("-")
		
	def seekFwd(s):
		s._send_(s.right)
		
	def seekBwd(s):
		s._send_(s.left)
		
	def seekFwdQuick(s):
		s._send_(s.up)
		
	def seekBwdQuick(s):
		s._send_(s.down)
		
class omxplayerPlaylist: # TODO
	def __init__(s):
		pass
		
if __name__ == '__main__': #TODO
	pass

