#!/usr/bin/env python2
#-*- encoding-: Utf-8 -*-

import os, socket, threading

class ParrotServer():
	def __init__(self, port):
		'''This function is the ParrotServer class constructor:
		* port: the port to listen to'''
		# Default values, you can change them
		ParrotServer.default_words_frequences = [('vite', 0.8), ('BOUM', 1.0)]
		ParrotServer.max_words = 5
		ParrotServer.greeting = 'Connected to useless\' parrot server. Have fun!\n'

		# We make sure the configuration is sound
		assert(len(ParrotServer.default_words_frequences) <= ParrotServer.max_words)

		self.port = port

		# We initialize the socket, and tell the OS
		# we want to reuse the address
		self.socket = socket.socket()
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('', self.port))
		self.socket.listen(5)

		# We initialize the ParrotServer's arguments
		self.words_frequences = []
		self.client_sockets = []

		for word,freq in ParrotServer.default_words_frequences:
			self.add_word_frequence(word, freq)

	def add_word_frequence(self, word, freq):
		'''This function will add a (word,frequence) couple to
		self.words_frequences. It will then call the send_word
		method, after having checked that there isn't too many
		words in the list:
		* word: word to add to the list
		* freq: frequence to add to the list'''
		# We check that the word isn't already in the list
		for w,f in self.words_frequences:
			if w == word:
				return

		# If it's not, we add it to the end of the list
		self.words_frequences.append((word, freq))
		# If there is too many elements, we delete the first one
		if len(self.words_frequences) > ParrotServer.max_words:
			deleted_word,_ = self.words_frequences.pop(0)
			print 'Deleted word \'%s\'' % deleted_word
		# If not, we have to add a timer
		else:
			self.send_word(len(self.words_frequences)-1)

		print 'New word added: (%s, %f)' % (word, freq)

	def send_word(self, i):
		'''This function sends the word, and launches a timer
		which will call the function again, after the time freq:
		* i: index of the (word,frequence) couple in the 
			self.words_frequences list'''
		word,freq = self.words_frequences[i]
		threading.Timer(freq, self.send_word, args=(i,)).start()
		for (client_socket, client_ip, client_port) in self.client_sockets:
			try:
				client_socket.send('%s ' % word)
			except:
				print 'Client %s:%d disconnected' % (client_ip, client_port)
				self.client_sockets.remove((client_socket, client_ip, client_port))

	def launch(self):
		'''This function launches the ParrotServer.'''
		print 'Listening on %d' % self.port

		try:
			while True:
				# We wait for a client to connect
				client_socket, (client_ip, client_port) = self.socket.accept()
				print 'New client from %s:%d' % (client_ip, client_port)

				# When he does, we add it to the other clients
				self.client_sockets.append((client_socket, client_ip, client_port))
				client_socket.send(ParrotServer.greeting)
		except KeyboardInterrupt:
			# When interrupted, we kill every timer,
			# we close the socket and exit
			for thread in threading.enumerate():
				if thread != threading.current_thread():
					thread.cancel()
			self.socket.close()

