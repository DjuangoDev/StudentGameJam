#!/usr/bin/env python
from websocket import create_connection

ID = 0
ACT = 1
OK = "200OK"

def send_message(socket, message_type, message):
    if message_type == ID:
        socket.send("ID GC " + message)
    elif message_type == ACT:
        socket.send("ACT GC " + message)


def recv_response(socket):
    message = socket.recv()
    if message != OK:
        return [False,message]
    else:
        return [True,message]

# Connection
ws = create_connection("ws://localhost:12345")
message = ws.recv()
print(message)

# Send client id to server
resp = False
while resp == False:
    client_id = input("Introduce the client ID:\n")
    send_message(ws, ID, client_id)
    [resp,message] = recv_response(ws)
    if resp == False:
	    print("Client ID not valid\n" + message)

# Send RIGHT to server
while True:
    message = input("Message to send:\n")
    send_message(ws, ACT, message)

resp = False
while resp == False:
    send_message(ws, ACT, "RIGHT")
    [resp,message] = recv_response(ws)
    if resp == False:
	    print("Not recognized action\n" + message)

ws.close()