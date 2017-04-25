from aiohttp import web, WSMsgType
import pyredis
import json
import service_controller

# aiohttp web app
app = web.Application()

try:
	# Redis client
	redis_client = pyredis.Client(host="localhost")
	#  Set UI enabled by default
	if not redis_client.get('enable_ui'):
		redis_client.set('enable_ui', True)
except Exception:
	print("Redis connection failed")

# Array of client websocket connections
clients = []
# Service to control
service = "ssh"

def is_ui_enabled():
	return redis_client.get('enable_ui') == b"True";

def set_ui_enabled(state):
	redis_client.set('enable_ui', state)

async def get_handler(request):
	return web.Response(body=open('static/index.html').read(), content_type="text/html")

async def websocket_handler(request):
	ws = web.WebSocketResponse()
	await ws.prepare(request)

	if ws not in clients:
		clients.append(ws)

	update_client(ws, service_controller.check_service_status(service), is_ui_enabled())

	async for msg in ws:
		if msg.type == WSMsgType.TEXT:
			try:
				handle_action(msg.data)
			except Exception:
				print(msg)

	print("Client removed")
	clients.remove(ws)

	return ws;

def handle_action(data):
	act = json.loads(data)['action']
	if act == "start":
		ret = service_controller.start_service(service)
		if ret: print(service + " started")
	elif act == "stop":
		ret = service_controller.stop_service(service)
		if ret: print(service + " stopped")
	elif act == "restart":
		ret = service_controller.restart_service(service)
		if ret: print(service + " restarted")
	elif act == "enableui":
		redis_client.set('enable_ui', True)
		print("enableui")
	elif act == "disableui":
		redis_client.set('enable_ui', False)
		print("disableui")

	send_updates(service_controller.check_service_status(service), is_ui_enabled())

def send_updates(status, enableui):
	for client in clients:
		update_client(client, status, enableui)

def update_client(client, status, enableui):
	msg = {'type':'status','active':status,'enable_ui':enableui}
	client.send_str(json.dumps(msg))

app.router.add_route('GET', '/ws', websocket_handler)
app.router.add_route('GET', '/', get_handler)
app.router.add_static('/', 'static/')

web.run_app(app)