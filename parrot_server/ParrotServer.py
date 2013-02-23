#!/usr/bin/env python2
#-*- encoding-: Utf-8 -*-

import os, socket
import WordServer

class ParrotServer():
    def __init__(self, port):
	'''This function is the ParrotServer class constructor:
	* port: the port to listen to'''
	# Default values, you can change them
	ParrotServer.default_words_frequences = [('vite', 0.8), ('BOUM', 1.0)]
	ParrotServer.max_word_servers = 10

	# We make sure the configuration is sound
	assert(len(ParrotServer.defautl_words_frequences) <= ParrotServer.max_word_servers)

	self.port = port

	# We initialize the socket, and tell the OS
	# we want to reuse the address
	self.socket = socket.socket()
	self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	self.socket.bind(('', self.port))
	self.socket.listen(5)

	# We initialize the ParrotServer's arguments
	self.word_servers = []
	self.child_pids = []
	self.client_sockets = []

    def add_word_server(self, word, frequence):
	'''This function adds a WordServer to the list of WordServers:
	* word: the word the WordServer should send
	* frequence: the frequence the WordServer should wait'''
	# We create a new WordServer, and append it to the list
	new_word_server = WordServer.WordServer(self, word, frequence)
	self.word_servers.append(new_word_server)

	# We fork, if in the child process, we start the WordServer.
	# If not, we add the PID to the list
	child_pid = os.fork()
	if child_pid:
	    self.child_pids.append(child_pid)
	else:
	    new_word_server.send_word()

    def launch(self):
	'''This function launches the ParrotServer. It will first
	add the default WordServers to the ParrotServer, then it
	will wait for client connections'''
	print 'Listening on %d' % self.port

	# For every (word, frequence) couples, we
	# add a word server
	for (word, frequence) in ParrotServer.default_words_frequences:
	    self.add_word_server(word, frequence)

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

