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
# server part and a client part. This file calls the server
# part.
#
# https://github.com/the-useless-one/parrot
#
# Guillaume Chelfi and Yannick Méheut - Copyright 2013

import sys
import ParrotServer

def main():
	if len(sys.argv) < 2:
		print 'usage: %s <port>' % sys.argv[0]
		return -1

	port = int(sys.argv[1])

	if port <= 0 or port > 65535:
		print 'error: port must be between 1 and 65535 (given value: %d)' % port
		return -1

	parrot_server = ParrotServer.ParrotServer(port)
	parrot_server.launch()

	return 0

if __name__ == '__main__':
	main()
	
