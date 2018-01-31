#! /usr/bin/env python
import NECreader
import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 50007
DEBUG = True

class RCservice:
	def __init__(s,host,port):
		s.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.socket.bind((host,port))
		s.socket.listen(5)
		s.clients = []
		s.running = True
		NECreader.setup(NECreader.channel)
		def poolRC():
			while s.running:
				time.sleep(0.5)
				NECreader.callIfEvent(s.rcEvent)
		threading.Thread(target=poolRC).start()
		
	def rcEvent(s,address,command):
		if DEBUG: print("rcEvent "+str((address,command)))
		if len(s.clients) == 0: return
		disconnected = []
		if DEBUG: print("clients "+str(len(s.clients)))
		for c in s.clients:
			msg = str((address,command))+"\r\n"
			try: c.sendall(msg.encode('utf-8'))
			except: disconnected.append(c)
		s.clients = [c for c in s.clients if not c in disconnected]

	def listen(s):
		if not s.running: return
		while True:
			conn, addr = s.socket.accept()
			s.clients.append(conn)
			if DEBUG: print("new connection "+str(addr))
		
	def cleanup(s):
		s.running = False
		s.socket.close()
		NECreader.cleanup(NECreader.channel)
		
if __name__ == '__main__':
	rc = RCservice(HOST,PORT)
	try:
		rc.listen()
	except KeyboardInterrupt:
		pass
	rc.cleanup()
