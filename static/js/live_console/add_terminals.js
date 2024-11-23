// // static/js/live_console/add_terminals.js

// document.addEventListener("DOMContentLoaded", () => {
//   // Button that triggers the modal
//   const launchBtn = document.querySelector(".w-btn");

//   // Create and append modal to the body
//   const modal = document.createElement("div");
//   modal.classList.add("modal");
//   modal.innerHTML = `
//       <div class="modal-content">
//         <h2>Select Environment</h2>
//         <button id="terminal-btn">Open Terminal</button>
//         <button id="python-btn">Open Python</button>
//         <button id="close-modal">Close</button>
//       </div>
//     `;
//   document.body.appendChild(modal);

//   // Show modal on button click
//   launchBtn.addEventListener("click", () => {
//     modal.style.display = "block";
//   });

//   // Close modal functionality
//   const closeModalBtn = document.getElementById("close-modal");
//   closeModalBtn.addEventListener("click", () => {
//     modal.style.display = "none";
//   });

//   // Initialize Socket.IO connections
//   const pythonSocket = io("/python_console");
//   const terminalSocket = io("/terminal");

//   // Select buttons
//   const terminalBtn = document.getElementById("terminal-btn");
//   const pythonBtn = document.getElementById("python-btn");

//   // Terminal container
//   const terminalContainer = document.createElement("div");
//   terminalContainer.id = "terminal-container";
//   terminalContainer.style.height = "300px";
//   terminalContainer.style.marginTop = "1rem";
//   document.querySelector(".result").appendChild(terminalContainer);

//   // Initialize xterm.js terminal
//   const terminal = new Terminal({
//     cursorBlink: true,
//     theme: {
//       background: "#1e1e1e",
//       foreground: "#d4d4d4",
//     },
//   });
//   terminal.open(terminalContainer);

//   // Function to append output to the terminal
//   function appendToTerminal(data) {
//     terminal.write(data);
//   }

//   // Handle Terminal selection
//   terminalBtn.addEventListener("click", () => {
//     modal.style.display = "none";
//     terminal.clear();
//     appendToTerminal("Starting Terminal...\r\n");
//     terminalSocket.emit("start_terminal");
//   });

//   // Handle Python selection
//   pythonBtn.addEventListener("click", () => {
//     modal.style.display = "none";
//     terminal.clear();
//     appendToTerminal("Launching Python Interpreter...\r\n");
//     terminalSocket.emit("start_python");
//   });

//   // Listen for terminal outputs
//   terminalSocket.on("terminal_output", (data) => {
//     appendToTerminal(data);
//   });

//   // Listen for terminal closure
//   terminalSocket.on("terminal_closed", () => {
//     appendToTerminal("\r\nProcess terminated.\r\n");
//   });

//   // Send user input to the backend
//   terminal.onData((input) => {
//     // Send input to the appropriate namespace based on the current process
//     // For simplicity, we'll assume a single active namespace
//     if (terminalSocket && terminalSocket.connected) {
//       terminalSocket.emit("execute_command", { command: input });
//     }
//   });

//   // Optional: Handle Python console separately if needed
//   /*
//     pythonSocket.on("execution_result", (data) => {
//       appendToTerminal(data.output);
//     });
  
//     document.querySelector(".execute-python-btn").addEventListener("click", () => {
//       const code = document.querySelector(".console-input").value;
//       pythonSocket.emit("execute_code", { code });
//     });
//     */
// });
