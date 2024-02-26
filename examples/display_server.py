from explora.display import display_server
import asyncio


# Create an event and set it when the first Ws client is connected
ready = asyncio.Event()
display_server.ws_manager.connected_callback = lambda w: ready.set()

states = ["ST1", "ST2"]

async def change_states():
	"""This task will change periodically the state of the frontend"""
	try:
		await ready.wait() # wait here for the first client to be connected
		print("Init Websocket task")
		current_state = 0
		while 1:
			# Send to all connected clients the new state
			await display_server.ws_manager.broadcast("sent from cli WS server", states[current_state])
			current_state = (current_state + 1) % len(states) 
			await asyncio.sleep(2)
   
	except Exception as e:
		print("WS task error:", e)

# Get the current event loop
loop = asyncio.new_event_loop()
# Add a task to the event loop
task = loop.create_task(change_states())
# Set a handler on server to cancel the task in case it's still pending
display_server.on_end = lambda app: task.cancel() 

try:
	# Run the display server, passing the current event loop
	# This allows to use custom defined tasks
    display_server.main(loop=loop)

except asyncio.CancelledError:
	pass



