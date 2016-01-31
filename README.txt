README:

All you have to do to run the assignment is use the command:
	“python proxy.py [port #]”
	Example: $ python proxy.py 1234

The port number given by the user is the port the proxy listens on for the client.
I decided to have the proxy send the message to the server on port 80 in all cases.
Also, I followed the example given in the assignment where if the user submits a get request to 
the server like so: 
	GET http://www.google.com HTTP/1.0
Then the message sent to the server will be:	
	GET / HTTP/1.0
	Host: www.google.com