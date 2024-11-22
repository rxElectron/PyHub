// electron_app/preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // Define methods you want to expose
  openConsole: () => ipcRenderer.send('open-console-window')
});
