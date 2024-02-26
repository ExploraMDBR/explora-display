import os
import json
import asyncio
from sys import stdout
from random import choice

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

_dir_path = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(_dir_path, "public")

app = FastAPI()

def get_ip():
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except Exception:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP


def get_comm_json(msg, state="system", count=0, user='no-user', extra=''):
	return json.dumps({
		"state": state,
		"msg": msg,
		"count": count,
		"user":user,
		"extra":extra
		})

def dump_to_console(msg, xtra=None):
	print("[WS] {} | xtra arg: {}".format(msg, xtra))
	stdout.flush()
 

class ConnectionManager:
	def __init__(self):
		self.active_connections: list[WebSocket] = []

	async def connect(self, websocket: WebSocket):
		await websocket.accept()
		self.active_connections.append(websocket)
		self.connected_callback(websocket)

	def disconnect(self, websocket: WebSocket):
		self.active_connections.remove(websocket)
		self.disconnected_callback(websocket)

	async def send_personal_message(self, websocket, message, state="system", count=0, user='no-user', extra=''):
		await websocket.send_text(get_comm_json(message, state, count, user, extra))

	async def broadcast(self, message: str, state="system", count=0, user='no-user', extra=''):
		for connection in self.active_connections:
			await connection.send_text(get_comm_json(message, state, count, user, extra))
			
	async def receive_callback(self, client_id, websocket, data):
		await ws_manager.send_personal_message(websocket,  f"Echo: {data}")

	def connected_callback(self, websocket):
		print("[WS] Connected WS client: {}, total: {}".format(websocket.scope["client"], len(self.active_connections)))
	
	def disconnected_callback(self, websocket):
		print("[WS] Disconnected WS client: {}, total: {}".format(websocket.scope["client"], len(self.active_connections)))

ws_manager = ConnectionManager()

def add_static_dir(path='/', directory=STATIC_DIR):
	print("Adding static dir ({}): {}".format(path, directory))
	app.mount(path, StaticFiles(directory=directory, html=True), name="public")


animals = [
"Elefante",
"Cane",
"Serpente",
"Giraffa",
"Scimmia",
"Uccello",
"Aquila",
"Ragno",
"Tigre",
"Leopardo",
"Orso",
"Talpa",
"Scoiattolo",
"Trilobite",
"Formica"
]

colori = [
"blue",
"rosa",
"rosso",
"verde",
"giallo",
"marrone",
"dorato",
"argentato",
"azzurro",
"indago",
"viola",
"trasparente",
"grigio"
]


def generate_username():
    return "{} {}".format(choice(animals), choice(colori))