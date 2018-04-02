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
jsonStructure = ["", "", "", "", "", "", "", "", ""]

def GameEngine(jStructure):
    # Client Logic
    print("GameEngine entered")
    if jStructure[0] == "X" and jStructure[1] == "X" and jStructure[2] == "X":
        return "X"
    elif jStructure[3] == "X" and jStructure[4] == "X" and jStructure[5] == "X":
        return "X"
    elif jStructure[6] == "X" and jStructure[7] == "X" and jStructure[8] == "X":
        return "X"
    elif jStructure[0] == "X" and jStructure[3] == "X" and jStructure[6] == "X":
        return "X"
    elif jStructure[1] == "X" and jStructure[4] == "X" and jStructure[7] == "X":
        return "X"
    elif jStructure[2] == "X" and jStructure[5] == "X" and jStructure[8] == "X":
        return "X"
    elif jStructure[0] == "X" and jStructure[4] == "X" and jStructure[8] == "X":
        return "X"
    elif jStructure[2] == "X" and jStructure[4] == "X" and jStructure[6] == "X":
        return "X"
    # Server Logic
    elif jStructure[0] == "O" and jStructure[1] == "O" and jStructure[2] == "O":
        return "O"
    elif jStructure[3] == "O" and jStructure[4] == "O" and jStructure[5] == "O":
        return "O"
    elif jStructure[6] == "O" and jStructure[7] == "O" and jStructure[8] == "O":
        return "O"
    elif jStructure[0] == "O" and jStructure[3] == "O" and jStructure[6] == "O":
        return "O"
    elif jStructure[1] == "O" and jStructure[4] == "O" and jStructure[7] == "O":
        return "O"
    elif jStructure[2] == "O" and jStructure[5] == "O" and jStructure[8] == "O":
        return "O"
    elif jStructure[0] == "O" and jStructure[4] == "O" and jStructure[8] == "O":
        return "O"
    elif jStructure[2] == "O" and jStructure[4] == "O" and jStructure[6] == "O":
        return "O"
    else:
        return ""

while 1:
    # Accept a connection from a client
    connectionSocket, addr = serverSocket.accept()
    # Retrieve the message sent by the client
    request = connectionSocket.recv(1024).decode('UTF-8')

    # Slices player choose out of API request
    clientSelection = int(request.split()[1].split('/')[1])

    # Checks whether submit or reset button has been pressed
    if clientSelection == 10:
        jsonStructure = ["", "", "", "", "", "", "", "", ""]
        response = json.dumps(jsonStructure)
    else:
        # Checks whether the clients choose is valid
        if jsonStructure[clientSelection - 1] == "":
            jsonStructure[clientSelection - 1] = "X"
            # Chooses a random square in on the board
            while 1:
                serverSelection = randint(0, 8)
                if jsonStructure[serverSelection] == "":
                    jsonStructure[serverSelection] = "O"
                    response = json.dumps(jsonStructure)
                    # The Web_server is throwing error: "Empty reply from application server"
                    # Also when a player wins, the jsonStructure array need to be send as the game.html
                    # still needs to display the clients winning move
                    winningPlayer = GameEngine(jsonStructure)
                    if winningPlayer == "X":
                        response = json.dumps("X")
                    elif winningPlayer == "O":
                        response = json.dumps("O")
                    break
        else:
            response = json.dumps("False")




    # Send HTTP response back to the client
    connectionSocket.send(response.encode())
        


    # Close the connection
    connectionSocket.close()
