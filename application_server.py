from socket import *
from random import *
import json

# Listening port for the server
serverPort = 8080

# Create the server socket object
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the server socket to the port
serverSocket.bind(('', serverPort))

# Start listening for new connections
serverSocket.listen(1)

print('The server is ready to receive messages')

# Records what numbers have been selected
gameBoard = list()

# JSON representation of naughts and crosses board
jsonStructure = ["null", "null", "null", "null", "null", "null", "null", "null", "null"]

while 1:
    # Accept a connection from a client
    connectionSocket, addr = serverSocket.accept()
    # Retrieve the message sent by the client
    request = connectionSocket.recv(1024).decode('UTF-8')

    # Slices player choose out of API request
    clientSelection = int(request.split()[1].split('/')[1])

    # Checks whether the clients choose is valid
    if jsonStructure[clientSelection - 1] == "null":
        jsonStructure[clientSelection - 1] = "X"
        while 1:
            serverSelection = randint(0, 8)
            if jsonStructure[serverSelection] == "null":
                jsonStructure[serverSelection] = "O"
                break
        
    response = json.dumps(jsonStructure)
    # Send HTTP response back to the client
    connectionSocket.send(response.encode())
    # Close the connection
    connectionSocket.close()
