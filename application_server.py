from socket import *

# Listening port for the server
serverPort = 8080

# Create the server socket object
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the server socket to the port
serverSocket.bind('', serverPort)

# Start listening for new connections
serverSocket.listen(1)

print('The server is ready to receive messages')

while 1:
    # Accept a connection from a client
    connectionSocket, addr = serverSocket.accept()
    # Retrieve the message sent by the client
    request = connectionSocket.recv(1024)
    # Create HTTP response
    response = "HTTP /1.1 200 OK\n\nWelcome to my home page"
    # Send HTTP response back to the client
    connectionSocket.send(response.encode())
    # Close the connection
    connectionSocket.close()