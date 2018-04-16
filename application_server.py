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

# Prevents the client from exceeding the board limit of 9
state = 0

# JSON representation of naughts and crosses board
class Game:
    boardLayout = []
    def __init__(self):
        self.boardLayout = ["", "", "", "", "", "", "", "", ""]
        self.state = 0
    def getBoardIndex(self, i):
        return self.boardLayout[i]
    def setBoardIdex(self, i, val):
        self.boardLayout[i] = val

# Computes whether game has been won
def GameEngine(jStructure):
    # Client Logic
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

myGame = Game()
while 1:
    # Accept a connection from a client
    connectionSocket, addr = serverSocket.accept()
    # Retrieve the message sent by the client
    request = connectionSocket.recv(1024).decode('UTF-8')

    # Slices player choose out of API request
    clientSelection = request.split()[1].split('/')[1]

    # Checks whether submit or reset button has been pressed
    if clientSelection == "restart":
        myGame = Game()
        response = json.dumps(myGame.__dict__)
    else:
        clientSelection = int(clientSelection) - 1
        # Checks whether the clients choose is valid
        if myGame.getBoardIndex(clientSelection) == "":
            myGame.setBoardIdex(clientSelection, "X")
            if state != 9:
                # Chooses a random square in on the board
                while 1:
                    serverSelection = randint(0, 8)
                    if myGame.boardLayout[serverSelection] == "" and serverSelection != clientSelection:
                        myGame.setBoardIdex(serverSelection, "O")
                        response = json.dumps(myGame.__dict__)
                        # Checks whether client or server has wn
                        winningPlayer = GameEngine(myGame.boardLayout)
                        # If client wins
                        if winningPlayer == "X":
                            myGame.state = "X"
                            response = json.dumps(myGame.__dict__)
                        # If server wins
                        elif winningPlayer == "O":
                            myGame.state = "O"
                            response = json.dumps(myGame.__dict__)
                        break
            else:
                myGame.state = "D"
                response = json.dumps(myGame.__dict__)
        # Enter only if clients sends invalid selection
        else:
            myGame.state = "Error"
            response = json.dumps(myGame.__dict__)




    # Send HTTP response back to the client
    connectionSocket.send(response.encode())
    state = state + 1


    # Close the connection
    connectionSocket.close()
