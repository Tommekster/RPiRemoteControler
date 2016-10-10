#! /usr/bin/env python

import subprocess
import os

# References:
# 
# https://dbus.freedesktop.org/doc/dbus-python/api/frames.html
# http://stackoverflow.com/questions/9135263/how-to-export-an-object-on-a-custom-dbus-using-python
# https://dbus.freedesktop.org/doc/dbus-send.1.html
# http://free-electrons.com/pub/conferences/2016/meetup/dbus/josserand-dbus-meetup.pdf
#
# http://pythonhackers.com/p/popcornmix/omxplayer

class omxplayer_dBus:
	def __init__(s):
		s.address = ""
		s.destination = "org.mpris.MediaPlayer2.omxplayer"
		s.path = "/org/mpris/MediaPlayer2"
		s.interface = "org.freedesktop.DBus.Properties"
		s.iPlayer = "org.mpris.MediaPlayer2.Player"
		s.timeout = 500
		s.setOmxplayerBusAddress()

	def setOmxplayerBusAddress(s):
		user = "pi" # TODO username from system
		with open("/tmp/omxplayerdbus."+user,"r") as f:
			l = f.readline()
			s.address = l.rstrip() 

	def send(s, property="",args=[]):
		if s.address == "":
			s.setOmxplayerBusAddress()
		if property == "":
			property = s.interface+".Duration"
		
		my_env = os.environ
		my_env["DBUS_SESSION_BUS_ADDRESS"] = s.address
		dbus_send_cmd = ["dbus-send", "--print-reply=literal", "--session", "--reply-timeout="+str(s.timeout), "--dest="+s.destination, s.path, property]
		dbus_send_cmd.extend(args)
		#return " ".join(dbus_send_cmd)
		try:
			response = subprocess.check_output(dbus_send_cmd, env=my_env)
		except subprocess.CalledProcessError as e:
			print('CalledProcessError')
			print("Command: " + " ".join(dbus_send_cmd))
			print("Exit code: " + str(e.returncode))
			print("Output: " + str(e.output))
			return ""
		return response
	
	def getDuration(s):
		response = s.send(s.interface+".Duration")
		items = response.split()
		# if len(items) > 1: # TODO ochrana toho co leze z dbus-send
		duration = items[1]
		return int(duration)

	def getPosition(s):
		response = s.send(s.interface+".Position")
		items = response.split()
		position = items[1]
		return int(position)

	def getPlayStatus(s):
		response = s.send(s.interface+".PlaybackStatus")
		items = response.split()
		status = items[0]
		return str(status)
		
	def omxplayerAction(s,action):
		s.send(s.iPlayer+".Action",[action])

	def pause(s):
		s.omxplayerAction("int32:16")

	def volumeUp(s):
		s.omxplayerAction("int32:18")

	def volumeDown(s):
		s.omxplayerAction("int32:17")

	def stop(s):
		s.omxplayerAction("int32:15")
		
	def seek(s,position):
		s.send(s.iPlayer+".Seek",["int64:"+str(position)])
		
	def seekStep(s,forward=True):
		duration = s.getDuration()
		position = s.getPosition()
		newPosition = (2*bool(forward)-1)*duration/20+position
		newPosition = max(0,min(duration,int(newPosition)))
		s.seek(newPosition)

if __name__ == '__main__':
	b = omxplayer_dBus()
	print(b.getDuration())
	print(b.getPosition())
	print(b.getPlayStatus())
	b.pause()
