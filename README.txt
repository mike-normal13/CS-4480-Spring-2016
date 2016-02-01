README:

All you have to do to run the assignment is use the command:
	“python proxy.py [port#]”
	Example: $ python proxy.py 1234

The port number given by the user is the port the proxy listens on for the client.
I decided to have the proxy send the message to the server on port 80 in all cases.

Also I took the assignment literally when it said that all client request must be in absolute URI form.
If client requests are not in absolute URI form, the proxy sends a 400 message to the client and exits.

As per the assignment, I am having the proxy send back 400 to the client if the client fails to supply an absolute URL.

Unless I fix it by the deadline, my proxy will send back 400 to client if the client supplies and entity body in its message.

The proxy should work if only the first line(the GET line) of the message is sent, as long as there are two '\r\n'.

The proxy will send 400 to client if the client does not supply two '\r\n\r\n at the end of the message regardless'