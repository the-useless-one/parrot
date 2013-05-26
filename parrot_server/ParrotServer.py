#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This file is a part of the Parrot project. Parrot consists on a
# server part and a client part. This file implements the server
# part.
#
# https://github.com/the-useless-one/parrot
#
# Guillaume Chelfi and Yannick Méheut - Copyright 2013

import os, socket, select, threading
from xml.dom.minidom import parseString

class ParrotServer():
	def __init__(self, configuration_file):
		'''This function is the ParrotServer class constructor:
		* port: the port to listen to'''
		# Open configuration file
		self.parse_configuration_file(configuration_file)

		# We make sure the configuration is sound
		assert(len(self.default_words_frequences) <= self.max_words)
		assert(self.port >= 1 and self.port <= 65535)


		# We initialize the socket, and tell the OS
		# we want to reuse the address
		self.socket = socket.socket()
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('', self.port))
		self.socket.listen(5)

		# We initialize the ParrotServer's arguments
		self.words_frequences = []
		self.client_sockets = []
		self.client_infos = []
		self.number_of_clients = 0

		print ('adding default words')
		for word,freq in self.default_words_frequences:
			self.add_word_frequence(word, freq)

	def parse_configuration_file(self, configuration_file):
		configuration_fd = open(configuration_file, 'r')
		configuration = parseString(configuration_fd.read())
		configuration_fd.close()

		self.port = int(configuration.getElementsByTagName('port')[0].attributes['value'].value)
		self.greeting = configuration.getElementsByTagName('greeting')[0].toxml().replace('<greeting>','').replace('</greeting>','')
		self.max_words = int(configuration.getElementsByTagName('max_words')[0].attributes['value'].value)
		self.default_words_frequences = []
		default_word_freq = configuration.getElementsByTagName('word_freq')

		for word_freq in default_word_freq:
			word = word_freq.attributes['word'].value
			freq = float(word_freq.attributes['freq'].value)
			self.default_words_frequences.append((word,freq))

		return 0

	def add_word_frequence(self, word, freq):
		'''This function will add a (word,frequence) couple to
		self.words_frequences. It will then call the send_word
		method, after having checked that there isn't too many
		words in the list:
		* word: word to add to the list
		* freq: frequence to add to the list'''
		# We encode the word in UTF-8
		word = word.encode('utf-8')
		# We check that the word isn't already in the list
		for w,f in self.words_frequences:
			if w == word:
				return

		# If it's not, we add it to the end of the list
		self.words_frequences.append((word, freq))
		# If there is too many elements, we delete the first one
		if len(self.words_frequences) > self.max_words:
			deleted_word,_ = self.words_frequences.pop(0)
			print ('deleted word \'%s\'' % deleted_word)
		# If not, we have to add a timer
		else:
			self.send_word(len(self.words_frequences)-1)

		print ('new word added: (%s, %f)' % (word, freq))

	def send_word(self, i):
		'''This function sends the word, and launches a timer
		which will call the function again, after the time freq:
		* i: index of the (word,frequence) couple in the 
			self.words_frequences list'''
		word,freq = self.words_frequences[i]
		threading.Timer(freq, self.send_word, args=(i,)).start()
		for i in range(self.number_of_clients):
			client_socket = self.client_sockets[i]
			client_ip, client_port = self.client_infos[i]
			try:
				client_socket.send(word + str.encode(' '))
			except IOError:
				print ('client %s:%d disconnected' % (client_ip, client_port))
				del self.client_sockets[i]
				del self.client_infos[i]
				self.number_of_clients -= 1

	def launch(self):
		'''This function launches the ParrotServer.'''
		print ('listening on %d' % self.port)

		try:
			while True:
				# We wait for incoming connexions
				incoming_connexions,_,_ = select.select([self.socket], [], [], 0.05)

				# We accept clients and add them to the client sockets list 
				for incoming_connexion in incoming_connexions:
					client_socket, (client_ip, client_port) = incoming_connexion.accept()
					print ('new client from %s:%d' % (client_ip, client_port))
					self.client_sockets.append(client_socket)
					self.client_infos.append((client_ip, client_port))
					self.number_of_clients += 1
					client_socket.send(str.encode(self.greeting) + str.encode('\n'))

				# We wait to see if clients want to add a word
				incoming_commands,_,_ = select.select(self.client_sockets, [], [], 0.05)

				# We execute the requested command
				for incoming_command in incoming_commands:
					try:
						cmd = incoming_command.recv(8192)
						if cmd:
							print ('received command %s' % bytes.decode(cmd))
					except IOError:
						pass
		except KeyboardInterrupt:
			# When interrupted, we kill every timer,
			# we close the socket and exit
			for thread in threading.enumerate():
				if thread != threading.current_thread():
					thread.cancel()
			self.socket.close()

