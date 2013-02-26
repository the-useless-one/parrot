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
# server part and a client part. This file implements the client 
# part.
#
# https://github.com/the-useless-one/parrot
#
# Guillaume Chelfi and Yannick Méheut - Copyright 2013

import socket, sys

def main():
	if len(sys.argv) < 3:
		print 'usage: %s <host> <port>'
		return -1

	# We get the arguments, and check whether they're correct
	host = sys.argv[1]
	port = int(sys.argv[2])
	if port <= 0 or port > 65535:
		print 'error: port must be between 1 and 65535 (given value: %d)' % port
		return -1

	# We try to connect to the host
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'connecting to %s:%d' % (host, port)
	try:
		client_socket.connect((host, port))
	except IOError, msg:
		print 'error: couldn\'t connect to %s:%d\nmessage: %s' % (host, port, msg)
		return -1
	else:
		print 'connected to host'

	# This boolean value is here to specify if we are
	# receiving the words, or in "command" mode
	interactive_mode = False

	while True:
		try:
			# if we're in command mode
			if interactive_mode:
				try:
					# We prompt a basic shell
					cmd = raw_input('~$ ')
				# If the user types ^D, we disconnect
				except EOFError:
					print '\ndisconnecting from host'
					client_socket.close()
					break
				else:
					# If the user types these commands, we disconenct
					if cmd.lower() in ['exit', 'quit', 'q', 'disconnect']:
						print 'disconnecting from host'
						client_socket.close()
						break
					# Otherwise, we send it to the server
					else:
						client_socket.send(cmd)
			else:
				# If we display the words, we juste read
				# from the socket, and print it
				sys.stdout.write(client_socket.recv(8192))
				sys.stdout.flush()
		# If the user types ^C, we switch modes
		except KeyboardInterrupt:
			print '\nswitching modes'
			interactive_mode = not interactive_mode

	return 0

if __name__ == '__main__':
	main()
