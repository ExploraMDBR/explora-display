from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from ._utils import (get_ip, get_comm_json, dump_to_console, 
                     ConnectionManager, add_static_dir,
                     app, ws_manager, STATIC_DIR)

PORT = 8080
HOST = "0.0.0.0"

@app.websocket("/")
async def _websocket_endpoint(websocket: WebSocket):
	await ws_manager.connect(websocket)
	client_id = websocket.scope["client"]
	try:
		while True:
			data = await websocket.receive_text()
			await ws_manager.receive_callback(client_id, websocket, data)
			await ws_manager.broadcast(f"Client #{client_id} sent message: {data}")
	except WebSocketDisconnect:
		ws_manager.disconnect(websocket)
		await ws_manager.broadcast(f"Client #{client_id} disconnected")

@app.get("/status")
async def _status():
	return {"status": "running"}

def on_startup(_app):
	pass

def on_end(_app):
	pass

@asynccontextmanager
async def _lifespan(app: FastAPI):
	on_startup(app)
	yield
	on_end(app)

app.router.lifespan_context = _lifespan

def main(_host = HOST, _port=PORT, _static_dir=("/", STATIC_DIR), loop=None):
	import uvicorn
	add_static_dir(*_static_dir)
	module_str = __name__ if __name__ != "__main__" else "explora.display.display_server"
	if not loop:
		uvicorn.run(app="{}:app".format(module_str), port=_port, 
			host=_host)
	else:
		config = uvicorn.Config(app=app, port=_port, 
								host=_host, loop=loop)
		server = uvicorn.Server(config)
		loop.run_until_complete(server.serve())