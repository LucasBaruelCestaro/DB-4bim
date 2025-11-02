const { app, BrowserWindow } = require("electron");
const path = require("path");

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    autoHideMenuBar: true,
    icon: "assets/icon.ico",
  });

    win.loadURL("http://127.0.0.1:5000/");
}

app.whenReady().then(createWindow);
