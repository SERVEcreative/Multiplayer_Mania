// Game variables
const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const statusElement = document.getElementById('status');
const playerCountElement = document.getElementById('player-count');
const connectionForm = document.getElementById('connection-form');
const serverUrlInput = document.getElementById('server-url');
const connectButton = document.getElementById('connect-btn');

// Set canvas size
function resizeCanvas() {
    const container = document.getElementById('game-container');
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
}

// Call resize on load and when window is resized
window.addEventListener('load', resizeCanvas);
window.addEventListener('resize', resizeCanvas);

// Game state
let socket;
let players = {};
let myId = null;
let playerPos = { x: 100, y: 100 };
const playerSpeed = 5;
let isConnected = false;

// Movement state
const keys = {
    up: false,
    down: false,
    left: false,
    right: false
};

// Connect to server
function connectToServer() {
    const serverUrl = serverUrlInput.value;
    
    if (socket) {
        socket.disconnect();
    }
    
    statusElement.textContent = 'Connecting...';
    
    // Updated Socket.IO configuration
    socket = io(serverUrl, {
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000,
        transports: ['polling', 'websocket'], // Try polling first, then upgrade to websocket
        upgrade: true,
        timeout: 20000,
        forceNew: true,
        path: '/socket.io/',
        withCredentials: false
    });
    
    setupSocketEvents();
}

// Setup socket event handlers
function setupSocketEvents() {
    socket.on('connect', () => {
        console.log('Connected to server');
        isConnected = true;
        myId = socket.id;
        statusElement.textContent = 'Connected';
        connectionForm.style.display = 'none';
        
        // Send initial position
        socket.emit('player_move', playerPos);
    });
    
    socket.on('disconnect', (reason) => {
        console.log('Disconnected:', reason);
        isConnected = false;
        statusElement.textContent = 'Disconnected';
        connectionForm.style.display = 'block';
    });
    
    socket.on('connect_error', (error) => {
        console.error('Connection error:', error);
        statusElement.textContent = `Connection error: ${error.message}`;
        connectionForm.style.display = 'block';
    });
    
    socket.on('error', (error) => {
        console.error('Socket error:', error);
        statusElement.textContent = `Socket error: ${error}`;
    });
    
    socket.on('game_state', (data) => {
        players = data.players;
        updatePlayerCount();
    });
    
    socket.on('player_joined', (data) => {
        players = data.players;
        updatePlayerCount();
    });
    
    socket.on('player_left', (data) => {
        players = data.players;
        updatePlayerCount();
    });
}

// Update player count display
function updatePlayerCount() {
    const count = Object.keys(players).length;
    playerCountElement.textContent = `Players: ${count}`;
}

// Handle button controls
document.getElementById('up-btn').addEventListener('mousedown', () => keys.up = true);
document.getElementById('up-btn').addEventListener('mouseup', () => keys.up = false);
document.getElementById('up-btn').addEventListener('touchstart', (e) => {
    e.preventDefault();
    keys.up = true;
});
document.getElementById('up-btn').addEventListener('touchend', (e) => {
    e.preventDefault();
    keys.up = false;
});

document.getElementById('down-btn').addEventListener('mousedown', () => keys.down = true);
document.getElementById('down-btn').addEventListener('mouseup', () => keys.down = false);
document.getElementById('down-btn').addEventListener('touchstart', (e) => {
    e.preventDefault();
    keys.down = true;
});
document.getElementById('down-btn').addEventListener('touchend', (e) => {
    e.preventDefault();
    keys.down = false;
});

document.getElementById('left-btn').addEventListener('mousedown', () => keys.left = true);
document.getElementById('left-btn').addEventListener('mouseup', () => keys.left = false);
document.getElementById('left-btn').addEventListener('touchstart', (e) => {
    e.preventDefault();
    keys.left = true;
});
document.getElementById('left-btn').addEventListener('touchend', (e) => {
    e.preventDefault();
    keys.left = false;
});

document.getElementById('right-btn').addEventListener('mousedown', () => keys.right = true);
document.getElementById('right-btn').addEventListener('mouseup', () => keys.right = false);
document.getElementById('right-btn').addEventListener('touchstart', (e) => {
    e.preventDefault();
    keys.right = true;
});
document.getElementById('right-btn').addEventListener('touchend', (e) => {
    e.preventDefault();
    keys.right = false;
});

// Handle keyboard controls
window.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp') keys.up = true;
    if (e.key === 'ArrowDown') keys.down = true;
    if (e.key === 'ArrowLeft') keys.left = true;
    if (e.key === 'ArrowRight') keys.right = true;
});

window.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowUp') keys.up = false;
    if (e.key === 'ArrowDown') keys.down = false;
    if (e.key === 'ArrowLeft') keys.left = false;
    if (e.key === 'ArrowRight') keys.right = false;
});

// Connect button event
connectButton.addEventListener('click', connectToServer);

// Game loop
function gameLoop() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Update player position based on keys
    if (isConnected) {
        if (keys.up) playerPos.y -= playerSpeed;
        if (keys.down) playerPos.y += playerSpeed;
        if (keys.left) playerPos.x -= playerSpeed;
        if (keys.right) playerPos.x += playerSpeed;
        
        // Keep player within canvas bounds
        playerPos.x = Math.max(0, Math.min(playerPos.x, canvas.width));
        playerPos.y = Math.max(0, Math.min(playerPos.y, canvas.height));
        
        // Send position to server
        socket.emit('player_move', playerPos);
    }
    
    // Draw all players
    for (const [id, player] of Object.entries(players)) {
        // Draw player circle
        ctx.beginPath();
        ctx.arc(player.x, player.y, 20, 0, Math.PI * 2);
        
        // Set color based on whether it's the current player or not
        if (id === myId) {
            ctx.fillStyle = 'rgba(0, 0, 255, 0.7)'; // Blue for current player
        } else {
            ctx.fillStyle = 'rgba(255, 0, 0, 0.7)'; // Red for other players
        }
        
        ctx.fill();
        ctx.closePath();
    }
    
    // Request next frame
    requestAnimationFrame(gameLoop);
}

// Start game loop
gameLoop(); 