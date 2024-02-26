from explora.display import display_server
import asyncio
import sys
import select
import websockets

ready = asyncio.Event()

display_server.ws_manager.connected_callback = lambda w: ready.set()

async def async_read_stdin(timeout)->str:
	loop = asyncio.get_event_loop()
	rfds, wfds, efds = select.select([sys.stdin,],[],[],timeout)
	if rfds:
		return (await loop.run_in_executor(None, sys.stdin.readline))
	return None

def prompt():
	print("ws> ", end="")
	sys.stdout.flush()

async def repl():
	try:
		await ready.wait()
		print("Init Websocket REPL, type a state string and press ENTER to send it to the clients")
		prompt()
		while 1:
			state = await async_read_stdin(2)
			if state and state.lower().startswith("quit"):
				print("Websocket REPL ended, press CTRL + C to end server")
				return
			if state:
				await display_server.ws_manager.broadcast("sent from cli WS server", state)
				prompt()
    
	except Exception as e:
		print("REPL error:", e)

loop = asyncio.new_event_loop()
task = loop.create_task(repl())

try:
    display_server.main(loop=loop)

except asyncio.CancelledError:
    pass



