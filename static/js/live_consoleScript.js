// // static/js/live_consoleScript.js

// let tabCount = 1;
// let terminalInstances = {};
// let pythonConsoleEditors = {};

// // Utility function to generate unique tab IDs
// function generateTabId(type) {
//   return `${type}-tab-${tabCount}`;
// }

// document.addEventListener("DOMContentLoaded", () => {
//   // Initialize the first Python Console tab
//   initializePythonConsole(`python-console-editor-1`);

//   // Attach event listeners using event delegation
//   const tabContent = document.getElementById("tab-content");

//   tabContent.addEventListener("click", (event) => {
//     const target = event.target.closest(".btn");

//     if (!target) return;

//     // Handle Execute Button
//     if (target.classList.contains("btn1") && target.textContent.trim() === "Execute") {
//       const tabPane = target.closest(".tab-pane");
//       const tabNumber = tabPane.getAttribute("data-tab-number");
//       executePythonCode(tabNumber);
//     }

//     // Handle Clear Button
//     if (target.classList.contains("btn") && target.textContent.trim() === "Clear") {
//       const tabPane = target.closest(".tab-pane");
//       const tabNumber = tabPane.getAttribute("data-tab-number");
//       clearPythonConsole(tabNumber);
//     }

//     // Handle Save Button
//     if (target.classList.contains("btn") && target.getAttribute("aria-label") === "Save Code") {
//       const tabPane = target.closest(".tab-pane");
//       const tabNumber = tabPane.getAttribute("data-tab-number");
//       saveCode(tabNumber);
//     }

//     // Handle Load Button
//     if (target.classList.contains("btn") && target.getAttribute("aria-label") === "Load Code") {
//       const tabPane = target.closest(".tab-pane");
//       const tabNumber = tabPane.getAttribute("data-tab-number");
//       loadCode(tabNumber);
//     }

//     // Handle Close Tab Button
//     if (target.classList.contains("btn") && target.getAttribute("aria-label") === "Close Tab") {
//       const tabPane = target.closest(".tab-pane");
//       const tabId = tabPane.getAttribute("id");
//       closeTab(tabId);
//     }

//     // Handle AI and Enhancer Buttons (Optional)
//     if (target.classList.contains("w-btn") && target.textContent.trim() === "AI") {
//       toggleAI();
//     }

//     if (target.classList.contains("w-btn") && target.getAttribute("aria-label") === "Toggle Enhancer") {
//       toggleEnhancer();
//     }
//   });

//   // Handle New Tab Button
//   const newTabBtn = document.getElementById("new-tab-btn");
//   if (newTabBtn) {
//     newTabBtn.addEventListener("click", createNewTab);
//   }

//   // Handle Theme Toggle Button
//   const themeToggleBtn = document.getElementById("theme-toggle-btn");
//   if (themeToggleBtn) {
//     themeToggleBtn.addEventListener("click", toggleTheme);
//   }
// });

// // ------------------------
// // Python Console Functions
// // ------------------------

// function initializePythonConsole(editorId) {
//   const editorElement = document.getElementById(editorId);
//   if (!editorElement) {
//     console.error(`Element with ID ${editorId} not found.`);
//     return;
//   }

//   const editorInstance = CodeMirror(editorElement, {
//     mode: "python",
//     theme: "dracula",
//     lineNumbers: true,
//     indentUnit: 4,
//     matchBrackets: true,
//     autoCloseBrackets: true,
//     extraKeys: {
//       "Ctrl-Space": "autocomplete",
//       "Ctrl-/": "toggleComment",
//     },
//   });

//   editorInstance.setSize("100%", "20rem");
//   pythonConsoleEditors[editorId] = editorInstance;
// }

// function executePythonCode(tabNumber) {
//   const editorId = `python-console-editor-${tabNumber}`;
//   const editorInstance = pythonConsoleEditors[editorId];
//   if (!editorInstance) {
//     alert(`Editor ${editorId} not found.`);
//     return;
//   }
//   const code = editorInstance.getValue();

//   // Establish SocketIO connection if not exists
//   if (!editorInstance.socket) {
//     const socket = io('/python_console');

//     socket.on('connect', () => {
//       console.log(`Connected to Python Console namespace for tab ${tabNumber}`);
//     });

//     socket.on('execution_result', (data) => {
//       const consoleOutput = document.getElementById(`console-output-${tabNumber}`);
//       if (consoleOutput) {
//         // Handle image output
//         if (data.type === "image") {
//           const img = document.createElement("img");
//           img.src = `data:image/png;base64,${data.data}`;
//           img.style.maxWidth = "100%";
//           img.style.height = "auto";
//           consoleOutput.innerHTML += `<div>${img.outerHTML}</div>`;
//         } else if (data.type === "text") {
//           consoleOutput.innerText += data.output + "\n";
//         }
//       }
//     });

