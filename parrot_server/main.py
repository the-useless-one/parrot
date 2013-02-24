#!/usr/bin/env python2
# -*- encoding: Utf-8 -*-

import sys
import MainServer

def main():
	if len(sys.argv) < 2:
		print 'usage: %s <port>' % sys.argv[0]
		return -1

	port = int(sys.argv[1])

	if port <= 0 or port > 65535:
		print 'error: port must be between 1 and 65535 (given value: %d)' % port
		return -1

	main_server = MainServer.MainServer(port)
	main_server.launch()

	return 0

if __name__ == '__main__':
	main()
	
