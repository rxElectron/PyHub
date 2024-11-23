// static/js/live_console/tab_manager.js

// Initialize tab state
let tabs = [];
let activeTabId = null;

// Debounce timer for input events
let debounceTimer;

// Constants for localStorage keys
const STORAGE_KEYS = {
  TABS: "liveConsoleTabs",
  THEME: "liveConsoleTheme",
};

// Function to generate a UUID for unique tab IDs
function generateUUID() {
  // Public Domain/MIT
  let d = new Date().getTime(); // Timestamp
  let d2 =
    (performance && performance.now && performance.now() * 1000) || 0; // Time in microseconds since page-load or 0 if unsupported
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    let r = Math.random() * 16; // Random number between 0 and 16
    if (d > 0) {
      r = (d + r) % 16 | 0;
      d = Math.floor(d / 16);
    } else {
      r = (d2 + r) % 16 | 0;
      d2 = Math.floor(d2 / 16);
    }
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });
}

// Function to add a new tab
function addTab(type, id = null, content = "") {
  const newTabId = id || generateUUID();
  const tabData = { id: newTabId, type: type, content: content, active: false };
  tabs.push(tabData);

  // Create the new tab element
  const tabElement = document.createElement("span");
  tabElement.classList.add("tab");
  tabElement.dataset.id = newTabId;
  tabElement.dataset.type = type;
  tabElement.innerHTML =
    type === "Terminal"
      ? `
    <button class="reset-btn" aria-label="Terminal Tab">
      <p>Terminal ID: ${newTabId}</p>
    </button>
    <button class="reset-btn close-btn" onclick="removeTab('${newTabId}')" aria-label="Close Tab">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
        stroke="currentColor" class="icons">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"></path>
      </svg>
    </button>
  `
      : `
    <button class="reset-btn" aria-label="Py.Console Tab">
      <p>Py.Console ID: ${newTabId}</p>
    </button>
    <button class="reset-btn close-btn" onclick="removeTab('${newTabId}')" aria-label="Close Tab">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
        stroke="currentColor" class="icons">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"></path>
      </svg>
    </button>
  `;

  // Set active tab on click (excluding close button)
  tabElement.addEventListener("click", (e) => {
    if (e.target.closest(".close-btn")) return; // Ignore clicks on close buttons
    setActiveTab(newTabId);
  });

  // Append the new tab to the #tabs-container
  document.getElementById("tabs-container").appendChild(tabElement);

  // Set the new tab as active
  setActiveTab(newTabId);

  // Save tabs to localStorage
  saveTabsToStorage();
}

// Function to set a tab as active
function setActiveTab(tabId) {
  // Update the active state in the tabs array
  tabs.forEach((tab) => {
    tab.active = tab.id === tabId;
  });
  activeTabId = tabId;

  // Update active class in the DOM
  document.querySelectorAll(".tab").forEach((tabElement) => {
    if (tabElement.dataset.id === tabId) {
      tabElement.classList.add("active");
    } else {
      tabElement.classList.remove("active");
    }
  });

  // Update the console title and input field
  const activeTab = tabs.find((tab) => tab.id === tabId);
  if (activeTab) {
    document.getElementById("active-console-title").innerText = `${activeTab.type} Console`;
    document.getElementById("python-console").value = activeTab.content || "";
  } else {
    document.getElementById("active-console-title").innerText = "No Active Console";
    document.getElementById("python-console").value = "";
  }

  // Update result output
  updateResultOutput();
}

// Function to remove a specific tab
function removeTab(tabId) {
  const tabIndex = tabs.findIndex((tab) => tab.id === tabId);
  if (tabIndex === -1) {
    console.warn(`Tab with ID ${tabId} does not exist.`);
    return;
  }

  tabs.splice(tabIndex, 1);

  // Remove the tab element from the DOM
  const tabElement = document.querySelector(`.tab[data-id='${tabId}']`);
  if (tabElement) tabElement.remove();

  // If the removed tab was active, set another tab as active
  if (tabId === activeTabId) {
    if (tabs.length > 0) {
      setActiveTab(tabs[0].id); // Set the first tab as active
    } else {
      activeTabId = null;
      document.getElementById("active-console-title").innerText = "No Active Console";
      document.getElementById("python-console").value = "";
      document.getElementById("result-output").innerHTML = "";
    }
  }

  // Save tabs to localStorage
  saveTabsToStorage();
}

// Function to remove all tabs of a specific type
function removeAllTabs(type) {
  // Find all tabs of the specified type
  const tabsToRemove = tabs.filter((tab) => tab.type === type);

  // Remove each tab from the array and DOM
  tabsToRemove.forEach((tab) => {
    removeTab(tab.id);
  });

  // Save tabs to localStorage
  saveTabsToStorage();
}

// Function to execute code in the active tab
function executeCurrentTab() {
  const activeTab = tabs.find((tab) => tab.id === activeTabId);
  if (!activeTab) {
    alert("No active tab to execute!");
    return;
  }

  const code = document.getElementById("python-console").value.trim();
  if (code === "") {
    alert("Cannot execute empty code!");
    return;
  }

  activeTab.content = code; // Save the code to the active tab's content
  updateResultOutput(`Executing in ${activeTab.type}:<br><pre>${escapeHTML(code)}</pre>`);

  // TODO: Integrate with backend to execute Python code and fetch results

  // Save tabs to localStorage
  saveTabsToStorage();
}

