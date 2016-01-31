#!/usr/bin/python

#	TODO:	I am assuming that the port the proxy is listening on is not the port it will be sending to the server....
#	TODO:	Before we worry about parsing the message from the client,
#				Lets just assume correct GET messages 
#				and see if we can't get the whole thing to work between the client -> proxy -> server -> proxy -> client
#	TODO:	are we dealing with persistent TCP conections here?
# 	TODO: more stringent port input validation would be nice....
#	TODO:	1:	Start the thing via command line
#			2:	Have socket listen in designated port
#			3:	When the client makes a request, have the proxy parse it
#			4:	have the proxy send the appropriate error code back if the request is ill formed
#					Send back error code 501 if GET is not sent
#					Send back error code 400 for all other cases
#			5:		
#			6:
#		
#			once the proxy is ready to open a connection to the url requested by the client

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

server_response = ''

# Get port
if len(sys.argv) != 1:
	listen_port = sys.argv[1]

# convert port to integer for good measure
listen_port = int(listen_port)

#	socket the proxy will be using to communicate with the client, this socket will be the doorway knocked on first.
client_sock = socket(AF_INET, SOCK_STREAM)
#	Socket the proxy will use to comunicate with next node in the network
out_sock = socket(AF_INET, SOCK_STREAM)

client_sock.bind((client_requested_host, listen_port))
client_sock.listen(1)			#	1 for now...

print 'proxy is waiting for client to connect'

while valid_client_message == False:
	dedicated_con_sock, addr = client_sock.accept()
	client_message = dedicated_con_sock.recv(1024)
	
	#	parse the client message to an array
	client_message_array = client_message.split(' ')

	print client_message
	#	check that the client sent a GET request
	if client_message_array[0] == 'GET':
		# TODO:	do further parsing to determine if the message from the client is valid

		#	TODO:	do a basic parse to get the URL from the client
		#	Example of simple get message:
		#	GET /hello.htm HTTP/1.1
		#	User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
		#	Host: www.tutorialspoint.com
		#	Accept-Language: en-us
		#	Accept-Encoding: gzip, deflate
		#	Connection: Keep-Alive

		# get URL
		client_requested_URL = client_message_array[1]

		#if the requested URL contains 'https://' etc, remove it
		if 'http://' in  client_requested_URL:
			client_requested_host = client_requested_URL.replace('http://', '')
		elif 'https://' in client_requested_URL:
			client_requested_host = client_requested_URL.replace('https://', '')
		else:
			client_requested_host = client_requested_URL

		print 'client_requested_host after removing http(s)://: ', client_requested_host

		start_host = client_requested_host.find('www')

		# if the given URL goes beyond the host name i.e. contains a '/'
		if '/' in client_requested_host:
			print 'there is a / in the url'
			end_host = client_requested_host.find('/', start_host)
			client_requested_host = client_requested_host[start_host:end_host]
		# else if the URL ends with .com or .edu, etc...
		else:
			print 'there is no / in the URL'
			client_requested_host = client_requested_host[start_host:len(client_requested_URL)]

		print 'client_requested_host: ', client_requested_host
		
		#	TODO:	verify that the host given by client is valid URI sybtax

		#	if so, break
		valid_client_message = True
	elif client_message_array[0] =='HEAD' or client_message_array[0] =='POST' or client_message_array[0] =='PUT' or client_message_array[0] =='DELETE' or client_message_array[0] =='TRACE' or client_message_array[0] =='OPTIONS' or client_message_array[0] =='PATCH':
		dedicated_con_sock.send('HTTP/1.1 501 Not Implemented')		#	TODO:	there needs to be more to this message...
	else:
		dedicated_con_sock.send('HTTP/1.1 400 Bad Request')	#	TODO: for now we will stick with this
															#			however, this is probably not the correct format of message 
															#			they are looking for..
#	TODO: now that we have the message sent by the client, we need to pass it on to the server,
#out_socket.connect((client_message_array[1], server_port))
out_sock.connect((client_requested_host, 80))						#	TODO:	we need to actually parse the host name and put it here....

# make the string to send to the server
server_request = 'GET / ' + client_message_array[2] + '\nHost: ' + client_requested_host + '\nConection: Close'

out_sock.send(server_request)
server_response = out_sock.recv(1024)	

print 'server response: ', server_response

dedicated_con_sock.send(server_response)



