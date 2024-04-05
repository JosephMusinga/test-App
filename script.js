const captionElement = document.getElementById('caption');
let ws = new WebSocket("ws://localhost:8765");  // Adjust URL

ws.onmessage = (event) => {
    captionElement.textContent = event.data;
};

// Microphone handling (Optional):