// Function to clear content of the active tab
function clearCurrentTab() {
  const activeTab = tabs.find((tab) => tab.id === activeTabId);
  if (!activeTab) {
    alert("No active tab to clear!");
    return;
  }

  activeTab.content = ""; // Clear the content
  document.getElementById("python-console").value = ""; // Clear the console input
  updateResultOutput(`Cleared content for ${activeTab.type}`);

  // Save tabs to localStorage
  saveTabsToStorage();
}

// Function to update the result display
function updateResultOutput(message = "") {
  const activeTab = tabs.find((tab) => tab.id === activeTabId);
  if (!activeTab) {
    document.getElementById("result-output").innerHTML = "";
    return;
  }

  if (!message) {
    message = activeTab.content
      ? `Last executed in ${activeTab.type}:<br><pre>${escapeHTML(activeTab.content)}</pre>`
      : `No code executed in ${activeTab.type}.`;
  }

  document.getElementById("result-output").innerHTML = `<p>${message}</p>`;
}

// Function to escape HTML to prevent XSS
function escapeHTML(str) {
  return str.replace(/[&<>'"]/g, (tag) => {
    const charsToReplace = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "'": "&#39;",
      '"': "&quot;",
    };
    return charsToReplace[tag] || tag;
  });
}

// Function to show a modal for adding consoles
function showAddConsoleModal() {
  const modalContent = `
    <div class="modal-overlay" onclick="closeModal()">
      <div class="modal-content" onclick="event.stopPropagation()">
        <button class="modal-btn" onclick="addTab('Py.Console'); closeModal();" aria-label="Add Py.Console">Add Py.Console</button>
        <button class="modal-btn" onclick="addTab('Terminal'); closeModal();" aria-label="Add Terminal">Add Terminal</button>
        <button class="modal-btn" onclick="closeModal()" aria-label="Close Modal">Close</button>
      </div>
    </div>`;
  document.body.insertAdjacentHTML("beforeend", modalContent);
}

// Function to close the modal
function closeModal() {
  const modal = document.querySelector(".modal-overlay");
  if (modal) modal.remove();
}

// Function to toggle the theme between light and dark
function toggleTheme() {
  const currentTheme = document.body.getAttribute("data-theme") || "light";
  const newTheme = currentTheme === "light" ? "dark" : "light";
  document.body.setAttribute("data-theme", newTheme);
  localStorage.setItem(STORAGE_KEYS.THEME, newTheme);
}

// Function to save tabs to localStorage
function saveTabsToStorage() {
  localStorage.setItem(STORAGE_KEYS.TABS, JSON.stringify(tabs));
}

// Function to load tabs from localStorage
function loadTabsFromStorage() {
  const savedTabs = JSON.parse(localStorage.getItem(STORAGE_KEYS.TABS));
  if (savedTabs && Array.isArray(savedTabs)) {
    tabs = [];
    savedTabs.forEach((tab) => {
      addTab(tab.type, tab.id, tab.content);
    });
  } else {
    initializeDefaultTabs();
  }

  // Load theme
  const savedTheme = localStorage.getItem(STORAGE_KEYS.THEME);
  if (savedTheme) {
    document.body.setAttribute("data-theme", savedTheme);
  }
}

// Function to handle keyboard shortcuts
function handleKeyboardShortcuts(e) {
  if (e.ctrlKey && e.key === "t") {
    e.preventDefault();
    showAddConsoleModal();
  }
  if (e.ctrlKey && e.key === "w") {
    e.preventDefault();
    if (activeTabId) {
      removeTab(activeTabId);
    }
  }
  if (e.ctrlKey && e.key === "k") {
    e.preventDefault();
    toggleTheme();
  }
}

// Function to initialize default tabs
function initializeDefaultTabs() {
  addTab("Py.Console"); // Add a Py.Console tab
  addTab("Terminal"); // Add a Terminal tab
}

// Function to initialize event listeners
function initializeEventListeners() {
  // Attach the modal display function to the add-console-selector button
  const addConsoleBtn = document.getElementById("add-console-selector");
  if (addConsoleBtn) {
    addConsoleBtn.addEventListener("click", showAddConsoleModal);
  }

  // Attach execute and clear buttons
  const executeBtn = document.querySelector(".btn1");
  if (executeBtn) {
    executeBtn.addEventListener("click", executeCurrentTab);
  }

  const clearBtn = document.querySelector(".btns .w-btn:nth-child(2)");
  if (clearBtn) {
    clearBtn.addEventListener("click", clearCurrentTab);
  }

  // Attach theme toggle button
  const themeToggleBtn = document.querySelector("#tab-controls .w-btn:nth-child(3)");
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", toggleTheme);
  }

  // Attach keyboard shortcuts
  document.addEventListener("keydown", handleKeyboardShortcuts);

  // Attach input event with debounce
  const consoleInput = document.getElementById("python-console");
  if (consoleInput) {
    consoleInput.addEventListener("input", (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        const activeTab = tabs.find((tab) => tab.id === activeTabId);
        if (activeTab) {
          activeTab.content = e.target.value;
          saveTabsToStorage();
        }
      }, 300);
    });
  }
}

// Function to initialize the page
function initializePage() {
  loadTabsFromStorage();
  initializeEventListeners();
}

// Function to handle window unload (optional: ensure data is saved)
window.addEventListener("beforeunload", saveTabsToStorage);

// Initialize the page when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", initializePage);
