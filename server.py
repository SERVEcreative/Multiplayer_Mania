import socketio
import eventlet
from aiohttp import web
import socket

# Create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')
app = socketio.WSGIApp(sio)

# Store connected players
players = {}

@sio.event
def connect(sid, environ):
    print(f'Player connected: {sid}')
    players[sid] = {'x': 100, 'y': 100, 'color': (255, 0, 0)}
    sio.emit('player_joined', {'players': players}, skip_sid=sid)
    sio.emit('game_state', {'players': players}, room=sid)

@sio.event
def disconnect(sid):
    print(f'Player disconnected: {sid}')
    if sid in players:
        del players[sid]
    sio.emit('player_left', {'players': players})

@sio.event
def player_move(sid, data):
    if sid in players:
        players[sid]['x'] = data['x']
        players[sid]['y'] = data['y']
        sio.emit('game_state', {'players': players})

if __name__ == '__main__':
    # Get local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print('Starting server...')
    print(f'Server IP: {local_ip}')
    print('To connect from other devices, use this IP address in the client')
    print('Press Ctrl+C to stop the server')
    
    # Use eventlet's monkey patching
    eventlet.monkey_patch()
    # Start the server on all network interfaces
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app) 