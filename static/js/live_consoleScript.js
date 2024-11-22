// static/js/live_consoleScript.js
document.addEventListener("DOMContentLoaded", () => {
  const executeBtn = document.getElementById("execute-btn");
  const clearBtn = document.getElementById("clear-btn");
  const saveBtn = document.getElementById("save-btn");

  executeBtn.addEventListener("click", (event) => {
    event.preventDefault();
    executeCode();
  });

  clearBtn.addEventListener("click", (event) => {
    event.preventDefault();
    clearConsole();
  });

  saveBtn.addEventListener("click", (event) => {
    event.preventDefault();
    saveCode();
  });
});

function executeCode() {
  const code = document.getElementById("python-console").value;
  fetch("/execute", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code }),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("console-output").innerText = data.output;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function clearConsole() {
  document.getElementById("python-console").value = "";
  document.getElementById("console-output").innerText = "";
}

function resetConsole() {
  clearConsole();
  // Additional reset logic if needed
}

function saveCode() {
  const code = document.getElementById("python-console").value;
  // Implement save functionality, e.g., send to backend or download as file
  fetch("/save_code", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code }),
  })
    .then((response) => response.json())
    .then((data) => {
      alert("Code saved successfully!");
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function toggleAI() {
  // Implement AI feature toggle
  alert("AI Features toggled.");
}

// function toggleAI() {
//   // Example: Fetch AI suggestions based on current code
//   const code = document.getElementById("python-console").value;
//   fetch("/ai_suggestions", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ code }),
//   })
//     .then(response => response.json())
//     .then(data => {
//       // Display AI suggestions in the UI
//       alert("AI Features toggled.");
//       // Implement displaying suggestions
//     })
//     .catch(error => {
//       console.error("Error:", error);
//     });
// }

// function toggleEnhancer() {
//   // Example: Toggle syntax highlighting
//   const textarea = document.getElementById("python-console");
//   textarea.classList.toggle("syntax-highlight");
//   alert("Enhancer toggled.");
// }

function toggleEnhancer() {
  // Implement Enhancer feature toggle
  alert("Enhancer toggled.");
}


// Function to navigate back
function navigateBack() {
  window.history.back();
}