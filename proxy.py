#!/usr/bin/python

import re
import sys
from socket import *

# port members
listen_port = 80
server_port = 80

#	client message storage member
client_message = ''
#	message sent by client parsed to an array
client_message_array = []

# flag indicating a connection has been made between the proxy and the client.
valid_client_message = False

#flag indaicating that the client requested a URL that went past the base page of a 
past_base_page = False

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

# doing this makes it so I don't have to wait 10 seconds or so between runs of the script waiting for this socket to close all the way.
client_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  #http://stackoverflow.com/questions/2765152/what-is-the-correct-way-to-close-a-socket-in-python-2-6

client_sock.bind((client_requested_host, listen_port))
client_sock.listen(1)			#	1 for now...

print 'proxy is waiting for client to connect'

while valid_client_message == False:
	dedicated_con_sock, addr = client_sock.accept()
	client_message = dedicated_con_sock.recv(1024)
	
	new_line_count = client_message.count('\\r\\n')

	#	parse the client message to an array based upon \r\n
	client_message_array = client_message.split("\\r\\n")

		# just in case the client sends the one GET line only, and only has one \r\n on the end of it....
	try:
		# if the message was formated correctly there should be an '' and '\r\n' in the last two positions, remove them
		client_message_array.remove('')
		client_message_array.remove('\r\n')
	except ValueError:
		dedicated_con_sock.send('HTTP/1.0 400 Bad Request\n')
		dedicated_con_sock.close()
		exit()

	# at this point the number of '\r\n' suppiled by the client in the message should be one more 
	#	than the number of items in the client_message_array
	#	TODO:	this check does not accout for an entity Body, if the user suplies an entity body, this block will terminate.
	if new_line_count != len(client_message_array) + 1:
		dedicated_con_sock.send('HTTP/1.0 400 Bad Request\n')
		dedicated_con_sock.close()
		exit()

	#	some checks for proper formating
	#	check that the client sent a GET request
	if client_message_array[0].startswith('GET'):

		# grab the first line and split it by white space
		get_line_array = client_message_array[0].split()

		# get URL
		client_requested_URL = get_line_array[1]

		# a few checks
			#	check for absoulute URI
		if (client_requested_URL.startswith('http://')) or (client_requested_URL.startswith('https://')):
			s = 2				# PYTHON!!!
		else:
			dedicated_con_sock.send('HTTP/1.0 400 Bad Request\n')
			dedicated_con_sock.close()
			exit()
			# check third arg in first line of message
		if 'HTTP/' not in get_line_array[2] and (get_line_array[2].endswith('\\r\\n') == False):
			dedicated_con_sock.send('HTTP/1.0 400 Bad Request\n')
			dedicated_con_sock.close()
			exit()

		#	within the client message array,
		#		if a word ends with \n then the next word must end with :
		i = 1
		while i < len(client_message_array) - 1:

			#split each line into arrays delimited by ' '
			header_line_array = client_message_array[i].split()

			# check for header line startign with cap letter
			if header_line_array[0][0].isupper() == False:
				dedicated_con_sock.send('HTTP/1.0 400 Bad Request\n')
				dedicated_con_sock.close()
				exit()

			# check for header line first word ending with ':'
			if header_line_array[0].endswith(':') == False:
				dedicated_con_sock.send('HTTP/1.0 400 Bad Request\n')
				dedicated_con_sock.close()
				exit()

			i = i + 1

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

			past_base_page = True
		# else if the URL ends with .com or .edu, etc...
		else:
			client_requested_host = client_requested_host[start_host:len(client_requested_URL)]

		#	if so, break
		valid_client_message = True
	elif client_message_array[0] =='HEAD' or client_message_array[0] =='POST' or client_message_array[0] =='PUT' or client_message_array[0] =='DELETE' or client_message_array[0] =='TRACE' or client_message_array[0] =='OPTIONS' or client_message_array[0] =='PATCH':
		dedicated_con_sock.send('HTTP/1.0 501 Not Implemented\n')		#	TODO:	there needs to be more to this message...
		dedicated_con_sock.close()
	else:
		dedicated_con_sock.send('HTTP/1.0 400 Bad Request\n')
		dedicated_con_sock.close()

out_sock.connect((client_requested_host, 80))						

# if the user supplied a url that goes past .com etc
if past_base_page == True:
	server_request = 'GET ' + index_in + ' HTTP/1.0\r\n'

	for line in range(1,len(client_message_array) - 1):
		server_request = server_request + client_message_array[line] + '\r\n' 
else:
	server_request = 'GET / HTTP/1.0\r\n'

	for line in range(1,len(client_message_array) - 1):
		server_request = server_request + client_message_array[line] + '\r\n' 

# one last new line
server_request = server_request + '\r\n'
#TODO: is this enough? should we provide any other hearders??

print 'server_request:\n', server_request

out_sock.send(server_request)
server_response = out_sock.recv(1024)	

print 'server response: ', server_response

dedicated_con_sock.send(server_response)

dedicated_con_sock.close()
out_sock.close()
client_sock.close()
exit(0)
