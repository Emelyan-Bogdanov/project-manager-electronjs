const { app, BrowserWindow, ipcMain } = require("electron");

const fs = require("fs");
const path = require("path");

let win;

// main window
function MainApp() {
  win = new BrowserWindow({
    width: 1400,
    height: 800,
    minWidth: 1400,
    minHeight: 730,
    // movable: false, // position fixe
    icon: "../assets/imgs/icon.png",
    title: "Gestionnaire de projets",
    center: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: true, 
      enableRemoteModule: false,
      preload: path.join(__dirname, "preload.js"), // use a preload script
    },

    // frame:false // remove top bar buttons [minimize,fullscreen,close]
  });

  // win.loadFile("./window.js")
  win.loadFile("src/templates/index.html");

  ipcMain.on("open-profile", () => {
    win.loadFile("src/templates/profile.html");
  });

  ipcMain.on("all-users", () => {
    win.loadFile("src/templates/allUsers.html");
  });

  win.on("closed", () => {
    win = null;
  });
}

app.whenReady().then(MainApp);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

// if profile username clicked => goto profile infos

// do something before closing the window
app.on("before-quit", () => {});
