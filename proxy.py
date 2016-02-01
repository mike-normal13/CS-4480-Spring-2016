#!/usr/bin/python

import sys
from socket import *

# port members
listen_port = 80
server_port = 80		#	TODO:	we will assume for now that any server this proxy sends a request to 
						#				will be listening on port 80

#	client message storage member
client_message = ''
#	message sent by client parsed to an array
client_message_array = []

# flag indicating a connection has been made between the proxy and the client.
valid_client_message = False

# will be parsed from 'client_message'
client_requested_host = ''		
client_requested_URL = ''

# response from the server
server_response = ''

# part of the message from client in the URL after the host name.
index_in = ''

# Get port
if len(sys.argv) != 1:
	listen_port = sys.argv[1]

# convert port to integer for good measure
listen_port = int(listen_port)

#	socket the proxy will be using to communicate with the client, this socket will be the doorway knocked on first.
client_sock = socket(AF_INET, SOCK_STREAM)
#	Socket the proxy will use to communicate with next node in the network
out_sock = socket(AF_INET, SOCK_STREAM)

client_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

client_sock.bind((client_requested_host, listen_port))
client_sock.listen(1)			#	1 for now...

print 'proxy is waiting for client to connect'

while valid_client_message == False:
	dedicated_con_sock, addr = client_sock.accept()
	client_message = dedicated_con_sock.recv(1024)
	
	#	parse the client message to an array
	client_message_array = client_message.split(' ')

	#	some checks for proper formating
	#if client_message_array[2]

	#	check that the client sent a GET request
	if client_message_array[0] == 'GET':
		# TODO:	do further parsing to determine if the message from the client is valid

		# get URL
		client_requested_URL = client_message_array[1]

		# a few checks
			#	check for absoulute URI
		if (client_requested_URL.startswith('http://')) or (client_requested_URL.startswith('https://')):
			s = 2				# PYTHON!!!
		else:
			dedicated_con_sock.send('HTTP/1.0 400 Bad Request\n')
			dedicated_con_sock.close()
			exit()
			# check third arg in first line of message
		if 'HTTP/' not in client_message_array[2]:
			dedicated_con_sock.send('HTTP/1.0 400 Bad Request\n')
			dedicated_con_sock.close()
			exit()

		#if the requested URL contains 'https://' etc, remove it
		if 'http://' in  client_requested_URL:
			client_requested_host = client_requested_URL.replace('http://', '')
		elif 'https://' in client_requested_URL:
			client_requested_host = client_requested_URL.replace('https://', '')
		else:
			client_requested_host = client_requested_URL

		#start_host = client_requested_host.find('www.')
		start_host = 0

		# if the given URL goes beyond the host name i.e. contains a '/'
		if '/' in client_requested_host:
			end_host = client_requested_host.find('/', start_host)
			# grab the part of the URL after the host name
			index_in = client_requested_host[end_host:len(client_requested_host)]
			client_requested_host = client_requested_host[start_host:end_host]
		# else if the URL ends with .com or .edu, etc...
		else:
			client_requested_host = client_requested_host[start_host:len(client_requested_URL)]

		#	if so, break
		valid_client_message = True
	elif client_message_array[0] =='HEAD' or client_message_array[0] =='POST' or client_message_array[0] =='PUT' or client_message_array[0] =='DELETE' or client_message_array[0] =='TRACE' or client_message_array[0] =='OPTIONS' or client_message_array[0] =='PATCH':
		dedicated_con_sock.send('HTTP/1.0 501 Not Implemented\n')		#	TODO:	there needs to be more to this message...
		dedicated_con_sock.close()
	else:
		dedicated_con_sock.send('HTTP/1.0 400 Bad Request\n')	#	TODO: for now we will stick with this
															#			however, this is probably not the correct format of message 
															#			they are looking for..
		dedicated_con_sock.close()
#	TODO: now that we have the message sent by the client, we need to pass it on to the server,
#out_socket.connect((client_message_array[1], server_port))
out_sock.connect((client_requested_host, 80))						#	TODO:	we need to actually parse the host name and put it here....

# make the string to send to the server
server_request = 'GET ' + index_in + " " + client_message_array[2] + '\nHost: ' + client_requested_host + '\nConection: Close'

out_sock.send(server_request)
server_response = out_sock.recv(1024)	

print 'server response: ', server_response

dedicated_con_sock.send(server_response)

dedicated_con_sock.close()
out_sock.close()
#client_sock.shutdown(SHUT_RDWR)
client_sock.close()
exit(0)



