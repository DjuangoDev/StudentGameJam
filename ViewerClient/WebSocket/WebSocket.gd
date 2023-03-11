extends Node2D

# The URL we will connect to
@export 
var websocket_url = "ws://localhost:12345"

# Our WebSocketClient instance
var _client = WebSocketPeer.new()
var _client_id := 0

# Message Types
const ID := 0
const CONNECTING := 0
const CONNECTED := 1
const OKMES = "200OK"
var int_state = CONNECTING

func _ready():
	randomize()
	# Initiate connection to the given URL.
	var err = _client.connect_to_url(websocket_url)
	_client_id = randi_range(10000,10000000)
	if err != OK:
		print("Unable to connect")
		set_process(false)

func _send_message(socket, message_type, message):
	if message_type == ID:
		socket.send_text("ID MC "+message)

func _process(delta):
	_client.poll()
	var state = _client.get_ready_state()
	if state == WebSocketPeer.STATE_OPEN:
		if int_state == CONNECTING:
			while _client.get_available_packet_count():
				var message = _client.get_packet().get_string_from_utf8()
				print(message)
				if message == "START":
					_send_message(_client, ID, str(_client_id))
				elif message == OKMES:
					int_state = CONNECTED
					print("OK")
		elif int_state == CONNECTED:
			while _client.get_available_packet_count():
				var message = _client.get_packet().get_string_from_utf8()
				print(message)
	elif state == WebSocketPeer.STATE_CLOSING:
		# Keep polling to achieve proper close.
		pass
	elif state == WebSocketPeer.STATE_CLOSED:
		var code = _client.get_close_code()
		var reason = _client.get_close_reason()
		print("WebSocket closed with code: %d, reason %s. Clean: %s" % [code, reason, code != -1])
		set_process(false) # Stop processing.

