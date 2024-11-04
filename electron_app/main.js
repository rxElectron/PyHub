const { app, BrowserWindow } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 1780,
    height: 836,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  const appURL = 'http://127.0.0.1:5000/';
  console.log(`Loading URL: ${appURL}`);  // Log the URL
  win.loadURL(appURL);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
