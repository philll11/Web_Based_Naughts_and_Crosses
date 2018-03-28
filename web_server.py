from socket import *
import os

# Listening port for the server
serverPort = 8000

# Create the server socket object
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the server socket to the port
serverSocket.bind(('', serverPort))

# Start listening for new connections
serverSocket.listen(1)

print('The server is ready to receive messages')

while 1:
    # Accept a connection from a client
    connectionSocket, addr = serverSocket.accept()
    # Retrieve the message sent by the client
    request = connectionSocket.recv(1024).decode('UTF-8')
    print(request)
    # Unsure if this is the best way to prevent while loop from crashing
    if request != "":
        if request.split()[0] == "GET":
            print(request.split()[0])
            # Extract the  GET requested resource from the path
            getResource = request.split()[1].split("/")[1]

            if os.path.isfile(getResource):
                response = b"HTTP/1,1 200 OK\n\n"
                print("File exists")
                with open(getResource, 'rb') as f:
                    response = response + f.read()
                    connectionSocket.send(response)
            else:
                print("File does not exist")
                response = "HTTP 404 not found\r\n"
                connectionSocket.send(response.encode())

        elif request.split()[0] == "POST":
            # Extract the POST requested resource from the path
            postResource = request.split()[1].split("/")[1]
            print(postResource)

    # Close the connection
    connectionSocket.close()