//     socket.on('disconnect', () => {
//       console.log(`Disconnected from Python Console namespace for tab ${tabNumber}`);
//     });

//     editorInstance.socket = socket;
//   }

//   // Emit execute_code event
//   editorInstance.socket.emit('execute_code', { code: code });
// }

// function clearPythonConsole(tabNumber) {
//   const consoleOutput = document.getElementById(`console-output-${tabNumber}`);
//   if (consoleOutput) {
//     consoleOutput.innerHTML = "";
//   }
// }

// function saveCode(tabNumber) {
//   const editorId = `python-console-editor-${tabNumber}`;
//   const editorInstance = pythonConsoleEditors[editorId];
//   if (!editorInstance) {
//     alert(`Editor ${editorId} not found.`);
//     return;
//   }
//   const code = editorInstance.getValue();

//   // انتخاب روش ذخیره‌سازی (LocalStorage یا سرور)
//   const saveMethod = prompt("Select save method:\n1. LocalStorage\n2. Server-side");

//   if (saveMethod === '1') {
//     // ذخیره در LocalStorage
//     localStorage.setItem(`userCodeTab${tabNumber}`, code);
//     alert("کد با موفقیت در LocalStorage ذخیره شد!");
//   } else if (saveMethod === '2') {
//     // ذخیره در سرور
//     fetch("/save_code", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ code }),
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         if (data.status === "success") {
//           alert("کد با موفقیت در سرور ذخیره شد!");
//         } else {
//           alert("ذخیره کد ناموفق بود.");
//         }
//       })
//       .catch((error) => {
//         console.error("Error:", error);
//         alert("یک خطا رخ داد هنگام ذخیره کد.");
//       });
//   } else {
//     alert("روش ذخیره‌سازی نامعتبر است.");
//   }
// }

// function loadFile(tabNumber) {
//   const filename = prompt("Enter the filename to load (e.g., file.txt, image.png, document.pdf):");
//   if (!filename) return;

//   fetch(`/load_file?filename=${encodeURIComponent(filename)}`)
//     .then(response => response.json())
//     .then(data => {
//       if (data.status === "success") {
//         const tabId = `tab-${tabNumber}`;
//         const tabPane = document.getElementById(tabId);

//         if (data.type === "image") {
//           const img = document.createElement("img");
//           img.src = `data:image/*;base64,${data.data}`;
//           img.style.maxWidth = "100%";
//           img.style.height = "auto";
//           tabPane.innerHTML = ''; // پاکسازی محتوای قبلی
//           tabPane.appendChild(img);
//         } else if (data.type === "pdf") {
//           const iframe = document.createElement("iframe");
//           iframe.src = `data:application/pdf;base64,${data.data}`;
//           iframe.width = "100%";
//           iframe.height = "600px";
//           tabPane.innerHTML = ''; // پاکسازی محتوای قبلی
//           tabPane.appendChild(iframe);
//         } else if (data.type === "text") {
//           const pre = document.createElement("pre");
//           pre.innerText = data.data;
//           pre.style.whiteSpace = "pre-wrap";
//           tabPane.innerHTML = ''; // پاکسازی محتوای قبلی
//           tabPane.appendChild(pre);
//         } else {
//           alert("Unsupported file type.");
//         }
//       } else {
//         alert(data.message);
//       }
//     })
//     .catch(error => {
//       console.error("Error:", error);
//       alert("An error occurred while loading the file.");
//     });
// }

// function loadCode(tabNumber) {
//   const filename = prompt("Enter the filename to load (e.g., file.py, image.png):");
//   if (!filename) return;

//   fetch(`/load_file?filename=${encodeURIComponent(filename)}`)
//     .then(response => response.json())
//     .then(data => {
//       if (data.status === "success") {
//         const tabId = `tab-${tabNumber}`;
//         const tabPane = document.getElementById(tabId);
//         const editorId = `python-console-editor-${tabNumber}`;

//         if (data.type === "text") {
//           if (pythonConsoleEditors[editorId]) {
//             pythonConsoleEditors[editorId].setValue(data.data);
//             alert("کد بارگذاری شد.");
//           }
//         } else {
//           // برای فایل‌های غیرمتنی مانند تصویر و PDF
//           loadFile(tabNumber);
//         }
//       } else {
//         alert(data.message);
//       }
//     })
//     .catch(error => {
//       console.error("Error:", error);
//       alert("An error occurred while loading the file.");
//     });
// }

// // ------------------------
// // Terminal Functions
// // ------------------------

// function initializeTerminal(tabId) {
//   const terminalElement = document.getElementById(tabId);
//   if (!terminalElement) {
//     console.error(`Element with ID ${tabId} not found.`);
//     return;
//   }

//   const terminalInstance = new Terminal({
//     cols: 80,
//     rows: 24,
//     theme: {
//       background: '#1e1e1e',
//       foreground: '#d4d4d4'
//     }
//   });
//   terminalInstance.open(terminalElement);
//   terminalInstances[tabId] = terminalInstance;

//   const socket = io('/terminal');

//   socket.on('connect', () => {
//     terminalInstance.writeln('Connected to server.\r\n');
//   });

//   socket.on('terminal_output', (data) => {
//     terminalInstance.write(data);
//   });

//   socket.on('disconnect', () => {
//     terminalInstance.writeln('\r\nDisconnected from server.');
//   });

//   terminalInstance.onData(data => {
//     socket.emit('execute_command', { command: data });
//   });
// }

// // ------------------------
// // Theme Toggle Function
// // ------------------------

// function toggleTheme() {
//   const body = document.body;
//   if (body.classList.contains("dark-mode")) {
//     body.classList.remove("dark-mode");
//     body.classList.add("light-mode");

//     // تغییر تم CodeMirror
//     for (let editorId in pythonConsoleEditors) {
//       pythonConsoleEditors[editorId].setOption("theme", "default");
//     }

//     // تغییر تم xterm.js
//     for (let tabId in terminalInstances) {
//       terminalInstances[tabId].setOption('theme', {
//         background: '#ffffff',
//         foreground: '#000000'
//       });
//     }
//   } else {
//     body.classList.remove("light-mode");
//     body.classList.add("dark-mode");

//     // تغییر تم CodeMirror
//     for (let editorId in pythonConsoleEditors) {
//       pythonConsoleEditors[editorId].setOption("theme", "dracula");
//     }

//     // تغییر تم xterm.js
//     for (let tabId in terminalInstances) {
//       terminalInstances[tabId].setOption('theme', {
//         background: '#1e1e1e',
//         foreground: '#d4d4d4'
//       });
//     }
//   }
// }



// // ------------------------
// // Additional Functions
// // ------------------------

// function toggleAI() {
//   // پیاده‌سازی قابلیت‌های AI
//   alert("AI Features toggled.");
// }

// function toggleEnhancer() {
//   // پیاده‌سازی قابلیت‌های Enhancer
//   alert("Enhancer toggled.");
// }

// // ------------------------
// // Save and Load Functions
// // ------------------------

// function loadFile(tabNumber) {
//   const filename = prompt("Enter the filename to load (e.g., file.txt, image.png, document.pdf):");
//   if (!filename) return;

//   fetch(`/load_file?filename=${encodeURIComponent(filename)}`)
//     .then(response => response.json())
//     .then(data => {
//       if (data.status === "success") {
//         const tabId = `tab-${tabNumber}`;
//         const tabPane = document.getElementById(tabId);

//         if (data.type === "image") {
//           const img = document.createElement("img");
//           img.src = `data:image/*;base64,${data.data}`;
//           img.style.maxWidth = "100%";
//           img.style.height = "auto";
//           tabPane.innerHTML = ''; // پاکسازی محتوای قبلی
//           tabPane.appendChild(img);
//         } else if (data.type === "pdf") {
//           const iframe = document.createElement("iframe");
//           iframe.src = `data:application/pdf;base64,${data.data}`;
//           iframe.width = "100%";
//           iframe.height = "600px";
//           tabPane.innerHTML = ''; // پاکسازی محتوای قبلی
//           tabPane.appendChild(iframe);
//         } else if (data.type === "text") {
//           const pre = document.createElement("pre");
//           pre.innerText = data.data;
//           pre.style.whiteSpace = "pre-wrap";
//           tabPane.innerHTML = ''; // پاکسازی محتوای قبلی
//           tabPane.appendChild(pre);
//         } else {
//           alert("Unsupported file type.");
//         }
//       } else {
//         alert(data.message);
//       }
//     })
//     .catch(error => {
//       console.error("Error:", error);
//       alert("An error occurred while loading the file.");
//     });
// }

// function loadCode(tabNumber) {
//   const filename = prompt("Enter the filename to load (e.g., file.py, image.png):");
//   if (!filename) return;

//   fetch(`/load_file?filename=${encodeURIComponent(filename)}`)
//     .then(response => response.json())
//     .then(data => {
//       if (data.status === "success") {
//         const tabId = `tab-${tabNumber}`;
//         const tabPane = document.getElementById(tabId);
//         const editorId = `python-console-editor-${tabNumber}`;

//         if (data.type === "text") {
//           if (pythonConsoleEditors[editorId]) {
//             pythonConsoleEditors[editorId].setValue(data.data);
//             alert("کد بارگذاری شد.");
//           }
//         } else {
//           // برای فایل‌های غیرمتنی مانند تصویر و PDF
//           loadFile(tabNumber);
//         }
//       } else {
//         alert(data.message);
//       }
//     })
//     .catch(error => {
//       console.error("Error:", error);
//       alert("An error occurred while loading the file.");
//     });
// }


