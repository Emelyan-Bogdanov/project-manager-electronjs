const { app, BrowserWindow } = require('electron');
const {MainApp} = require("./src/main/window")

const fs = require('fs');
const path = require('path');





app.whenReady().then(MainApp);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});


// do something before closing the window
app.on("before-quit",()=>{ 
    
})