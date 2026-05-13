const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
    getUsers: () => ipcRenderer.invoke('get-users'),
    getTasks: () => ipcRenderer.invoke('get-tasks'),
    getWorkspaces: () => ipcRenderer.invoke('get-workspaces'),
    getFiles: () => ipcRenderer.invoke('get-files'),
    deleteFile: (id) => ipcRenderer.invoke('delete-file', id),
    createUser: (data) => ipcRenderer.invoke('create-user', data),
    createTask: (data) => ipcRenderer.invoke('create-task', data),
    createWorkspace: (data) => ipcRenderer.invoke('create-workspace', data),
    login: (credentials) => ipcRenderer.invoke('login', credentials),
    logout: () => ipcRenderer.invoke('logout'),
    checkSession: () => ipcRenderer.invoke('check-session'),
    navigate: (page) => ipcRenderer.send('navigate', page),
})
