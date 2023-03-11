#!/usr/bin/env python

# import asyncio
# import websockets

# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(message)

# async def main():
#     async with websockets.serve(echo, "localhost", 12345):
#         await asyncio.Future()  # run forever

# asyncio.run(main())

from websocket_server import WebsocketServer

OK = "200OK"
ERROR = "300ER"


clients = []
connections = {}

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id {0}".format(client['id']))
	server.send_message(client, "START")
	clients.append(client)
	print(clients)

# Called for every client disconnecting
def client_left(client, server):
	print("Client({0}) disconnected".format(client['id']))
	#TODO delete client from clients list and connections

# Called when a client sends a message
def message_received(client, server, message):
	print("message: " + message)
	parts = message.split(' ')
	print(parts)
	if parts[0] == "ID" and parts[1] == "MC":
		client['id'] = parts[2]
		print("Client({0}) said: {1}".format(client['id'], message))
		server.send_message(client, OK)
	elif parts[0] == "ID" and parts[1] == "GC":
		print("ENTRA en ID GC")
		for i,c in enumerate(clients):
			if c['id'] == parts[2]:
				connections[client['id']] = i
				print("Gesture Client({0}) connected to Mobile Client({1})".format(client['id'],parts[2]))
				server.send_message(client, OK)
				break
		server.send_message(client, ERROR)
	elif parts[0] == "ACT" and parts[1] == "GC":
		print(connections)
		connections[client['id']]
		server.send_message(clients[connections[client['id']]],parts[2])
	

PORT=12345
server = WebsocketServer(port = PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()