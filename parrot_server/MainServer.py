#!/usr/bin/env python2
#-*- encoding-: Utf-8 -*-

import os, socket
import ParrotServer

class MainServer():
	def __init__(self, port):
		'''This function is the MainServer class constructor:
		* port: the port to listen to'''
		# Default values, you can change them
		MainServer.default_words_frequences = [('vite', 0.8), ('BOUM', 1.0)]
		MainServer.max_parrot_servers = 10

		# We make sure the configuration is sound
		assert(len(MainServer.default_words_frequences) <= MainServer.max_parrot_servers)

		self.port = port

		# We initialize the socket, and tell the OS
		# we want to reuse the address
		self.socket = socket.socket()
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('', self.port))
		self.socket.listen(5)

		# We initialize the MainServer's arguments
		self.parrot_servers = []
		self.child_pids = []
		self.client_sockets = []

	def add_parrot_server(self, word, frequence):
		'''This function adds a ParrotServer to the list of ParrotServers:
		* word: the word the ParrotServer should send
		* frequence: the frequence the ParrotServer should wait'''
		# We create a new ParrotServer, and append it to the list
		new_parrot_server = ParrotServer.ParrotServer(self, word, frequence)
		self.parrot_servers.append(new_parrot_server)

		# We fork, if in the child process, we start the ParrotServer.
		# If not, we add the PID to the list
		child_pid = os.fork()
		if child_pid:
			self.child_pids.append(child_pid)
		else:
			new_parrot_server.send_word()

	def launch(self):
		'''This function launches the MainServer. It will first
		add the default ParrotServers to the MainServer, then it
		will wait for client connections'''
		print 'Listening on %d' % self.port

		# For every (word, frequence) couples, we
		# add a ParrotServer
		for (word, frequence) in MainServer.default_words_frequences:
			self.add_parrot_server(word, frequence)

		try:
			while True:
				# We wait for a client to connect
				client_socket, (client_ip, client_port) = self.socket.accept()
				print 'New client from %s:%d' % (client_ip, client_port)

				# When he does, we add it to the other clients
				self.client_sockets.append(client_socket)
				self.client_sockets[-1].send('Connected to the parrot server. Have fun!\n')
		except KeyboardInterrupt:
			# When interrupted, we kill every child process,
			# we close the socket and exit
			for child_pid in self.child_pids:
				os.kill(child_pid, 9)
			self.socket.close()

