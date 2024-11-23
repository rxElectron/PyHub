// static/js/live_console/terminal_manager.js

// Ensure the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    // Initialize Socket.IO
    const socket = io();
  
    // Initialize xterm.js
    const term = new Terminal({
      cursorBlink: true,
      rows: 20,
      cols: 80,
      theme: {
        background: '#1e1e1e',
        foreground: '#ffffff',
        cursor: '#ffffff',
        selection: '#44475a',
      }
    });
  
    // Load the Fit Addon and fit the terminal to its container
    const fitAddon = new FitAddon.FitAddon();
    term.loadAddon(fitAddon);
    term.open(document.getElementById('terminal-container'));
    fitAddon.fit();
  
    // Handle window resize
    window.addEventListener('resize', () => {
      fitAddon.fit();
    });
  
    // When the terminal is ready, notify the backend
    term.onData(data => {
      socket.emit('input', data);
    });
  
    // Listen for output from the backend and write it to the terminal
    socket.on('output', (data) => {
      term.write(data);
    });
  
    // Listen for terminal initialization
    socket.on('connect', () => {
      term.writeln('Connected to the terminal backend.\r\n');
    });
  
    socket.on('disconnect', () => {
      term.writeln('\r\nDisconnected from the terminal backend.');
    });
  });
  