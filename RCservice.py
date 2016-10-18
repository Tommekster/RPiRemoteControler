#! /usr/bin/env python
import NECreader
import socket

HOST = '127.0.0.1'
PORT = 50007

class RCservice:
	def __init__(s,host,port):
		s.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.socket.bind((host,port))
		s.socket.listen(1)
		s.socket.settimeout(0.5)
		s.history = []
		NECreader.setup(NECreader.channel)
		
	def rcEvent(s,address,command):
		s.history.append((address,command))
		
	def socketEvent(s,conn,addr):
		if len(s.history) == 0:
			conn.sendall("empty")
		else:
			button = s.history[-1]
			conn.sendall(str(button[0]) + " " + str(button[1]))
			s.history = []
		conn.close()
		
	def listen(s):
		while True:
			timeout = False
			try:
				conn, addr = s.socket.accept()
			except socket.timeout:
				timeout = True
			if not timeout:
				s.socketEvent(conn,addr)
			NECreader.callIfEvent(s.rcEvent)
		
	def cleanup(s):
		NECreader.cleanup(NECreader.channel)
		
if __name__ == '__main__':
	rc = RCservice(HOST,PORT)
	try:
		rc.listen()
	except KeyboardInterrupt:
		pass
	rc.cleanup()
