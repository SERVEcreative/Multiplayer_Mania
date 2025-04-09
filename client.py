import pygame
import socketio
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Multiplayer Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Server connection settings
SERVER_URL = 'http://localhost:5000'  # Change this to the server's IP address

# Initialize Socket.IO client
sio = socketio.Client(reconnection=True, reconnection_attempts=5, reconnection_delay=1)

# Player state
players = {}
player_pos = {'x': 100, 'y': 100}
player_speed = 5

@sio.event
def connect():
    print('Connected to server')
    # Send initial position
    sio.emit('player_move', player_pos)

@sio.event
def connect_error(data):
    print(f"Connection error: {data}")

@sio.event
def disconnect():
    print('Disconnected from server')
    # Try to reconnect
    try:
        sio.connect(SERVER_URL)
    except:
        print("Could not reconnect to server")

@sio.event
def game_state(data):
    global players
    players = data['players']

@sio.event
def player_joined(data):
    global players
    players = data['players']

@sio.event
def player_left(data):
    global players
    players = data['players']

def main():
    print(f"Connecting to server at {SERVER_URL}")
    print("To connect to a different server, change the SERVER_URL in the code")
    try:
        sio.connect(SERVER_URL)
    except Exception as e:
        print(f"Could not connect to server: {e}")
        sys.exit(1)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos['x'] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos['x'] += player_speed
        if keys[pygame.K_UP]:
            player_pos['y'] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos['y'] += player_speed

        # Keep player within screen bounds
        player_pos['x'] = max(0, min(player_pos['x'], WINDOW_SIZE[0]))
        player_pos['y'] = max(0, min(player_pos['y'], WINDOW_SIZE[1]))

        # Send position to server
        try:
            sio.emit('player_move', player_pos)
        except:
            print("Lost connection to server")
            running = False

        # Draw everything
        screen.fill(WHITE)
        
        # Draw all players
        for player_id, player_data in players.items():
            pygame.draw.circle(screen, player_data.get('color', (255, 0, 0)),
                             (int(player_data['x']), int(player_data['y'])), 20)

        pygame.display.flip()
        clock.tick(60)

    sio.disconnect()
    pygame.quit()

if __name__ == '__main__':
    main() 