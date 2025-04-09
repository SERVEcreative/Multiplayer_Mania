# Multiplayer Game

A real-time multiplayer game where players can move around and see each other in real-time. Built with Python (Socket.IO) for the backend and HTML5 Canvas + JavaScript for the frontend.

## Features

- Real-time multiplayer using Socket.IO
- Works on both desktop and mobile devices
- Simple controls (arrow keys for desktop, touch buttons for mobile)
- Player count display
- Connection status indicator
- Responsive design that works on any screen size

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multiplayer-game.git
cd multiplayer-game
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## How to Run

1. Start the web server:
```bash
python web_server.py
```

2. The server will display its IP address and port. Open this URL in your web browser:
```
http://<server-ip>:<port>
```

## How to Play

### Desktop Controls
- Use arrow keys (↑, ↓, ←, →) to move your player
- Your player is shown in blue
- Other players are shown in red

### Mobile Controls
- Use the on-screen directional buttons
- Works on any mobile device with a web browser

### Playing with Others
1. Make sure all players are on the same network
2. Share the server URL with other players
3. Each player opens the URL in their browser
4. Click "Connect" to join the game

## Project Structure

- `web_server.py` - The main server file that handles Socket.IO connections
- `index.html` - The main HTML file with the game interface
- `game.js` - The JavaScript file containing game logic
- `requirements.txt` - Python package dependencies

## Customization

You can customize various aspects of the game:

1. Player Colors:
   - Edit the `game.js` file to change player colors
   - Current player: `rgba(0, 0, 255, 0.7)` (blue)
   - Other players: `rgba(255, 0, 0, 0.7)` (red)

2. Game Speed:
   - Modify the `playerSpeed` variable in `game.js`
   - Default value is 5

3. Canvas Size:
   - Edit the CSS in `index.html`
   - Default size is 800x600 pixels

4. Server Port:
   - The server automatically finds an available port
   - Default range is 5000-5010

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Socket.IO for real-time communication
- HTML5 Canvas for game rendering
- Python aiohttp for the web server 