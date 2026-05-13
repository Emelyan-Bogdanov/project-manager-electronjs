const { ipcMain, app } = require('electron');
const fs = require('fs');
const path = require('path');

const FLASK_BASE_URL = 'http://localhost:5000';

function getSessionFile() {
    return path.join(app.getPath('userData'), 'user-session.json');
}

// ── Auth ──

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

// ── API Proxy ──

async function apiFetch(url, options = {}) {
    const res = await fetch(`${FLASK_BASE_URL}${url}`, {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options,
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

ipcMain.handle('get-users', async () => {
    try { return await apiFetch('/api/users'); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('get-tasks', async () => {
    try { return await apiFetch('/api/tasks'); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('get-workspaces', async () => {
    try { return await apiFetch('/api/workspaces'); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('get-files', async () => {
    try { return await apiFetch('/api/files'); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('delete-file', async (event, fileId) => {
    try {
        return await apiFetch(`/api/files/${fileId}/delete`, { method: 'DELETE' });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

// ── Create ──

ipcMain.handle('create-user', async (event, data) => {
    try {
        return await apiFetch('/api/users', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

ipcMain.handle('create-task', async (event, data) => {
    try {
        return await apiFetch('/addtask', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

ipcMain.handle('create-workspace', async (event, data) => {
    try {
        return await apiFetch('/addworkspace', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    } catch (e) {
        return { success: false, error: e.message };
    }
});
