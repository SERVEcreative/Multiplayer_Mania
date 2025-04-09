import socketio
import eventlet
from aiohttp import web
import socket
import os

# Create a Socket.IO server with proper CORS and transport settings
sio = socketio.AsyncServer(
    cors_allowed_origins='*',
    async_mode='aiohttp',
    ping_timeout=60,
    ping_interval=25,
    transports=['polling', 'websocket'],
    logger=True,
    engineio_logger=True
)
app = web.Application()
sio.attach(app)

# Store connected players
players = {}

# Serve static files
async def index(request):
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return web.Response(text=f.read(), content_type='text/html')
    except Exception as e:
        print(f"Error reading index.html: {e}")
        return web.Response(text="Error loading game", status=500)

async def game_js(request):
    try:
        with open('game.js', 'r', encoding='utf-8') as f:
            return web.Response(text=f.read(), content_type='application/javascript')
    except Exception as e:
        print(f"Error reading game.js: {e}")
        return web.Response(text="// Error loading game script", status=500)

# Add routes
app.router.add_get('/', index)
app.router.add_get('/game.js', game_js)

@sio.event
async def connect(sid, environ):
    print(f'Player connected: {sid}')
    players[sid] = {'x': 100, 'y': 100, 'color': (255, 0, 0)}
    await sio.emit('player_joined', {'players': players}, skip_sid=sid)
    await sio.emit('game_state', {'players': players}, room=sid)

@sio.event
async def disconnect(sid):
    print(f'Player disconnected: {sid}')
    if sid in players:
        del players[sid]
    await sio.emit('player_left', {'players': players})

@sio.event
async def player_move(sid, data):
    if sid in players:
        players[sid]['x'] = data['x']
        players[sid]['y'] = data['y']
        await sio.emit('game_state', {'players': players})

def find_available_port(start_port=5000, max_port=5010):
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise OSError("No available ports found")

if __name__ == '__main__':
    # Get local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    # Find an available port
    port = find_available_port()
    
    print('Starting web server...')
    print(f'Server IP: {local_ip}')
    print('To connect from other devices, use this URL in a web browser:')
    print(f'http://{local_ip}:{port}')
    print('Press Ctrl+C to stop the server')
    
    # Start the server
    web.run_app(app, host='0.0.0.0', port=port) 