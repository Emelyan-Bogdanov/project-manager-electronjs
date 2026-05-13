const { ipcMain, app } = require('electron');
const fs = require('fs');
const path = require('path');

const FLASK_BASE_URL = 'http://localhost:5000';

function getSessionFile() {
    return path.join(app.getPath('userData'), 'user-session.json');
}

ipcMain.handle('login', async (event, { username, password, rememberMe }) => {
    try {
        if (!username || !password) {
            return { success: false, error: "Nom d'utilisateur et mot de passe requis" };
        }
        const user = { id: 1, username, name: username, role: "Utilisateur" };
        const session = { user, rememberMe, savedAt: Date.now() };
        fs.writeFileSync(getSessionFile(), JSON.stringify(session));
        return { success: true, user };
    } catch (error) {
        return { success: false, error: error.message };
    }
});

ipcMain.handle('check-session', () => {
    try {
        const raw = fs.readFileSync(getSessionFile(), 'utf8');
        const session = JSON.parse(raw);
        if (session.rememberMe && session.user) {
            return { loggedIn: true, user: session.user };
        }
        return { loggedIn: false };
    } catch {
        return { loggedIn: false };
    }
});

ipcMain.handle('logout', () => {
    try { fs.unlinkSync(getSessionFile()); } catch {}
    return { success: true };
});

ipcMain.handle('get-users', async () => {
    try {
        const response = await fetch(`${FLASK_BASE_URL}/api/users`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const users = await response.json();
        return users;
    } catch (error) {
        console.error('Error fetching users:', error);
        return [];
    }
});

ipcMain.handle('get-tasks', async () => {
    try {
        const response = await fetch(`${FLASK_BASE_URL}/api/tasks`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const tasks = await response.json();
        return tasks;
    } catch (error) {
        console.error('Error fetching tasks:', error);
        return [];
    }
});

ipcMain.handle('get-workspaces', async () => {
    try {
        const response = await fetch(`${FLASK_BASE_URL}/api/workspaces`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const workspaces = await response.json();
        return workspaces;
    } catch (error) {
        console.error('Error fetching workspaces:', error);
        return [];
    }
});

ipcMain.handle('get-messages', async () => {
    try {
        // Note: Cette route n'existe pas encore dans le backend
        // Vous devrez l'ajouter dans messages.py
        const response = await fetch(`${FLASK_BASE_URL}/api/messages`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const messages = await response.json();
        return messages;
    } catch (error) {
        console.error('Error fetching messages:', error);
        return [];
    }
});
