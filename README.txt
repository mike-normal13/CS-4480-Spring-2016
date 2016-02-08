README:

All you have to do to run the assignment is use the command:
	“python proxy2.py [port#]”
	Example: $ python proxy2.py 1234

There are two .py files in the tarball. proxy2.py is the one you should run for this assingment.

The port number given by the user is the port the proxy listens on for the client.
I decided to have the proxy send the message to the server on port 80 in all cases.

Also I took the assignment literally when it said that all client request must be in absolute URI form.
If client requests are not in absolute URI form, the proxy sends a 400 message to the client and exits.

As per the assignment, I am having the proxy send back 400 to the client if the client fails to supply an absolute URL.

Unless I fix it by the deadline, my proxy will send back 400 to client if the client supplies and entity body in its message.

The proxy should work if only the first line(the GET line) of the message is sent, as long as there are two '\r\n'.

The proxy will send 400 to client if the client does not supply two '\r\n\r\n at the end of the message regardless.

I tried doing this without multithreads, and took the professors recommendation is class to use the select method.

I found this example online and based my solution off of it:

	http://ilab.cs.byu.edu/python/select/echoserver.html

I could only get it to work under very limited circumstances.
The biggest problem is that calls to the recv() method are hanging, and refusing to return.
You can connect multiple telnet clients to my proxy, 
	but the proxy only works if you send the GET request from the client that was most recently connected.
If you connect client 1 and then connect client 2, and then send a GET request via client one,
	the call to recv() will hang.

