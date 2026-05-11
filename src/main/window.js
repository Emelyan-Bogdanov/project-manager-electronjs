

const { BrowserWindow } = require('electron');

// main window
function MainApp() {
  const win = new BrowserWindow({
    width: 1024,
    height: 500,
    // movable: false, // position fixe 
    icon: '../assets/imgs/icon.png',
    title: "Gestionnaire de projets",
    center : true,
    // frame:false // remove top bar buttons [minimize,fullscreen,close]

  });

    win.loadFile("./window.js")
    win.loadFile('src/templates/index.html');

//   win.loadFile('src/templates/main.html');
}



// exports everything if want to import from outside
module.exports = {
  MainApp
};