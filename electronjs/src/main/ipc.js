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
        const result = await apiFetch('/api/login', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        });
        if (!result.success) return result;
        const user = { ...result.user, role: "Utilisateur" };
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
    if (!res.ok) {
        let message = `HTTP ${res.status}`;
        try {
            const data = await res.json();
            message = data.error || message;
        } catch {}
        throw new Error(message);
    }
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

ipcMain.handle('get-task', async (event, id) => {
    try { return await apiFetch(`/task/${id}`); }
    catch (e) { console.error(e); return null; }
});

ipcMain.handle('get-workspaces', async () => {
    try { return await apiFetch('/api/workspaces'); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('get-workspace', async (event, id) => {
    try { return await apiFetch(`/workspace/${id}`); }
    catch (e) { console.error(e); return null; }
});

ipcMain.handle('get-workspace-tasks', async (event, id) => {
    try { return await apiFetch(`/api/workspaces/${id}/tasks`); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('get-files', async () => {
    try { return await apiFetch('/api/files'); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('get-workspace-files', async (event, workspaceId) => {
    try { return await apiFetch(`/api/workspaces/${workspaceId}/files`); }
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

ipcMain.handle('update-user', async (event, id, data) => {
    try {
        const result = await apiFetch(`/api/users/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
        if (result.success && result.user) {
            const session = { user: { ...result.user, role: "Utilisateur" }, rememberMe: true, savedAt: Date.now() };
            fs.writeFileSync(getSessionFile(), JSON.stringify(session));
        }
        return result;
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

ipcMain.handle('update-task', async (event, id, data) => {
    try {
        return await apiFetch(`/task/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

ipcMain.handle('delete-task', async (event, id, userId) => {
    try {
        return await apiFetch(`/task/${id}`, {
            method: 'DELETE',
            body: JSON.stringify({ userId }),
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

ipcMain.handle('get-my-workspaces', async (event, userId) => {
    try { return await apiFetch(`/api/workspaces/mine?userId=${userId}`); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('get-workspace-members', async (event, workspaceId) => {
    try { return await apiFetch(`/api/workspaces/${workspaceId}/members`); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('add-workspace-member', async (event, workspaceId, userId, requesterId) => {
    try {
        return await apiFetch(`/api/workspaces/${workspaceId}/members`, {
            method: 'POST',
            body: JSON.stringify({ userId, requesterId }),
        });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

ipcMain.handle('remove-workspace-member', async (event, workspaceId, userId, requesterId) => {
    try {
        return await apiFetch(`/api/workspaces/${workspaceId}/members/${userId}`, {
            method: 'DELETE',
            body: JSON.stringify({ requesterId }),
        });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

ipcMain.handle('send-join-request', async (event, workspaceId, userId) => {
    try {
        return await apiFetch(`/api/workspaces/${workspaceId}/join-requests`, {
            method: 'POST',
            body: JSON.stringify({ userId }),
        });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

ipcMain.handle('get-join-requests', async (event, workspaceId, userId) => {
    try { return await apiFetch(`/api/workspaces/${workspaceId}/join-requests?userId=${userId}`); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('approve-join-request', async (event, requestId, userId) => {
    try {
        return await apiFetch(`/api/join-requests/${requestId}/approve`, {
            method: 'POST',
            body: JSON.stringify({ userId }),
        });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

ipcMain.handle('reject-join-request', async (event, requestId, userId) => {
    try {
        return await apiFetch(`/api/join-requests/${requestId}/reject`, {
            method: 'POST',
            body: JSON.stringify({ userId }),
        });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

ipcMain.handle('get-my-join-requests', async (event, userId) => {
    try { return await apiFetch(`/api/users/${userId}/join-requests`); }
    catch (e) { console.error(e); return []; }
});

// ── Comments ──

ipcMain.handle('get-task-comments', async (event, taskId) => {
    try { return await apiFetch(`/api/tasks/${taskId}/comments`); }
    catch (e) { console.error(e); return []; }
});

ipcMain.handle('add-task-comment', async (event, taskId, userId, text) => {
    try {
        return await apiFetch(`/api/tasks/${taskId}/comments`, {
            method: 'POST',
            body: JSON.stringify({ userId, text }),
        });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

ipcMain.handle('increment-task-view', async (event, taskId) => {
    try {
        return await apiFetch(`/api/tasks/${taskId}/view`, { method: 'POST' });
    } catch (e) {
        return { success: false, error: e.message };
    }
});

// ── User Stats ──

ipcMain.handle('get-user-stats', async (event, userId) => {
    try { return await apiFetch(`/api/users/${userId}/stats`); }
    catch (e) { console.error(e); return null; }
});

// ── Config ──

const CONFIG_FILE = path.join(app.getPath('userData'), 'config.json');

ipcMain.handle('get-config', () => {
    try {
        const raw = fs.readFileSync(CONFIG_FILE, 'utf8');
        return JSON.parse(raw);
    } catch {
        return { serverUrl: FLASK_BASE_URL };
    }
});

ipcMain.handle('save-config', async (event, config) => {
    try {
        fs.writeFileSync(CONFIG_FILE, JSON.stringify(config));
        return { success: true };
    } catch (e) {
        return { success: false, error: e.message };
    }
});

// ── Image Storage (handled via direct fetch in renderer) ──
