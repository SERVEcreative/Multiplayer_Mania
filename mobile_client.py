from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
import socketio
import json

# Server connection settings
SERVER_URL = 'http://localhost:5000'  # Change this to the server's IP address

# Initialize Socket.IO client
sio = socketio.Client(reconnection=True, reconnection_attempts=5, reconnection_delay=1)

# Game state
players = {}
player_pos = {'x': 100, 'y': 100}
player_speed = 5

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_controls()
        self.connect_to_server()
        
    def setup_controls(self):
        # Create directional buttons
        button_size = (100, 100)
        
        # Up button
        self.up_button = Button(
            text='↑',
            size=button_size,
            pos=(Window.width/2 - 50, Window.height - 150)
        )
        self.up_button.bind(on_press=self.move_up, on_release=self.stop_vertical)
        
        # Down button
        self.down_button = Button(
            text='↓',
            size=button_size,
            pos=(Window.width/2 - 50, 50)
        )
        self.down_button.bind(on_press=self.move_down, on_release=self.stop_vertical)
        
        # Left button
        self.left_button = Button(
            text='←',
            size=button_size,
            pos=(50, Window.height/2 - 50)
        )
        self.left_button.bind(on_press=self.move_left, on_release=self.stop_horizontal)
        
        # Right button
        self.right_button = Button(
            text='→',
            size=button_size,
            pos=(Window.width - 150, Window.height/2 - 50)
        )
        self.right_button.bind(on_press=self.move_right, on_release=self.stop_horizontal)
        
        # Add buttons to widget
        self.add_widget(self.up_button)
        self.add_widget(self.down_button)
        self.add_widget(self.left_button)
        self.add_widget(self.right_button)
        
        # Status label
        self.status_label = Label(
            text='Connecting...',
            pos=(10, Window.height - 30),
            size=(Window.width - 20, 30)
        )
        self.add_widget(self.status_label)
        
        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        
        # Start update loop
        Clock.schedule_interval(self.update, 1.0/60.0)
    
    def connect_to_server(self):
        try:
            sio.connect(SERVER_URL)
            self.status_label.text = 'Connected to server'
        except Exception as e:
            self.status_label.text = f'Connection failed: {str(e)}'
    
    def move_up(self, instance):
        self.moving_up = True
    
    def move_down(self, instance):
        self.moving_down = True
    
    def move_left(self, instance):
        self.moving_left = True
    
    def move_right(self, instance):
        self.moving_right = True
    
    def stop_vertical(self, instance):
        self.moving_up = False
        self.moving_down = False
    
    def stop_horizontal(self, instance):
        self.moving_left = False
        self.moving_right = False
    
    def update(self, dt):
        # Update player position based on movement flags
        if self.moving_up:
            player_pos['y'] -= player_speed
        if self.moving_down:
            player_pos['y'] += player_speed
        if self.moving_left:
            player_pos['x'] -= player_speed
        if self.moving_right:
            player_pos['x'] += player_speed
        
        # Keep player within screen bounds
        player_pos['x'] = max(0, min(player_pos['x'], Window.width))
        player_pos['y'] = max(0, min(player_pos['y'], Window.height))
        
        # Send position to server
        try:
            sio.emit('player_move', player_pos)
        except:
            self.status_label.text = 'Lost connection to server'
        
        # Redraw
        self.canvas.clear()
        with self.canvas:
            # Draw all players
            for player_id, player_data in players.items():
                Color(1, 0, 0)  # Red color
                Ellipse(pos=(player_data['x'] - 20, player_data['y'] - 20), size=(40, 40))

# Socket.IO event handlers
@sio.event
def connect():
    print('Connected to server')
    sio.emit('player_move', player_pos)

@sio.event
def connect_error(data):
    print(f"Connection error: {data}")

@sio.event
def disconnect():
    print('Disconnected from server')
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

class MultiplayerGameApp(App):
    def build(self):
        return GameWidget()
    
    def on_stop(self):
        sio.disconnect()

if __name__ == '__main__':
    MultiplayerGameApp().run() 