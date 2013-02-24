#!/usr/bin/env python2
# -*- encoding: Utf-8 -*-

import os, socket, select
import time, random

class ParrotServer():
    def __init__(self, parent, word, frequence):
		'''This function is the constructor for the ParrotServer class:
			* parent: the calling MainServer
			* word: the word we\'ll send
			* frequence: the frequence we\'ll wait'''
		# Default parameter, change it to desired value
		ParrotServer.min_frequence = 0.5

		# We initialize the parameters
		self.parent = parent
		self.word = word
		# If the frequence is correct, we keep it
		if frequence >= ParrotServer.min_frequence:
			self.frequence = frequence
		# If it's negative, we take a random smaller frequence
		elif frequence <= -1.0 * ParrotServer.min_frequence:
			self.frequence = -1.0*ParrotServer.min_frequence*random.random()
	# FIXME we have to handle the case where the frequence is not correct

    def send_word(self):
		'''This function sends the specified word at
		the specified frequence'''
		try:
			print '[PID: %5i] ParrotServer, sending %s' % (os.getpid(), self.word)
			while True:
				# We send the word to every client
				for client_socket in self.parent.client_sockets:
					client_socket.send(self.word)
			# And we sleep the desired frequence
			time.sleep(self.frequence)
		except KeyboardInterrupt:
			# When killed, we exit
			return	

