const { contextBridge, ipcRenderer } = require('electron')




contextBridge.exposeInMainWorld('electronAPI', {
    getUsers: () => ipcRenderer.invoke('get-users'),
    getTasks: () => ipcRenderer.invoke('get-tasks')
})
