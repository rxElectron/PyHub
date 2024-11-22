// static/js/live_consoleScript.js

let tabCount = 1;
let terminalInstances = {};
let pythonConsoleEditors = {};

document.addEventListener("DOMContentLoaded", () => {
  // Initialize CodeMirror for the first Python Console tab
  initializePythonConsole(`editor-1`);

  const executeBtn = document.getElementById("execute-btn-1");
  const clearBtn = document.getElementById("clear-btn-1");
  const saveBtn = document.getElementById("save-btn-1");
  const loadBtn = document.getElementById("load-btn-1");
  const newTabBtn = document.getElementById("new-tab-btn");
  const tabs = document.getElementById("tabs");

  // بررسی وجود دکمه‌ها قبل از افزودن رویدادها
  if (executeBtn) {
    executeBtn.addEventListener("click", (event) => {
      event.preventDefault();
      executePythonCode(1);
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener("click", (event) => {
      event.preventDefault();
      clearPythonConsole(1);
    });
  }

  if (saveBtn) {
    saveBtn.addEventListener("click", (event) => {
      event.preventDefault();
      saveCode(1);
    });
  }

  if (loadBtn) {
    loadBtn.addEventListener("click", (event) => {
      event.preventDefault();
      loadCode(1);
    });
  }

  if (newTabBtn) {
    newTabBtn.addEventListener("click", createNewTab);
  }

  if (tabs) {
    tabs.addEventListener("click", (event) => {
      if (event.target.classList.contains("tab")) {
        switchTab(event.target);
        const tabId = event.target.getAttribute("data-tab");

        if (tabId.startsWith("terminal") && !terminalInstances[tabId]) {
          initializeTerminal(tabId);
        }
      }
    });
  }

  const themeToggleBtn = document.getElementById("theme-toggle-btn");
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", toggleTheme);
  }
});

// ------------------------
// Python Console Functions
// ------------------------

function initializePythonConsole(editorId) {
  const editorElement = document.getElementById(editorId);
  if (!editorElement) {
    console.error(`Element with ID ${editorId} not found.`);
    return;
  }

  const editorInstance = CodeMirror(editorElement, {
    mode: "python",
    theme: "dracula",
    lineNumbers: true,
    indentUnit: 4,
    matchBrackets: true,
    autoCloseBrackets: true,
    extraKeys: {
      "Ctrl-Space": "autocomplete",
      "Ctrl-/": "toggleComment",
    },
  });

  editorInstance.setSize("100%", "20rem");
  pythonConsoleEditors[editorId] = editorInstance;
}

function executePythonCode(tabNumber) {
  const editorId = `editor-${tabNumber}`;
  const editorInstance = pythonConsoleEditors[editorId];
  if (!editorInstance) {
    alert(`Editor ${editorId} not found.`);
    return;
  }
  const code = editorInstance.getValue();

  // Establish SocketIO connection if not exists
  if (!editorInstance.socket) {
    const socket = io('/python_console');

    socket.on('connect', () => {
      console.log(`Connected to Python Console namespace for tab ${tabNumber}`);
    });

    socket.on('execution_result', (data) => {
      const consoleOutput = document.getElementById(`console-output-${tabNumber}`);
      if (consoleOutput) {
        consoleOutput.innerText += data.output + "\n";
      }
    });

    socket.on('disconnect', () => {
      console.log(`Disconnected from Python Console namespace for tab ${tabNumber}`);
    });

    editorInstance.socket = socket;
  }

  // Emit execute_code event
  editorInstance.socket.emit('execute_code', { code: code });
}

function clearPythonConsole(tabNumber) {
  const consoleOutput = document.getElementById(`console-output-${tabNumber}`);
  if (consoleOutput) {
    consoleOutput.innerText = "";
  }
}

function saveCode(tabNumber) {
  const editorId = `editor-${tabNumber}`;
  const editorInstance = pythonConsoleEditors[editorId];
  if (!editorInstance) {
    alert(`Editor ${editorId} not found.`);
    return;
  }
  const code = editorInstance.getValue();

  fetch("/save_code", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        alert("کد با موفقیت ذخیره شد!");
      } else {
        alert("ذخیره کد ناموفق بود.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("یک خطا رخ داد هنگام ذخیره کد.");
    });
}

// ------------------------
// Terminal Functions
// ------------------------

function initializeTerminal(tabId) {
  const terminalElement = document.getElementById(tabId);
  if (!terminalElement) {
    console.error(`Element with ID ${tabId} not found.`);
    return;
  }

  const terminalInstance = new Terminal();
  terminalInstance.open(terminalElement);
  terminalInstances[tabId] = terminalInstance;

  const socket = io('/terminal');

  socket.on('connect', () => {
    terminalInstance.writeln('Connected to server.\r\n');
  });

  socket.on('terminal_output', (data) => {
    terminalInstance.write(data);
  });

  socket.on('disconnect', () => {
    terminalInstance.writeln('\r\nDisconnected from server.');
  });

  terminalInstance.onData(data => {
    socket.emit('execute_command', { command: data });
  });
}

// ------------------------
// Theme Toggle Function
// ------------------------

function toggleTheme() {
  const body = document.body;
  if (body.classList.contains("dark-mode")) {
    body.classList.remove("dark-mode");
    body.classList.add("light-mode");

    // تغییر تم CodeMirror
    for (let editorId in pythonConsoleEditors) {
      pythonConsoleEditors[editorId].setOption("theme", "default");
    }

    // تغییر تم xterm.js
    for (let tabId in terminalInstances) {
      terminalInstances[tabId].setOption('theme', {
        background: '#ffffff',
        foreground: '#000000'
      });
    }
  } else {
    body.classList.remove("light-mode");
    body.classList.add("dark-mode");

    // تغییر تم CodeMirror
    for (let editorId in pythonConsoleEditors) {
      pythonConsoleEditors[editorId].setOption("theme", "dracula");
    }

    // تغییر تم xterm.js
    for (let tabId in terminalInstances) {
      terminalInstances[tabId].setOption('theme', {
        background: '#1e1e1e',
        foreground: '#d4d4d4'
      });
    }
  }
}

// ------------------------
// Tab Management Functions
// ------------------------

function createNewTab() {
  tabCount += 1;
  const newTabId = `tab-${tabCount}`;
  const tabs = document.getElementById("tabs");
  const tabContent = document.getElementById("tab-content");

  if (!tabs || !tabContent) {
    alert("Tabs container not found.");
    return;
  }

  // انتخاب نوع تب (Python Console یا Terminal)
  const tabType = prompt("Select tab type:\n1. Python Console\n2. Terminal");
  if (!tabType || !['1', '2'].includes(tabType)) {
    alert("Invalid tab type selected.");
    tabCount -= 1;
    return;
  }

  // ایجاد تب جدید
  const newTab = document.createElement("li");
  newTab.classList.add("tab");
  newTab.setAttribute("data-tab", newTabId);
  newTab.innerText = tabType === '1' ? `Python Console ${tabCount}` : `Terminal ${tabCount}`;
  tabs.appendChild(newTab);

  // ایجاد محتوای تب جدید
  const newTabPane = document.createElement("div");
  newTabPane.classList.add("tab-pane");
  newTabPane.setAttribute("id", newTabId);

  if (tabType === '1') {
    // Python Console Tab
    newTabPane.innerHTML = `
      <div class="sum-box">
        <div class="box">
          <div class="top">
            <span>
              <button class="reset-btn">
                <p>Py.Console</p>
              </button>
              <button class="reset-btn" onclick="closeTab('${newTabId}')">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="icons">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
              </button>
            </span>
          </div>
          <div class="shell">
            <p>Python Interactive Shell</p>
            <div class="btns">
              <button class="w-btn">AI</button>
              <button class="w-btn" onclick="toggleEnhancer()">
                <!-- SVG مشابه -->
              </button>
            </div>
          </div>
          <form>
            <div id="editor-${tabCount}" class="console-input"></div>
          </form>
          <div class="w-btns">
            <button class="w-btn" id="reset-btn-${tabCount}">
              <!-- Reset Icon SVG -->
            </button>
            <div class="btns">
              <button class="w-btn btn1" id="execute-btn-${tabCount}">Execute</button>
              <button class="w-btn" id="clear-btn-${tabCount}">Clear</button>
              <button class="w-btn" id="save-btn-${tabCount}">
                <!-- Save Icon SVG -->
              </button>
              <button class="w-btn" id="load-btn-${tabCount}">Load</button>
            </div>
          </div>
          <div id="console-output-${tabCount}" class="result"></div>
        </div>
      </div>
    `;
    tabContent.appendChild(newTabPane);
    switchTab(newTab);
    initializePythonConsole(`editor-${tabCount}`);
    attachPythonConsoleEventListeners(tabCount);
  } else {
    // Terminal Tab
    newTabPane.innerHTML = `
      <div class="sum-box">
        <div class="box">
          <div class="top">
            <span>
              <button class="reset-btn">
                <p>Terminal</p>
              </button>
              <button class="reset-btn" onclick="closeTab('${newTabId}')">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="icons">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
              </button>
            </span>
          </div>
          <div id="${newTabId}" style="height: 20rem;"></div>
        </div>
      </div>
    `;
    tabContent.appendChild(newTabPane);
    switchTab(newTab);
    initializeTerminal(newTabId);
  }
}

function attachPythonConsoleEventListeners(tabNumber) {
  const executeBtn = document.getElementById(`execute-btn-${tabNumber}`);
  const clearBtn = document.getElementById(`clear-btn-${tabNumber}`);
  const saveBtn = document.getElementById(`save-btn-${tabNumber}`);
  const loadBtn = document.getElementById(`load-btn-${tabNumber}`);

  if (executeBtn) {
    executeBtn.addEventListener("click", (event) => {
      event.preventDefault();
      executePythonCode(tabNumber);
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener("click", (event) => {
      event.preventDefault();
      clearPythonConsole(tabNumber);
    });
  }

  if (saveBtn) {
    saveBtn.addEventListener("click", (event) => {
      event.preventDefault();
      saveCode(tabNumber);
    });
  }

  if (loadBtn) {
    loadBtn.addEventListener("click", (event) => {
      event.preventDefault();
      loadCode(tabNumber);
    });
  }
}

function closeTab(tabId) {
  const tab = document.querySelector(`.tab[data-tab="${tabId}"]`);
  const tabPane = document.getElementById(tabId);

  if (tab && tabPane) {
    // بستن SocketIO connections
    if (tabId.startsWith("editor-")) {
      const tabNumber = tabId.split('-')[1];
      const editorInstance = pythonConsoleEditors[`editor-${tabNumber}`];
      if (editorInstance && editorInstance.socket) {
        editorInstance.socket.disconnect();
      }
      delete pythonConsoleEditors[`editor-${tabNumber}`];
    } else if (tabId.startsWith("terminal")) {
      if (terminalInstances[tabId]) {
        // بستن ترمینال
        terminalInstances[tabId].dispose();
        delete terminalInstances[tabId];
      }
    }

    // حذف تب و محتوای آن
    tab.remove();
    tabPane.remove();

    // فعال‌سازی تب بعدی به صورت خودکار
    const remainingTabs = document.querySelectorAll(".tab");
    if (remainingTabs.length > 0) {
      switchTab(remainingTabs[remainingTabs.length - 1]);
    }
  }
}

// ------------------------
// Additional Functions
// ------------------------

function toggleAI() {
  // Implement AI feature toggle
  alert("AI Features toggled.");
}

function toggleEnhancer() {
  // Implement Enhancer feature toggle
  alert("Enhancer toggled.");
}

// Function to navigate back
function navigateBack() {
  window.history.back();
}

function loadFile(tabNumber) {
  const filename = prompt("Enter the filename to load (e.g., file.txt, image.png, document.pdf):");
  if (!filename) return;

  fetch(`/load_file?filename=${filename}`)
    .then(response => response.json())
    .then(data => {
      if (data.status === "success") {
        const tabId = `tab-${tabNumber}`;
        const tabPane = document.getElementById(tabId);

        if (data.type === "image") {
          const img = document.createElement("img");
          img.src = `data:image/*;base64,${data.data}`;
          img.style.maxWidth = "100%";
          img.style.height = "auto";
          tabPane.innerHTML = ''; // پاکسازی محتوای قبلی
          tabPane.appendChild(img);
        } else if (data.type === "pdf") {
          const iframe = document.createElement("iframe");
          iframe.src = `data:application/pdf;base64,${data.data}`;
          iframe.width = "100%";
          iframe.height = "600px";
          tabPane.innerHTML = ''; // پاکسازی محتوای قبلی
          tabPane.appendChild(iframe);
        } else if (data.type === "text") {
          const pre = document.createElement("pre");
          pre.innerText = data.data;
          pre.style.whiteSpace = "pre-wrap";
          tabPane.innerHTML = ''; // پاکسازی محتوای قبلی
          tabPane.appendChild(pre);
        } else {
          alert("Unsupported file type.");
        }
      } else {
        alert(data.message);
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("An error occurred while loading the file.");
    });
}

// به‌روزرسانی تابع loadCode برای مدیریت انواع فایل‌ها
function loadCode(tabNumber) {
  const filename = prompt("Enter the filename to load (e.g., file.py, image.png):");
  if (!filename) return;

  fetch(`/load_file?filename=${filename}`)
    .then(response => response.json())
    .then(data => {
      if (data.status === "success") {
        const tabId = `tab-${tabNumber}`;
        const tabPane = document.getElementById(tabId);
        const editorId = `editor-${tabNumber}`;

        if (data.type === "text") {
          if (pythonConsoleEditors[editorId]) {
            pythonConsoleEditors[editorId].setValue(data.data);
            alert("کد بارگذاری شد.");
          }
        } else {
          // برای فایل‌های غیرمتنی مانند تصویر و PDF
          loadFile(tabNumber);
        }
      } else {
        alert(data.message);
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("An error occurred while loading the file.");
    });
}

// ------------------------
// Tab Switching Function
// ------------------------

function switchTab(selectedTab) {
  const tabs = document.querySelectorAll(".tab");
  const tabPanes = document.querySelectorAll(".tab-pane");

  tabs.forEach(tab => {
    tab.classList.remove("active");
  });

  tabPanes.forEach(pane => {
    pane.classList.remove("active");
  });

  selectedTab.classList.add("active");
  const tabId = selectedTab.getAttribute("data-tab");
  const activePane = document.getElementById(tabId);
  if (activePane) {
    activePane.classList.add("active");
  }
}
